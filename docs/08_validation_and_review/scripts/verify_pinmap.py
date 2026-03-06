#!/usr/bin/env python3
"""
OMI L0 Artifact Integrity — Pin Map Verification (Session 3)

Validates the DDR4 UDIMM 288-pin edge connector mapping against
structural integrity rules, net naming conventions, and optional
net manifest cross-referencing.

Usage:
    python verify_pinmap.py --reference path/to/ddr4_udimm_288_pinmap.csv
    python verify_pinmap.py --reference path/to/csv --manifest path/to/net_manifest.md
    python verify_pinmap.py --reference path/to/csv --output path/to/report.json

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
# Constants — derived from naming_rules.md and net manifest
# ---------------------------------------------------------------------------

EXPECTED_PIN_COUNT = 288

VALID_POWER_NETS = {"VDD", "VDDQ", "VPP", "VREF", "VDDSPD", "VTT", "GND"}

VALID_SPD_NETS = {"SPD_SDA", "SPD_SCL", "SA0", "SA1", "SA2"}

VALID_CA_NETS = {
    # Address
    "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9",
    "A10", "A11", "A12", "A13", "A14", "A15", "A16", "A17",
    # Bank / Bank Group
    "BA0", "BA1", "BG0", "BG1",
    # Control
    "ACT_n", "CS0_n", "CKE0", "ODT0", "RESET_n", "ALERT_n", "PARITY",
    # Clock
    "CK_t", "CK_c",
}

# Rank-1 signals that must be NC in single-rank v1
SINGLE_RANK_NC_SYMBOLS = {"CS1_n", "ODT1", "CKE1", "CK1_t", "CK1_c"}

# ECC/CB symbols that must be NC on non-ECC x64 module
ECC_SYMBOLS = {
    "CB0/NC", "CB1/NC", "CB2/NC", "CB3/NC",
    "CB4/NC", "CB5/NC", "CB6/NC", "CB7/NC",
    "CB7/DBI8_n", "CB6/DBI8_n",
    "DM8_n/DBI8_n", "DQS8_c", "DQS8_t",
}

# Regex for valid DQ_DQS group omi_net values
RE_DQ = re.compile(r"^D[0-7]_DQ[0-7]$")
RE_DQS = re.compile(r"^D[0-7]_DQS_[tc]$")
RE_DM = re.compile(r"^D[0-7]_DM_DBI_n$")

VALID_GROUPS = {"DQ_DQS", "CA_CLK", "POWER", "SPD", "OTHER"}


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
    """Load the 288-pin map CSV. Returns list of row dicts."""
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        expected_cols = {"pin", "symbol", "omi_net", "group", "notes"}
        if not expected_cols.issubset(set(reader.fieldnames or [])):
            missing = expected_cols - set(reader.fieldnames or [])
            raise ValueError(f"CSV missing required columns: {missing}")
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
# Validation checks
# ---------------------------------------------------------------------------

def check_pin_completeness(pins: list[dict]) -> CheckResult:
    """Verify exactly 288 unique pins numbered 1-288, no duplicates or gaps."""
    result = CheckResult("Pin Completeness (288/288)")

    pin_numbers = [p["pin"] for p in pins]
    result.details["total_rows"] = len(pins)

    # Check count
    if len(pins) != EXPECTED_PIN_COUNT:
        result.fail(f"Expected {EXPECTED_PIN_COUNT} rows, got {len(pins)}")

    # Check duplicates
    seen = {}
    for p in pins:
        n = p["pin"]
        if n in seen:
            result.fail(f"Duplicate pin number: {n}")
        seen[n] = True

    # Check range 1-288
    expected = set(range(1, EXPECTED_PIN_COUNT + 1))
    actual = set(pin_numbers)
    missing = expected - actual
    extra = actual - expected

    if missing:
        result.fail(f"Missing pin numbers: {sorted(missing)}")
    if extra:
        result.fail(f"Unexpected pin numbers: {sorted(extra)}")

    result.details["unique_pins"] = len(actual)
    result.details["missing"] = sorted(missing)
    result.details["duplicates"] = sorted(
        n for n, c in __import__("collections").Counter(pin_numbers).items() if c > 1
    )

    return result


def check_group_validity(pins: list[dict]) -> CheckResult:
    """Verify all pins have a recognized group value."""
    result = CheckResult("Group Validity")
    invalid = []
    for p in pins:
        if p["group"] not in VALID_GROUPS:
            invalid.append((p["pin"], p["group"]))
    if invalid:
        for pin, grp in invalid:
            result.fail(f"Pin {pin}: invalid group '{grp}'")
    result.details["invalid_groups"] = invalid
    return result


def check_net_naming(pins: list[dict]) -> CheckResult:
    """Verify omi_net values conform to naming rules per group."""
    result = CheckResult("Net Naming Conformance")
    violations = []

    for p in pins:
        pin = p["pin"]
        net = p["omi_net"]
        group = p["group"]

        if not net or net.strip() == "":
            result.fail(f"Pin {pin}: empty omi_net")
            violations.append(pin)
            continue

        if group == "DQ_DQS":
            if not (RE_DQ.match(net) or RE_DQS.match(net) or RE_DM.match(net)):
                result.fail(
                    f"Pin {pin}: DQ_DQS net '{net}' does not match "
                    f"D[0-7]_DQ[0-7] | D[0-7]_DQS_[tc] | D[0-7]_DM_DBI_n"
                )
                violations.append(pin)

        elif group == "POWER":
            if net not in VALID_POWER_NETS:
                result.fail(f"Pin {pin}: POWER net '{net}' not in {VALID_POWER_NETS}")
                violations.append(pin)

        elif group == "SPD":
            if net not in VALID_SPD_NETS:
                result.fail(f"Pin {pin}: SPD net '{net}' not in {VALID_SPD_NETS}")
                violations.append(pin)

        elif group == "CA_CLK":
            if net not in VALID_CA_NETS and net != "NC":
                result.fail(f"Pin {pin}: CA_CLK net '{net}' not in known CA set or NC")
                violations.append(pin)

        elif group == "OTHER":
            if net != "NC":
                result.fail(f"Pin {pin}: OTHER group net '{net}' should be 'NC'")
                violations.append(pin)

    result.details["violation_count"] = len(violations)
    result.details["violating_pins"] = violations
    return result


def check_ecc_exclusion(pins: list[dict]) -> CheckResult:
    """Verify all ECC/CB pins are mapped to NC (non-ECC x64 module)."""
    result = CheckResult("ECC Exclusion (Non-ECC x64)")
    violations = []

    for p in pins:
        symbol = p["symbol"]
        net = p["omi_net"]
        # Check against known ECC symbol patterns
        if symbol in ECC_SYMBOLS or "CB" in symbol:
            if net != "NC":
                result.fail(
                    f"Pin {p['pin']}: ECC symbol '{symbol}' mapped to '{net}', "
                    f"expected 'NC'"
                )
                violations.append(p["pin"])

    result.details["ecc_violations"] = violations
    return result


def check_single_rank_exclusion(pins: list[dict]) -> CheckResult:
    """Verify rank-1 signals are NC in single-rank v1 config."""
    result = CheckResult("Single-Rank Exclusion (1R)")
    violations = []

    for p in pins:
        symbol = p["symbol"]
        net = p["omi_net"]
        if symbol in SINGLE_RANK_NC_SYMBOLS:
            if net != "NC":
                result.fail(
                    f"Pin {p['pin']}: rank-1 symbol '{symbol}' mapped to '{net}', "
                    f"expected 'NC' for single-rank v1"
                )
                violations.append(p["pin"])

    result.details["rank1_violations"] = violations
    return result


def check_power_net_presence(pins: list[dict]) -> CheckResult:
    """Verify that required power nets are present on the edge connector."""
    result = CheckResult("Power Net Presence")

    power_pins = [p for p in pins if p["group"] == "POWER"]
    present_nets = {p["omi_net"] for p in power_pins}

    # VDDQ is internal (not on edge connector) — exclude from this check
    required_on_edge = {"VDD", "VPP", "VREF", "VDDSPD", "VTT", "GND"}
    missing = required_on_edge - present_nets
    if missing:
        result.fail(f"Missing power nets on edge connector: {missing}")

    result.details["power_nets_found"] = sorted(present_nets)
    result.details["missing_power_nets"] = sorted(missing) if missing else []
    return result


def parse_manifest_nets(path: Path) -> set[str]:
    """Extract net names from the Stage 7.5 net manifest markdown."""
    nets = set()
    # Pattern for range notation: `D1_DQ0`–`D1_DQ7`
    range_re = re.compile(
        r"^\|\s*`([^`]+)`[\s\u2013\-]+`([^`]+)`\s*\|"
    )
    single_re = re.compile(r"^\|\s*`([^`]+)`\s*\|")

    with open(path, encoding="utf-8") as f:
        for line in f:
            # Try range notation first (e.g., `D1_DQ0`–`D1_DQ7`)
            rm = range_re.match(line)
            if rm:
                start_net = rm.group(1)
                end_net = rm.group(2)
                # Expand range: extract trailing digit and generate sequence
                start_m = re.match(r"^(.+?)(\d+)$", start_net)
                end_m = re.match(r"^(.+?)(\d+)$", end_net)
                if start_m and end_m and start_m.group(1) == end_m.group(1):
                    prefix = start_m.group(1)
                    for i in range(int(start_m.group(2)), int(end_m.group(2)) + 1):
                        nets.add(f"{prefix}{i}")
                else:
                    nets.add(start_net)
                    nets.add(end_net)
                continue

            # Single net name
            sm = single_re.match(line)
            if sm:
                nets.add(sm.group(1))

    return nets


def check_manifest_cross_ref(
    pins: list[dict], manifest_path: Path
) -> CheckResult:
    """Cross-reference CSV omi_nets against the net manifest."""
    result = CheckResult("Manifest Cross-Reference")

    manifest_nets = parse_manifest_nets(manifest_path)
    result.details["manifest_net_count"] = len(manifest_nets)

    # Collect unique non-NC, non-GND omi_nets from CSV
    csv_nets = {
        p["omi_net"]
        for p in pins
        if p["omi_net"] not in ("NC", "GND")
    }
    result.details["csv_unique_nets"] = len(csv_nets)

    # Nets in CSV but not in manifest
    not_in_manifest = csv_nets - manifest_nets
    if not_in_manifest:
        for net in sorted(not_in_manifest):
            result.warn(f"CSV net '{net}' not found in manifest")
        result.details["not_in_manifest"] = sorted(not_in_manifest)

    # Nets in manifest but not in CSV (some are expected, like VDDQ, A17, PAR, EVENT_n)
    expected_internal = {"VDDQ", "A17", "PAR", "EVENT_n"}
    not_in_csv = manifest_nets - csv_nets - {"GND"} - expected_internal
    # Also exclude rank-1 signals already handled
    rank1_nets = {"CK1_t", "CK1_c", "CKE1", "ODT1", "CS1_n"}
    not_in_csv -= rank1_nets

    if not_in_csv:
        for net in sorted(not_in_csv):
            result.warn(f"Manifest net '{net}' not found as omi_net in CSV")
        result.details["not_in_csv"] = sorted(not_in_csv)

    return result


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    results: list[CheckResult],
    csv_path: Path,
    csv_hash: str,
    manifest_path: Path | None = None,
) -> dict:
    """Build the structured JSON report."""
    all_passed = all(r.passed for r in results)

    report = {
        "tool": "verify_pinmap.py",
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

    if manifest_path:
        report["input_files"]["manifest"] = str(manifest_path)
        report["input_files"]["manifest_sha256"] = compute_sha256(manifest_path)

    return report


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def print_results(results: list[CheckResult]):
    """Print human-readable results to stdout."""
    print("=" * 70)
    print("  OMI L0 — Pin Map Verification (verify_pinmap.py)")
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
        print(f"  288 pins mapped, matched, and verified.")
    else:
        failed = total - passed
        print(f"  STATUS: FAIL  ({failed}/{total} checks failed)")
    print("-" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="OMI L0 — DDR4 UDIMM 288-pin map verification"
    )
    parser.add_argument(
        "--reference",
        required=True,
        type=Path,
        help="Path to ddr4_udimm_288_pinmap.csv",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Path to Stage 7.5 net manifest markdown (optional cross-check)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Path to write JSON report (default: stdout only)",
    )
    args = parser.parse_args()

    # Validate inputs
    if not args.reference.exists():
        print(f"ERROR: Reference CSV not found: {args.reference}", file=sys.stderr)
        sys.exit(2)
    if args.manifest and not args.manifest.exists():
        print(f"ERROR: Manifest not found: {args.manifest}", file=sys.stderr)
        sys.exit(2)

    # Load data
    try:
        pins = load_pinmap_csv(args.reference)
    except (ValueError, csv.Error) as e:
        print(f"ERROR: Failed to parse CSV: {e}", file=sys.stderr)
        sys.exit(2)

    csv_hash = compute_sha256(args.reference)

    # Run checks
    results: list[CheckResult] = [
        check_pin_completeness(pins),
        check_group_validity(pins),
        check_net_naming(pins),
        check_ecc_exclusion(pins),
        check_single_rank_exclusion(pins),
        check_power_net_presence(pins),
    ]

    # Optional manifest cross-reference
    if args.manifest:
        results.append(check_manifest_cross_ref(pins, args.manifest))

    # Output
    print_results(results)

    report = generate_report(results, args.reference, csv_hash, args.manifest)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"\n  JSON report written to: {args.output}")

    # Exit code
    all_passed = all(r.passed for r in results)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
