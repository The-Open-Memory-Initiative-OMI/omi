#!/usr/bin/env python3
"""
OMI L1 Bench Electrical — Probe Sequence Generator

Reads the canonical DDR4 UDIMM 288-pin map CSV and produces a structured
probing checklist organized by L1 session and pin group.  The output tells
the bench tester exactly which pins to measure and what thresholds apply.

Usage:
    python generate_probe_sequence.py --reference path/to/ddr4_udimm_288_pinmap.csv
    python generate_probe_sequence.py --reference path/to/csv --format markdown --output checklist.md
    python generate_probe_sequence.py --reference path/to/csv --output probes.csv

Exit codes:
    0 = Probe sequence generated successfully
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

# Session 1: Continuity (unpowered)
GND_RESISTANCE_MAX_OHM = 1.0
SIGNAL_CONTINUITY_MAX_OHM = 10.0
NC_ISOLATION_MIN_OHM = 1_000_000  # 1 MΩ

# Session 2: PDN (powered)
RAIL_ISOLATION_MIN_OHM = 10_000  # 10 kΩ
VDD_NOMINAL_V = 1.2
VDD_TOLERANCE = 0.05  # ±5%
VPP_NOMINAL_V = 2.5
VPP_TOLERANCE = 0.05
VDDSPD_MIN_V = 2.2
VDDSPD_MAX_V = 3.6
VTT_NOMINAL_RATIO = 0.5  # VDD / 2
VREF_NOMINAL_RATIO = 0.5  # VDD / 2

# Key diagnostic pins from 08-5_failure_signatures.md
DIAGNOSTIC_PINS = {
    "VDD_REFERENCE": 64,
    "VDDSPD": 284,
    "VPP_FIRST": 142,
    "VREF": 146,
    "VTT_FIRST": 77,
    "VTT_SECOND": 221,
    "RESET_n": 58,
    "CKE0": 60,
    "SCL": 141,
    "SDA": 285,
    "SA0": 139,
    "SA1": 140,
    "SA2": 238,
}

# Rail-to-rail isolation pairs to check
RAIL_ISOLATION_PAIRS = [
    ("VDD", "VPP"),
    ("VDD", "VDDSPD"),
    ("VDD", "VTT"),
    ("VDD", "VREF"),
    ("VDD", "GND"),
    ("VPP", "VDDSPD"),
    ("VPP", "GND"),
    ("VDDSPD", "GND"),
    ("VTT", "GND"),
    ("VREF", "GND"),
]


# ---------------------------------------------------------------------------
# CSV loading (same pattern as verify_pinmap.py)
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
# Probe point data structure
# ---------------------------------------------------------------------------

class ProbePoint:
    """A single measurement point in the probe sequence."""

    def __init__(
        self,
        session: str,
        group: str,
        pin: int,
        symbol: str,
        omi_net: str,
        measurement_type: str,
        expected_value: str,
        threshold_min: str,
        threshold_max: str,
        notes: str = "",
    ):
        self.session = session
        self.group = group
        self.pin = pin
        self.symbol = symbol
        self.omi_net = omi_net
        self.measurement_type = measurement_type
        self.expected_value = expected_value
        self.threshold_min = threshold_min
        self.threshold_max = threshold_max
        self.notes = notes

    def to_dict(self) -> dict:
        return {
            "session": self.session,
            "group": self.group,
            "pin": self.pin,
            "symbol": self.symbol,
            "omi_net": self.omi_net,
            "measurement_type": self.measurement_type,
            "expected_value": self.expected_value,
            "threshold_min": self.threshold_min,
            "threshold_max": self.threshold_max,
            "notes": self.notes,
        }


# ---------------------------------------------------------------------------
# Session 1: Continuity probes (unpowered)
# ---------------------------------------------------------------------------

def generate_continuity_probes(pins: list[dict]) -> list[ProbePoint]:
    """Generate Session 1 continuity probe points."""
    probes = []

    # Group 1A — GND continuity
    gnd_pins = [p for p in pins if p["omi_net"] == "GND"]
    for p in gnd_pins:
        probes.append(ProbePoint(
            session="S1_Continuity",
            group="1A_GND",
            pin=p["pin"],
            symbol=p["symbol"],
            omi_net=p["omi_net"],
            measurement_type="resistance",
            expected_value=f"<={GND_RESISTANCE_MAX_OHM} ohm",
            threshold_min="0",
            threshold_max=str(GND_RESISTANCE_MAX_OHM),
            notes="Measure resistance to chassis/reference GND",
        ))

    # Group 1B — Power rail continuity (non-GND power pins)
    power_nets = {}
    for p in pins:
        if p["group"] == "POWER" and p["omi_net"] != "GND":
            net = p["omi_net"]
            if net not in power_nets:
                power_nets[net] = []
            power_nets[net].append(p)

    for net, rail_pins in sorted(power_nets.items()):
        for p in rail_pins:
            probes.append(ProbePoint(
                session="S1_Continuity",
                group="1B_Power_Rail",
                pin=p["pin"],
                symbol=p["symbol"],
                omi_net=p["omi_net"],
                measurement_type="continuity",
                expected_value="PASS",
                threshold_min="",
                threshold_max="",
                notes=f"Verify continuity within {net} rail",
            ))

    # Group 1C — DQ/DQS signal continuity
    dq_pins = [p for p in pins if p["group"] == "DQ_DQS"]
    for p in dq_pins:
        lane = p["omi_net"].split("_")[0] if "_" in p["omi_net"] else ""
        probes.append(ProbePoint(
            session="S1_Continuity",
            group="1C_DQ_DQS",
            pin=p["pin"],
            symbol=p["symbol"],
            omi_net=p["omi_net"],
            measurement_type="continuity",
            expected_value="PASS",
            threshold_min="",
            threshold_max=str(SIGNAL_CONTINUITY_MAX_OHM),
            notes=f"Edge connector to DRAM pad ({lane})",
        ))

    # Group 1D — CA/CLK signal continuity (non-NC only)
    ca_pins = [p for p in pins if p["group"] == "CA_CLK" and p["omi_net"] != "NC"]
    for p in ca_pins:
        probes.append(ProbePoint(
            session="S1_Continuity",
            group="1D_CA_CLK",
            pin=p["pin"],
            symbol=p["symbol"],
            omi_net=p["omi_net"],
            measurement_type="continuity",
            expected_value="PASS",
            threshold_min="",
            threshold_max=str(SIGNAL_CONTINUITY_MAX_OHM),
            notes="Edge connector to bus/DRAM",
        ))

    # Group 1E — SPD bus continuity
    spd_pins = [p for p in pins if p["group"] == "SPD"]
    for p in spd_pins:
        probes.append(ProbePoint(
            session="S1_Continuity",
            group="1E_SPD",
            pin=p["pin"],
            symbol=p["symbol"],
            omi_net=p["omi_net"],
            measurement_type="continuity",
            expected_value="PASS",
            threshold_min="",
            threshold_max=str(SIGNAL_CONTINUITY_MAX_OHM),
            notes="Edge connector to SPD EEPROM",
        ))

    # Group 1F — NC pin isolation
    nc_pins = [p for p in pins if p["omi_net"] == "NC"]
    for p in nc_pins:
        probes.append(ProbePoint(
            session="S1_Continuity",
            group="1F_NC_Isolation",
            pin=p["pin"],
            symbol=p["symbol"],
            omi_net=p["omi_net"],
            measurement_type="isolation",
            expected_value=f">={NC_ISOLATION_MIN_OHM / 1e6:.0f} Mohm",
            threshold_min=str(NC_ISOLATION_MIN_OHM),
            threshold_max="",
            notes="Verify no short to adjacent pins",
        ))

    return probes


# ---------------------------------------------------------------------------
# Session 2: PDN probes (powered)
# ---------------------------------------------------------------------------

def generate_pdn_probes(pins: list[dict]) -> list[ProbePoint]:
    """Generate Session 2 PDN initialization probe points."""
    probes = []

    # Group 2A — Rail voltage measurements
    rail_specs = {
        "VDD": {
            "nominal": VDD_NOMINAL_V,
            "min": VDD_NOMINAL_V * (1 - VDD_TOLERANCE),
            "max": VDD_NOMINAL_V * (1 + VDD_TOLERANCE),
        },
        "VPP": {
            "nominal": VPP_NOMINAL_V,
            "min": VPP_NOMINAL_V * (1 - VPP_TOLERANCE),
            "max": VPP_NOMINAL_V * (1 + VPP_TOLERANCE),
        },
        "VDDSPD": {
            "nominal": 3.3,
            "min": VDDSPD_MIN_V,
            "max": VDDSPD_MAX_V,
        },
        "VTT": {
            "nominal": VDD_NOMINAL_V * VTT_NOMINAL_RATIO,
            "min": VDD_NOMINAL_V * VTT_NOMINAL_RATIO * 0.9,
            "max": VDD_NOMINAL_V * VTT_NOMINAL_RATIO * 1.1,
        },
        "VREF": {
            "nominal": VDD_NOMINAL_V * VREF_NOMINAL_RATIO,
            "min": VDD_NOMINAL_V * VREF_NOMINAL_RATIO * 0.9,
            "max": VDD_NOMINAL_V * VREF_NOMINAL_RATIO * 1.1,
        },
    }

    # Find one representative pin per rail for voltage measurement
    rail_representative_pins = {}
    for p in pins:
        if p["group"] == "POWER" and p["omi_net"] in rail_specs:
            net = p["omi_net"]
            if net not in rail_representative_pins:
                rail_representative_pins[net] = p

    for net, spec in rail_specs.items():
        if net in rail_representative_pins:
            p = rail_representative_pins[net]
            probes.append(ProbePoint(
                session="S2_PDN",
                group="2A_Rail_Voltage",
                pin=p["pin"],
                symbol=p["symbol"],
                omi_net=net,
                measurement_type="voltage",
                expected_value=f"{spec['nominal']:.2f} V",
                threshold_min=f"{spec['min']:.3f}",
                threshold_max=f"{spec['max']:.3f}",
                notes=f"Measure {net} rail voltage (powered, with host)",
            ))

    # Group 2B — Rail-to-rail isolation
    for rail_a, rail_b in RAIL_ISOLATION_PAIRS:
        pin_a = rail_representative_pins.get(rail_a)
        pin_b = rail_representative_pins.get(rail_b)
        if not pin_b and rail_b == "GND":
            gnd_pins = [p for p in pins if p["omi_net"] == "GND"]
            pin_b = gnd_pins[0] if gnd_pins else None
        if pin_a and pin_b:
            probes.append(ProbePoint(
                session="S2_PDN",
                group="2B_Rail_Isolation",
                pin=pin_a["pin"],
                symbol=f"{rail_a}(pin {pin_a['pin']}) <-> {rail_b}(pin {pin_b['pin']})",
                omi_net=f"{rail_a}_to_{rail_b}",
                measurement_type="resistance",
                expected_value=f">={RAIL_ISOLATION_MIN_OHM / 1e3:.0f} kohm",
                threshold_min=str(RAIL_ISOLATION_MIN_OHM),
                threshold_max="",
                notes=f"Cross-rail isolation (unpowered): {rail_a} to {rail_b}",
            ))

    # Group 2C — Power sequencing check points
    sequencing_checks = [
        ("VPP", "Must be established BEFORE VDD (JEDEC DDR4 requirement)"),
        ("VDD", "Apply after VPP is stable"),
        ("VDDSPD", "Required for SPD EEPROM — verify present"),
    ]
    for net, note in sequencing_checks:
        if net in rail_representative_pins:
            p = rail_representative_pins[net]
            probes.append(ProbePoint(
                session="S2_PDN",
                group="2C_Power_Sequencing",
                pin=p["pin"],
                symbol=p["symbol"],
                omi_net=net,
                measurement_type="sequencing",
                expected_value="See notes",
                threshold_min="",
                threshold_max="",
                notes=note,
            ))

    return probes


# ---------------------------------------------------------------------------
# Session 3: SPD bus probes (powered)
# ---------------------------------------------------------------------------

def generate_spd_probes(pins: list[dict]) -> list[ProbePoint]:
    """Generate Session 3 SPD bus analysis probe points."""
    probes = []

    # Key SPD bus pins
    spd_bus_pins = {
        "SCL": {"expected_pin": 141, "desc": "I2C clock line"},
        "SDA": {"expected_pin": 285, "desc": "I2C data line"},
        "VDDSPD": {"expected_pin": 284, "desc": "SPD EEPROM supply"},
        "SA0": {"expected_pin": 139, "desc": "Address bit 0"},
        "SA1": {"expected_pin": 140, "desc": "Address bit 1"},
        "SA2": {"expected_pin": 238, "desc": "Address bit 2"},
    }

    # Build lookup from omi_net -> pin record
    pin_by_net = {}
    for p in pins:
        net = p["omi_net"]
        if net.startswith("SPD_"):
            pin_by_net[net.replace("SPD_", "")] = p
        elif net in spd_bus_pins:
            pin_by_net[net] = p

    # Group 3A — SPD supply verification
    vddspd_pins = [p for p in pins if p["omi_net"] == "VDDSPD"]
    for p in vddspd_pins:
        probes.append(ProbePoint(
            session="S3_SPD_Bus",
            group="3A_SPD_Supply",
            pin=p["pin"],
            symbol=p["symbol"],
            omi_net="VDDSPD",
            measurement_type="voltage",
            expected_value=f"{VDDSPD_MIN_V}-{VDDSPD_MAX_V} V",
            threshold_min=str(VDDSPD_MIN_V),
            threshold_max=str(VDDSPD_MAX_V),
            notes="SPD EEPROM supply must be present before I2C read",
        ))

    # Group 3B — I2C bus signal integrity
    scl_pins = [p for p in pins if p["omi_net"] == "SPD_SCL"]
    for p in scl_pins:
        probes.append(ProbePoint(
            session="S3_SPD_Bus",
            group="3B_I2C_Bus",
            pin=p["pin"],
            symbol=p["symbol"],
            omi_net="SPD_SCL",
            measurement_type="waveform",
            expected_value="Open-drain with pull-up",
            threshold_min="",
            threshold_max="",
            notes="Scope: verify pull-up waveform, not floating. "
                  "Rise time should be consistent with I2C spec.",
        ))

    sda_pins = [p for p in pins if p["omi_net"] == "SPD_SDA"]
    for p in sda_pins:
        probes.append(ProbePoint(
            session="S3_SPD_Bus",
            group="3B_I2C_Bus",
            pin=p["pin"],
            symbol=p["symbol"],
            omi_net="SPD_SDA",
            measurement_type="waveform",
            expected_value="Open-drain with pull-up; ACK/NACK visible",
            threshold_min="",
            threshold_max="",
            notes="Scope/logic analyzer: verify data transitions "
                  "and ACK from EEPROM at address 0x50.",
        ))

    # Group 3C — Address pin verification
    sa_pins = [p for p in pins if p["omi_net"] in ("SA0", "SA1", "SA2")]
    for p in sa_pins:
        probes.append(ProbePoint(
            session="S3_SPD_Bus",
            group="3C_Address",
            pin=p["pin"],
            symbol=p["symbol"],
            omi_net=p["omi_net"],
            measurement_type="voltage",
            expected_value="Logic LOW (tied to GND) or HIGH per design",
            threshold_min="",
            threshold_max="",
            notes=f"SA pin determines EEPROM I2C address. "
                  f"Default 0x50 when SA0=SA1=SA2=0.",
        ))

    # Group 3D — SPD read verification
    probes.append(ProbePoint(
        session="S3_SPD_Bus",
        group="3D_SPD_Read",
        pin=141,
        symbol="SCL",
        omi_net="SPD_SCL",
        measurement_type="protocol",
        expected_value="EEPROM responds with non-0xFF/non-0x00 data",
        threshold_min="",
        threshold_max="",
        notes="Perform I2C read at address 0x50. Verify byte 2 "
              "(SPD revision) is a valid value. All-0xFF or all-0x00 "
              "indicates blank/missing EEPROM.",
    ))

    return probes


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------

PROBE_CSV_COLUMNS = [
    "session", "group", "pin", "symbol", "omi_net",
    "measurement_type", "expected_value",
    "threshold_min", "threshold_max", "notes",
]


def export_probe_csv(probes: list[ProbePoint], path: Path):
    """Write probe sequence to CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=PROBE_CSV_COLUMNS)
        writer.writeheader()
        for p in probes:
            writer.writerow(p.to_dict())


