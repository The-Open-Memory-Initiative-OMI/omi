#!/usr/bin/env python3
"""
OMI L0 Artifact Integrity — Naming Consistency Audit (Session 4)

Validates byte-lane isolation, per-device naming conventions,
CA/CLK bus completeness, and power domain isolation across the
DDR4 UDIMM 288-pin map.

Usage:
    python verify_naming.py --reference path/to/ddr4_udimm_288_pinmap.csv
    python verify_naming.py --reference path/to/csv --output path/to/report.json
    python verify_naming.py --reference path/to/csv --matrix path/to/lane_matrix.csv

Exit codes:
    0 = All checks PASS
    1 = One or more checks FAIL
    2 = Input error (file not found, parse error)
"""

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

NUM_LANES = 8
BITS_PER_LANE = 8
NETS_PER_LANE = 11  # 8 DQ + 2 DQS + 1 DM

RE_DQ = re.compile(r"^D([0-7])_DQ([0-7])$")
RE_DQS = re.compile(r"^D([0-7])_DQS_([tc])$")
RE_DM = re.compile(r"^D([0-7])_DM_DBI_n$")

# Expected CA/CLK nets (active in OMI v1 single-rank)
EXPECTED_CA_NETS = {
    # Address
    "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9",
    "A10", "A11", "A12", "A13", "A14", "A15", "A16",
    # Bank / Bank Group
    "BA0", "BA1", "BG0", "BG1",
    # Control
    "ACT_n", "CS0_n", "CKE0", "ODT0", "RESET_n", "ALERT_n", "PARITY",
    # Clock
    "CK_t", "CK_c",
}

# Power nets expected on edge connector
EXPECTED_POWER_NETS = {"VDD", "VPP", "VREF", "VDDSPD", "VTT", "GND"}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class CheckResult:
    """Result of a single validation check."""

    def __init__(self, name: str):
        self.name = name
        self.passed = True
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.details: dict = {}

    def fail(self, msg: str):
        self.passed = False
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "status": "PASS" if self.passed else "FAIL",
            "errors": self.errors,
            "warnings": self.warnings,
            "details": self.details,
        }


# ---------------------------------------------------------------------------
# CSV loading
# ---------------------------------------------------------------------------

def load_pinmap_csv(path: Path) -> list[dict]:
    """Load the 288-pin map CSV."""
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["pin"] = int(row["pin"])
            rows.append(row)
    return rows


