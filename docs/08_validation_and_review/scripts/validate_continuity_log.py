#!/usr/bin/env python3
"""
OMI L1 Bench Electrical — Continuity Log Validator

Parses a tester-submitted measurement CSV and validates each entry
against L1 pass/fail thresholds derived from 08-2_bringup_ladder.md.

Usage:
    python validate_continuity_log.py \\
        --reference path/to/ddr4_udimm_288_pinmap.csv \\
        --measurements path/to/measurement_log.csv
    python validate_continuity_log.py \\
        --reference path/to/csv --measurements path/to/log.csv \\
        --output path/to/report.json

Measurement CSV format (columns):
    pin,symbol,omi_net,group,measurement_type,measured_value,unit,pass_fail,notes

Exit codes:
    0 = All checks PASS
    1 = One or more checks FAIL
    2 = Input error (file not found, parse error)
"""

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants — L1 thresholds per 08-2_bringup_ladder.md
# ---------------------------------------------------------------------------

GND_RESISTANCE_MAX_OHM = 1.0
SIGNAL_CONTINUITY_MAX_OHM = 10.0
NC_ISOLATION_MIN_OHM = 1_000_000  # 1 MΩ
RAIL_ISOLATION_MIN_OHM = 10_000  # 10 kΩ

# Voltage specs
VDD_NOMINAL_V = 1.2
VDD_TOLERANCE = 0.05
VPP_NOMINAL_V = 2.5
VPP_TOLERANCE = 0.05
VDDSPD_MIN_V = 2.2
VDDSPD_MAX_V = 3.6

VOLTAGE_SPECS = {
    "VDD": (VDD_NOMINAL_V * (1 - VDD_TOLERANCE), VDD_NOMINAL_V * (1 + VDD_TOLERANCE)),
    "VPP": (VPP_NOMINAL_V * (1 - VPP_TOLERANCE), VPP_NOMINAL_V * (1 + VPP_TOLERANCE)),
    "VDDSPD": (VDDSPD_MIN_V, VDDSPD_MAX_V),
    "VTT": (VDD_NOMINAL_V * 0.45, VDD_NOMINAL_V * 0.55),
    "VREF": (VDD_NOMINAL_V * 0.45, VDD_NOMINAL_V * 0.55),
}


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
        expected_cols = {"pin", "symbol", "omi_net", "group", "notes"}
        if not expected_cols.issubset(set(reader.fieldnames or [])):
            missing = expected_cols - set(reader.fieldnames or [])
            raise ValueError(f"CSV missing required columns: {missing}")
        for row in reader:
            row["pin"] = int(row["pin"])
            rows.append(row)
    return rows


def load_measurement_csv(path: Path) -> list[dict]:
    """Load the tester's measurement CSV."""
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"pin", "measurement_type", "measured_value", "unit"}
        fieldnames = set(reader.fieldnames or [])
        if not required.issubset(fieldnames):
            missing = required - fieldnames
            raise ValueError(f"Measurement CSV missing columns: {missing}")
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


def parse_measured_value(value_str: str) -> float | None:
    """Parse a measured value string to float. Returns None if not numeric."""
    if not value_str or value_str.strip() == "":
        return None
    cleaned = value_str.strip().upper()
    if cleaned in ("PASS", "FAIL", "OL", "OPEN", "N/A"):
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Validation checks
# ---------------------------------------------------------------------------

def check_measurement_completeness(
    reference: list[dict], measurements: list[dict]
) -> CheckResult:
    """Verify every functional pin has a measurement entry."""
    result = CheckResult("Measurement Completeness")

    ref_pins = {p["pin"] for p in reference}
    meas_pins = {m["pin"] for m in measurements}

    # Functional pins = everything except NC-only pins
    functional_pins = set()
    for p in reference:
        if p["omi_net"] != "NC":
            functional_pins.add(p["pin"])

    missing = functional_pins - meas_pins
    if missing:
        result.fail(
            f"{len(missing)} functional pin(s) have no measurement: "
            f"{sorted(missing)[:20]}{'...' if len(missing) > 20 else ''}"
        )

    result.details["total_reference_pins"] = len(ref_pins)
    result.details["total_measurement_rows"] = len(meas_pins)
    result.details["functional_pins"] = len(functional_pins)
    result.details["missing_measurements"] = sorted(missing)

    return result