def export_probe_markdown(probes: list[ProbePoint], path: Path):
    """Write probe sequence as a printable markdown checklist."""
    path.parent.mkdir(parents=True, exist_ok=True)

    # Group probes by session, then by group
    sessions = {}
    for p in probes:
        if p.session not in sessions:
            sessions[p.session] = {}
        if p.group not in sessions[p.session]:
            sessions[p.session][p.group] = []
        sessions[p.session][p.group].append(p)

    session_titles = {
        "S1_Continuity": "Session 1 — Continuity Audit (Unpowered)",
        "S2_PDN": "Session 2 — PDN Initialization (Powered)",
        "S3_SPD_Bus": "Session 3 — SPD Bus Analysis (Powered)",
    }

    with open(path, "w", encoding="utf-8") as f:
        f.write("# OMI L1 Bench Electrical — Probe Sequence Checklist\n\n")
        f.write(f"*Generated: {datetime.now(timezone.utc).isoformat()}*\n\n")
        f.write("---\n\n")

        for session_key in sorted(sessions.keys()):
            title = session_titles.get(session_key, session_key)
            f.write(f"## {title}\n\n")

            for group_key in sorted(sessions[session_key].keys()):
                group_probes = sessions[session_key][group_key]
                # Format group name
                group_name = group_key.replace("_", " ").split(" ", 1)
                group_label = group_name[1] if len(group_name) > 1 else group_key
                f.write(f"### {group_key}: {group_label}\n\n")
                f.write("| Pin | Symbol | Net | Type | Expected | Notes |\n")
                f.write("|-----|--------|-----|------|----------|-------|\n")

                for p in group_probes:
                    f.write(
                        f"| {p.pin} | {p.symbol} | {p.omi_net} "
                        f"| {p.measurement_type} | {p.expected_value} "
                        f"| {p.notes} |\n"
                    )

                f.write("\n")

            f.write("---\n\n")

        f.write("*Generated by generate_probe_sequence.py v1.0.0*\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="OMI L1 — Probe Sequence Generator"
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
        help="Output file path (default: stdout summary only)",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "markdown"],
        default="csv",
        help="Output format: csv (default) or markdown",
    )
    args = parser.parse_args()

    # Validate inputs
    if not args.reference.exists():
        print(f"ERROR: Reference CSV not found: {args.reference}", file=sys.stderr)
        sys.exit(2)

    # Load pin map
    try:
        pins = load_pinmap_csv(args.reference)
    except (ValueError, csv.Error) as e:
        print(f"ERROR: Failed to parse CSV: {e}", file=sys.stderr)
        sys.exit(2)

    csv_hash = compute_sha256(args.reference)

    # Generate all probe points
    probes = []
    probes.extend(generate_continuity_probes(pins))
    probes.extend(generate_pdn_probes(pins))
    probes.extend(generate_spd_probes(pins))

    # Summary
    sessions = {}
    for p in probes:
        sessions[p.session] = sessions.get(p.session, 0) + 1

    print("=" * 70)
    print("  OMI L1 — Probe Sequence Generator")
    print("=" * 70)
    print()
    print(f"  Reference CSV:   {args.reference}")
    print(f"  CSV SHA-256:     {csv_hash}")
    print(f"  Total probes:    {len(probes)}")
    print()
    for session, count in sorted(sessions.items()):
        print(f"    {session}: {count} probe points")
    print()

    # Export
    if args.output:
        if args.format == "markdown":
            export_probe_markdown(probes, args.output)
        else:
            export_probe_csv(probes, args.output)
        print(f"  Output written to: {args.output}")
    else:
        print("  (No --output specified; use --output to save probe sequence)")

    print()
    print("=" * 70)
    sys.exit(0)


if __name__ == "__main__":
    main()