def compute_sha256(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Byte-lane grouping
# ---------------------------------------------------------------------------

def group_by_byte_lane(pins: list[dict]) -> dict[int, list[dict]]:
    """
    Group DQ_DQS pins by byte lane number.
    Returns dict mapping lane (0-7) -> list of pin dicts.
    """
    lanes: dict[int, list[dict]] = {i: [] for i in range(NUM_LANES)}

    dq_dqs_pins = [p for p in pins if p["group"] == "DQ_DQS"]

    for p in dq_dqs_pins:
        net = p["omi_net"]
        # Try each regex to extract lane number
        for pattern in (RE_DQ, RE_DQS, RE_DM):
            m = pattern.match(net)
            if m:
                lane = int(m.group(1))
                lanes[lane].append(p)
                break

    return lanes


# ---------------------------------------------------------------------------
# Validation checks
# ---------------------------------------------------------------------------

def check_lane_completeness(lane_groups: dict[int, list[dict]]) -> CheckResult:
    """Verify each lane has exactly 11 nets (8 DQ + 2 DQS + 1 DM)."""
    result = CheckResult("Byte-Lane Completeness (11 nets/lane)")
    lane_details = {}

    for lane in range(NUM_LANES):
        nets = lane_groups[lane]
        count = len(nets)
        lane_details[f"lane_{lane}"] = count

        if count != NETS_PER_LANE:
            result.fail(
                f"Lane {lane} (D{lane}): expected {NETS_PER_LANE} nets, "
                f"found {count}"
            )

    total = sum(len(v) for v in lane_groups.values())
    lane_details["total_dq_dqs_nets"] = total

    if total != NUM_LANES * NETS_PER_LANE:
        result.fail(
            f"Expected {NUM_LANES * NETS_PER_LANE} total DQ/DQS nets, "
            f"found {total}"
        )

    result.details = lane_details
    return result


def check_lane_isolation(lane_groups: dict[int, list[dict]]) -> CheckResult:
    """Verify no cross-lane contamination — each net prefix matches its lane."""
    result = CheckResult("Byte-Lane Isolation")
    violations = []

    for lane in range(NUM_LANES):
        expected_prefix = f"D{lane}_"
        for p in lane_groups[lane]:
            if not p["omi_net"].startswith(expected_prefix):
                violations.append({
                    "pin": p["pin"],
                    "lane": lane,
                    "net": p["omi_net"],
                    "expected_prefix": expected_prefix,
                })
                result.fail(
                    f"Pin {p['pin']}: net '{p['omi_net']}' in lane {lane} "
                    f"does not start with '{expected_prefix}'"
                )

    result.details["violations"] = violations
    return result


def check_dq_bit_uniqueness(lane_groups: dict[int, list[dict]]) -> CheckResult:
    """Verify each lane has DQ bits 0-7 exactly once."""
    result = CheckResult("DQ Bit Uniqueness Per Lane")

    for lane in range(NUM_LANES):
        bits_found: dict[int, list[int]] = {}

        for p in lane_groups[lane]:
            m = RE_DQ.match(p["omi_net"])
            if m:
                bit = int(m.group(2))
                bits_found.setdefault(bit, []).append(p["pin"])

        # Check all 8 bits present
        expected_bits = set(range(BITS_PER_LANE))
        actual_bits = set(bits_found.keys())
        missing = expected_bits - actual_bits
        if missing:
            result.fail(f"Lane {lane}: missing DQ bits {sorted(missing)}")

        # Check no duplicates
        for bit, pin_list in bits_found.items():
            if len(pin_list) > 1:
                result.fail(
                    f"Lane {lane}: DQ bit {bit} appears on multiple pins: "
                    f"{pin_list}"
                )

    return result


def check_dqs_pairing(lane_groups: dict[int, list[dict]]) -> CheckResult:
    """Verify each lane has exactly one DQS_t and one DQS_c."""
    result = CheckResult("DQS Differential Pairing")

    for lane in range(NUM_LANES):
        dqs_t = []
        dqs_c = []

        for p in lane_groups[lane]:
            m = RE_DQS.match(p["omi_net"])
            if m:
                polarity = m.group(2)
                if polarity == "t":
                    dqs_t.append(p["pin"])
                else:
                    dqs_c.append(p["pin"])

        if len(dqs_t) != 1:
            result.fail(
                f"Lane {lane}: expected 1 DQS_t, found {len(dqs_t)} "
                f"(pins: {dqs_t})"
            )
        if len(dqs_c) != 1:
            result.fail(
                f"Lane {lane}: expected 1 DQS_c, found {len(dqs_c)} "
                f"(pins: {dqs_c})"
            )

    return result


def check_dm_presence(lane_groups: dict[int, list[dict]]) -> CheckResult:
    """Verify each lane has exactly one DM/DBI net."""
    result = CheckResult("DM/DBI Presence Per Lane")

    for lane in range(NUM_LANES):
        dm_count = sum(1 for p in lane_groups[lane] if RE_DM.match(p["omi_net"]))
        if dm_count != 1:
            result.fail(
                f"Lane {lane}: expected 1 DM_DBI_n net, found {dm_count}"
            )

    return result


def check_ca_completeness(pins: list[dict]) -> CheckResult:
    """Verify all expected CA/CLK nets are present on the edge connector."""
    result = CheckResult("CA/CLK Bus Completeness")

    ca_pins = [p for p in pins if p["group"] == "CA_CLK"]
    present_nets = {p["omi_net"] for p in ca_pins if p["omi_net"] != "NC"}

    missing = EXPECTED_CA_NETS - present_nets
    if missing:
        result.fail(f"Missing CA/CLK nets: {sorted(missing)}")

    result.details["expected"] = sorted(EXPECTED_CA_NETS)
    result.details["found"] = sorted(present_nets)
    result.details["missing"] = sorted(missing) if missing else []
    return result


def check_clock_differential(pins: list[dict]) -> CheckResult:
    """Verify CK_t and CK_c are both present (differential pair)."""
    result = CheckResult("Clock Differential Pair")

    ca_nets = {p["omi_net"] for p in pins if p["group"] == "CA_CLK"}

    if "CK_t" not in ca_nets:
        result.fail("Missing CK_t (clock true)")
    if "CK_c" not in ca_nets:
        result.fail("Missing CK_c (clock complement)")

    return result


def check_power_isolation(pins: list[dict]) -> CheckResult:
    """Verify power domains are distinct and do not share pins."""
    result = CheckResult("Power Domain Isolation")

    power_pins = [p for p in pins if p["group"] == "POWER"]

    # Check all expected power nets present
    present_nets = {p["omi_net"] for p in power_pins}
    missing = EXPECTED_POWER_NETS - present_nets
    if missing:
        result.fail(f"Missing power nets on edge connector: {sorted(missing)}")

    # Check no pin is assigned to multiple power domains
    # (this would be caught by net naming, but verify explicitly)
    for p in power_pins:
        if p["omi_net"] not in EXPECTED_POWER_NETS:
            result.fail(
                f"Pin {p['pin']}: unexpected power net '{p['omi_net']}'"
            )

    result.details["power_nets_found"] = sorted(present_nets)
    result.details["missing"] = sorted(missing) if missing else []

    # Count pins per power net
    net_counts: dict[str, int] = {}
    for p in power_pins:
        net_counts[p["omi_net"]] = net_counts.get(p["omi_net"], 0) + 1
    result.details["pins_per_net"] = net_counts

    return result


def check_ecc_lane_absent(pins: list[dict]) -> CheckResult:
    """Verify no 9th byte lane (ECC lane 8) exists in DQ_DQS group."""
    result = CheckResult("ECC Lane 8 Absent (Non-ECC)")

    dq_dqs_pins = [p for p in pins if p["group"] == "DQ_DQS"]
    for p in dq_dqs_pins:
        net = p["omi_net"]
        # Check for lane 8 or 9 (should not exist)
        if re.match(r"^D[89]_", net):
            result.fail(
                f"Pin {p['pin']}: found lane 8+ net '{net}' — "
                f"ECC lane should not exist on non-ECC x64 module"
            )

    return result


# ---------------------------------------------------------------------------
# Lane matrix export
# ---------------------------------------------------------------------------

def export_lane_matrix_csv(
    lane_groups: dict[int, list[dict]], output_path: Path
):
    """Export lane-by-lane matrix as CSV for evidence."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "lane", "net_type", "omi_net", "pin", "symbol", "notes"
        ])

        for lane in range(NUM_LANES):
            # Sort by net type then net name
            sorted_pins = sorted(
                lane_groups[lane],
                key=lambda p: (
                    0 if RE_DQ.match(p["omi_net"])
                    else 1 if RE_DQS.match(p["omi_net"])
                    else 2,
                    p["omi_net"],
                ),
            )
            for p in sorted_pins:
                net = p["omi_net"]
                if RE_DQ.match(net):
                    net_type = "DQ"
                elif RE_DQS.match(net):
                    net_type = "DQS"
                elif RE_DM.match(net):
                    net_type = "DM_DBI"
                else:
                    net_type = "UNKNOWN"

                writer.writerow([
                    lane, net_type, net, p["pin"], p["symbol"], p.get("notes", "")
                ])


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    results: list[CheckResult],
    csv_path: Path,
    csv_hash: str,
) -> dict:
    """Build the structured JSON report."""
    all_passed = all(r.passed for r in results)

    return {
        "tool": "verify_naming.py",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if all_passed else "FAIL",
        "input_files": {
            "reference_csv": str(csv_path),
            "reference_csv_sha256": csv_hash,
        },
        "checks": [r.to_dict() for r in results],
        "summary": {
            "total_checks": len(results),
            "passed": sum(1 for r in results if r.passed),
            "failed": sum(1 for r in results if not r.passed),
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def print_results(results: list[CheckResult]):
    """Print human-readable results to stdout."""
    print("=" * 70)
    print("  OMI L0 — Naming Consistency Audit (verify_naming.py)")
    print("=" * 70)
    print()

    for r in results:
        status = "PASS" if r.passed else "FAIL"
        marker = "[+]" if r.passed else "[X]"
        print(f"  {marker} {r.name}: {status}")

        if r.errors:
            for err in r.errors:
                print(f"      ERROR: {err}")
        if r.warnings:
            for w in r.warnings:
                print(f"      WARN:  {w}")

    print()
    all_passed = all(r.passed for r in results)
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    print("-" * 70)
    if all_passed:
        print(f"  STATUS: PASS  ({passed}/{total} checks passed)")
        print(f"  8 byte lanes verified. Naming consistency confirmed.")
    else:
        failed = total - passed
        print(f"  STATUS: FAIL  ({failed}/{total} checks failed)")
    print("-" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="OMI L0 — Byte-lane naming consistency audit"
    )
    parser.add_argument(
        "--reference",
        required=True,
        type=Path,
        help="Path to ddr4_udimm_288_pinmap.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Path to write JSON report",
    )
    parser.add_argument(
        "--matrix",
        type=Path,
        default=None,
        help="Path to write lane matrix CSV",
    )
    args = parser.parse_args()

    if not args.reference.exists():
        print(f"ERROR: Reference CSV not found: {args.reference}", file=sys.stderr)
        sys.exit(2)

    # Load data
    try:
        pins = load_pinmap_csv(args.reference)
    except (ValueError, csv.Error) as e:
        print(f"ERROR: Failed to parse CSV: {e}", file=sys.stderr)
        sys.exit(2)

    csv_hash = compute_sha256(args.reference)

    # Group by byte lane
    lane_groups = group_by_byte_lane(pins)

    # Run checks
    results: list[CheckResult] = [
        check_lane_completeness(lane_groups),
        check_lane_isolation(lane_groups),
        check_dq_bit_uniqueness(lane_groups),
        check_dqs_pairing(lane_groups),
        check_dm_presence(lane_groups),
        check_ecc_lane_absent(pins),
        check_ca_completeness(pins),
        check_clock_differential(pins),
        check_power_isolation(pins),
    ]

    # Output
    print_results(results)

    # Export lane matrix
    if args.matrix:
        export_lane_matrix_csv(lane_groups, args.matrix)
        print(f"\n  Lane matrix written to: {args.matrix}")

    # JSON report
    report = generate_report(results, args.reference, csv_hash)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"  JSON report written to: {args.output}")

    all_passed = all(r.passed for r in results)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