def check_gnd_resistance(
    reference: list[dict], measurements: list[dict]
) -> CheckResult:
    """Verify all GND pin measurements are ≤1 Ω."""
    result = CheckResult("GND Resistance (<=1 ohm)")

    gnd_pins = {p["pin"] for p in reference if p["omi_net"] == "GND"}
    meas_by_pin = {m["pin"]: m for m in measurements}

    checked = 0
    violations = []

    for pin in sorted(gnd_pins):
        m = meas_by_pin.get(pin)
        if not m:
            continue

        checked += 1
        value = parse_measured_value(m.get("measured_value", ""))
        pass_fail = m.get("pass_fail", "").strip().upper()

        if pass_fail == "FAIL":
            violations.append(pin)
            result.fail(f"Pin {pin}: tester marked FAIL")
        elif value is not None and value > GND_RESISTANCE_MAX_OHM:
            violations.append(pin)
            result.fail(
                f"Pin {pin}: GND resistance {value} ohm "
                f"exceeds {GND_RESISTANCE_MAX_OHM} ohm"
            )

    result.details["gnd_pins_total"] = len(gnd_pins)
    result.details["gnd_pins_checked"] = checked
    result.details["violations"] = violations

    if checked == 0 and len(gnd_pins) > 0:
        result.warn("No GND pin measurements found in log")

    return result


def check_signal_continuity(
    reference: list[dict], measurements: list[dict]
) -> CheckResult:
    """Verify all signal pins show continuity (PASS or ≤10 Ω)."""
    result = CheckResult("Signal Continuity")

    signal_pins = set()
    for p in reference:
        if p["group"] in ("DQ_DQS", "SPD"):
            signal_pins.add(p["pin"])
        elif p["group"] == "CA_CLK" and p["omi_net"] != "NC":
            signal_pins.add(p["pin"])

    meas_by_pin = {m["pin"]: m for m in measurements}

    checked = 0
    violations = []

    for pin in sorted(signal_pins):
        m = meas_by_pin.get(pin)
        if not m:
            continue

        checked += 1
        value = parse_measured_value(m.get("measured_value", ""))
        pass_fail = m.get("pass_fail", "").strip().upper()
        mtype = m.get("measurement_type", "").strip().lower()

        if pass_fail == "FAIL":
            violations.append(pin)
            result.fail(f"Pin {pin}: tester marked FAIL (open circuit?)")
        elif mtype == "continuity" and pass_fail == "PASS":
            continue  # Continuity beep = good
        elif value is not None and value > SIGNAL_CONTINUITY_MAX_OHM:
            violations.append(pin)
            result.fail(
                f"Pin {pin}: resistance {value} ohm "
                f"exceeds {SIGNAL_CONTINUITY_MAX_OHM} ohm — possible open"
            )
        elif value is not None and mtype == "resistance" and value <= SIGNAL_CONTINUITY_MAX_OHM:
            continue  # Low resistance = good
        elif pass_fail not in ("PASS", "FAIL", "") and value is None:
            result.warn(
                f"Pin {pin}: unrecognized measurement '{m.get('measured_value', '')}'"
            )

    result.details["signal_pins_total"] = len(signal_pins)
    result.details["signal_pins_checked"] = checked
    result.details["violations"] = violations

    if checked == 0 and len(signal_pins) > 0:
        result.warn("No signal pin measurements found in log")

    return result


def check_nc_isolation(
    reference: list[dict], measurements: list[dict]
) -> CheckResult:
    """Verify NC pins show ≥1 MΩ isolation (no shorts)."""
    result = CheckResult("NC Pin Isolation (>=1 Mohm)")

    nc_pins = {p["pin"] for p in reference if p["omi_net"] == "NC"}
    meas_by_pin = {m["pin"]: m for m in measurements}

    checked = 0
    violations = []

    for pin in sorted(nc_pins):
        m = meas_by_pin.get(pin)
        if not m:
            continue

        checked += 1
        value = parse_measured_value(m.get("measured_value", ""))
        pass_fail = m.get("pass_fail", "").strip().upper()
        val_str = m.get("measured_value", "").strip().upper()

        if pass_fail == "FAIL":
            violations.append(pin)
            result.fail(f"Pin {pin}: tester marked FAIL — possible short")
        elif val_str in ("OL", "OPEN"):
            continue  # Open/overload = infinite resistance = good
        elif pass_fail == "PASS":
            continue  # Tester confirmed isolation
        elif value is not None and value < NC_ISOLATION_MIN_OHM:
            violations.append(pin)
            result.fail(
                f"Pin {pin}: NC isolation {value} ohm "
                f"below {NC_ISOLATION_MIN_OHM / 1e6:.0f} Mohm — short detected"
            )

    result.details["nc_pins_total"] = len(nc_pins)
    result.details["nc_pins_checked"] = checked
    result.details["violations"] = violations

    if checked == 0 and len(nc_pins) > 0:
        result.warn("No NC pin isolation measurements found in log")

    return result


