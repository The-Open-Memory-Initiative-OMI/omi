# L1 — Bench Electrical

## Purpose

L1 is the first physical validation level in the OMI Validation Ladder.
It proves that the manufactured module has correct electrical connectivity
before any active host platform is used.

L1 validates three domains:

1. **Continuity** — all 288 edge connector pins reach their mapped nets
2. **Power Rail Isolation** — VDD, VPP, VREF, VDDSPD, VTT are isolated
3. **SPD Bus Integrity** — I2C bus can reach the SPD EEPROM

## Prerequisites

- **L0 must be PASSED** before starting L1.
- **Hardware:** manufactured OMI v1 DDR4 UDIMM prototype board.
- **Equipment:** DMM with continuity mode, bench power supply, oscilloscope
  or logic analyzer, DDR4 UDIMM test socket (Class C jig).
- **Software:** Python 3.8+ (for running validation scripts).

## Quick Start

```bash
# From the repository root:

# 1. Generate the probe sequence (what to measure and where)
python docs/08_validation_and_review/scripts/generate_probe_sequence.py \
  --reference design/connector/ddr4_udimm_288_pinmap.csv \
  --output validation/evidence/probe_sequence.csv

# 2. Generate a printable checklist for the bench
python docs/08_validation_and_review/scripts/generate_probe_sequence.py \
  --reference design/connector/ddr4_udimm_288_pinmap.csv \
  --format markdown \
  --output validation/evidence/probe_checklist.md

# 3. After completing measurements, validate your log
python docs/08_validation_and_review/scripts/validate_continuity_log.py \
  --reference design/connector/ddr4_udimm_288_pinmap.csv \
  --measurements path/to/your_measurement_log.csv

# 4. Run the full L1 suite with evidence generation
python docs/08_validation_and_review/scripts/l1_runner.py \
  --reference design/connector/ddr4_udimm_288_pinmap.csv \
  --measurements path/to/your_measurement_log.csv \
  --output-dir validation/evidence
```

## Directory Contents

| File | Purpose |
|------|---------|
| `measurement_procedures.md` | Step-by-step bench procedures for all 3 sessions |
| `measurement_log_template.csv` | Blank CSV template for recording measurements |
| `probe_sequence_reference.csv` | Pre-generated probe sequence for reference |

## Related Files

| File | Location |
|------|----------|
| L1 scripts | `docs/08_validation_and_review/scripts/` |
| Report templates | `docs/08_validation_and_review/templates/` |
| Canonical pin map CSV | `design/connector/ddr4_udimm_288_pinmap.csv` |
| Bringup ladder | `docs/08_validation_and_review/08-2_bringup_ladder.md` |
| Failure signatures | `docs/08_validation_and_review/08-5_failure_signatures.md` |

## L1 Pass/Fail Criteria

(From `08-2_bringup_ladder.md`)

### Pass
- All 288 edge contacts show continuity to their mapped net
- No shorts between adjacent pins (≥1 MΩ between non-connected nets)
- VDD, VDDQ, VPP, VREF, VTT, VDDSPD rails are isolated from each other
- GND contact resistance ≤1 Ω across all VSS pins

### Fail
- Any open circuit on a functional signal net (DQ, DQS, DM, CA, CLK, control)
- Any short between two distinct signal nets
- Rail-to-rail resistance <10 kΩ on rails that must be isolated

### Stop Condition
**Halt and open issue** if any short or open is detected on a functional net.
Document exact pin numbers and measured values.
Do not proceed to L2 until L1 is fully passed.