def check_power_continuity(
    reference: list[dict], measurements: list[dict]
) -> CheckResult:
    """Verify power rail pins within same rail show continuity."""
    result = CheckResult("Power Rail Continuity")

    power_rails = {}
    for p in reference:
        if p["group"] == "POWER" and p["omi_net"] != "GND":
            net = p["omi_net"]
            if net not in power_rails:
                power_rails[net] = []
            power_rails[net].append(p["pin"])

    meas_by_pin = {m["pin"]: m for m in measurements}

    checked = 0
    violations = []

    for net, rail_pins in sorted(power_rails.items()):
        for pin in rail_pins:
            m = meas_by_pin.get(pin)
            if not m:
                continue

            checked += 1
            pass_fail = m.get("pass_fail", "").strip().upper()
            value = parse_measured_value(m.get("measured_value", ""))

            if pass_fail == "FAIL":
                violations.append(pin)
                result.fail(f"Pin {pin} ({net}): tester marked FAIL")
            elif value is not None and value > SIGNAL_CONTINUITY_MAX_OHM:
                violations.append(pin)
                result.fail(
                    f"Pin {pin} ({net}): resistance {value} ohm — "
                    f"possible open on {net} rail"
                )

    result.details["power_rails"] = {
        net: pins for net, pins in sorted(power_rails.items())
    }
    result.details["checked"] = checked
    result.details["violations"] = violations

    return result


def check_rail_isolation(
    reference: list[dict], measurements: list[dict]
) -> CheckResult:
    """Verify cross-rail isolation ≥10 kΩ."""
    result = CheckResult("Rail-to-Rail Isolation (>=10 kohm)")

    # Look for rail isolation measurements in the log
    # These have measurement_type "isolation" or "resistance" with
    # omi_net like "VDD_to_VPP"
    isolation_measurements = [
        m for m in measurements
        if m.get("measurement_type", "").strip().lower() in ("isolation", "resistance")
        and "_to_" in m.get("omi_net", "")
    ]

    checked = 0
    violations = []

    for m in isolation_measurements:
        checked += 1
        value = parse_measured_value(m.get("measured_value", ""))
        pass_fail = m.get("pass_fail", "").strip().upper()
        pair = m.get("omi_net", "")
        val_str = m.get("measured_value", "").strip().upper()

        if pass_fail == "FAIL":
            violations.append(pair)
            result.fail(f"{pair}: tester marked FAIL — rail short suspected")
        elif val_str in ("OL", "OPEN"):
            continue  # Infinite resistance = perfect isolation
        elif pass_fail == "PASS":
            continue
        elif value is not None and value < RAIL_ISOLATION_MIN_OHM:
            violations.append(pair)
            result.fail(
                f"{pair}: isolation {value} ohm "
                f"below {RAIL_ISOLATION_MIN_OHM / 1e3:.0f} kohm"
            )

    result.details["isolation_pairs_checked"] = checked
    result.details["violations"] = violations

    if checked == 0:
        result.warn(
            "No rail isolation measurements found. "
            "Expected rows with measurement_type='isolation' "
            "and omi_net like 'VDD_to_VPP'."
        )

    return result


def check_rail_voltage(
    reference: list[dict], measurements: list[dict]
) -> CheckResult:
    """Verify powered rail voltages are within spec."""
    result = CheckResult("Rail Voltage (Powered)")

    voltage_measurements = [
        m for m in measurements
        if m.get("measurement_type", "").strip().lower() == "voltage"
        and m.get("omi_net", "") in VOLTAGE_SPECS
    ]

    checked = 0
    violations = []

    for m in voltage_measurements:
        checked += 1
        net = m["omi_net"]
        value = parse_measured_value(m.get("measured_value", ""))
        pass_fail = m.get("pass_fail", "").strip().upper()

        if pass_fail == "FAIL":
            violations.append(net)
            result.fail(f"{net}: tester marked FAIL")
        elif value is not None:
            v_min, v_max = VOLTAGE_SPECS[net]
            if value < v_min or value > v_max:
                violations.append(net)
                result.fail(
                    f"{net}: measured {value} V outside spec "
                    f"[{v_min:.3f}, {v_max:.3f}] V"
                )

    result.details["voltage_checks"] = checked
    result.details["violations"] = violations

    if checked == 0:
        result.warn(
            "No rail voltage measurements found. "
            "Expected rows with measurement_type='voltage' "
            "for VDD, VPP, VDDSPD, VTT, VREF."
        )

    return result


def check_spd_bus(
    reference: list[dict], measurements: list[dict]
) -> CheckResult:
    """Verify SPD bus integrity (SCL, SDA, SA, VDDSPD continuity)."""
    result = CheckResult("SPD Bus Integrity")

    spd_pins = {p["pin"] for p in reference if p["group"] == "SPD"}
    vddspd_pins = {p["pin"] for p in reference if p["omi_net"] == "VDDSPD"}
    all_spd = spd_pins | vddspd_pins

    meas_by_pin = {m["pin"]: m for m in measurements}

    checked = 0
    violations = []

    for pin in sorted(all_spd):
        m = meas_by_pin.get(pin)
        if not m:
            continue

        checked += 1
        pass_fail = m.get("pass_fail", "").strip().upper()

        if pass_fail == "FAIL":
            ref_pin = next((p for p in reference if p["pin"] == pin), {})
            net = ref_pin.get("omi_net", f"pin {pin}")
            violations.append(pin)
            result.fail(
                f"Pin {pin} ({net}): SPD bus signal FAIL — "
                f"see FS-01 in failure_signatures.md"
            )

    result.details["spd_pins_total"] = len(all_spd)
    result.details["spd_pins_checked"] = checked
    result.details["violations"] = violations

    if checked == 0 and len(all_spd) > 0:
        result.warn("No SPD bus measurements found in log")

    return result


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    results: list[CheckResult],
    reference_path: Path,
    reference_hash: str,
    measurements_path: Path,
    measurements_hash: str,
) -> dict:
    """Build the structured JSON report."""
    all_passed = all(r.passed for r in results)

    return {
        "tool": "validate_continuity_log.py",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if all_passed else "FAIL",
        "input_files": {
            "reference_csv": str(reference_path),
            "reference_csv_sha256": reference_hash,
            "measurements_csv": str(measurements_path),
            "measurements_csv_sha256": measurements_hash,
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
    print("  OMI L1 — Continuity Log Validation")
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
    else:
        failed = total - passed
        print(f"  STATUS: FAIL  ({failed}/{total} checks failed)")
    print("-" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="OMI L1 — Continuity Log Validator"
    )
    parser.add_argument(
        "--reference",
        required=True,
        type=Path,
        help="Path to ddr4_udimm_288_pinmap.csv",
    )
    parser.add_argument(
        "--measurements",
        required=True,
        type=Path,
        help="Path to tester's measurement CSV",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Path to write JSON report",
    )
    args = parser.parse_args()

    # Validate inputs
    if not args.reference.exists():
        print(f"ERROR: Reference CSV not found: {args.reference}", file=sys.stderr)
        sys.exit(2)
    if not args.measurements.exists():
        print(f"ERROR: Measurements CSV not found: {args.measurements}", file=sys.stderr)
        sys.exit(2)

    # Load data
    try:
        reference = load_pinmap_csv(args.reference)
    except (ValueError, csv.Error) as e:
        print(f"ERROR: Failed to parse reference CSV: {e}", file=sys.stderr)
        sys.exit(2)

    try:
        measurements = load_measurement_csv(args.measurements)
    except (ValueError, csv.Error) as e:
        print(f"ERROR: Failed to parse measurement CSV: {e}", file=sys.stderr)
        sys.exit(2)

    ref_hash = compute_sha256(args.reference)
    meas_hash = compute_sha256(args.measurements)

    # Run checks
    results: list[CheckResult] = [
        check_measurement_completeness(reference, measurements),
        check_gnd_resistance(reference, measurements),
        check_signal_continuity(reference, measurements),
        check_nc_isolation(reference, measurements),
        check_power_continuity(reference, measurements),
        check_rail_isolation(reference, measurements),
        check_rail_voltage(reference, measurements),
        check_spd_bus(reference, measurements),
    ]

    # Output
    print_results(results)

    report = generate_report(
        results, args.reference, ref_hash, args.measurements, meas_hash
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"\n  JSON report written to: {args.output}")

    all_passed = all(r.passed for r in results)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
