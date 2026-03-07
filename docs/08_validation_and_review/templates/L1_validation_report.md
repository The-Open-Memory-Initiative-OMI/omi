# OMI Stage 8 Validation: L1 Bench Electrical Report

**Run ID:** `RUN-YYYYMMDD-PLATFORM-L1-001`
**Executing Engineer:** [GitHub Handle / Name]
**Date:** YYYY-MM-DD
**Target Commit Hash:** [insert git SHA]

---

## 1. Executive Summary

This report presents the evidence required to fulfill Level 1 (L1) validation
for the OMI v1 target (DDR4 UDIMM, 8 GB, 1R, x8, Non-ECC).

All continuity, power rail isolation, and SPD bus integrity checks have been
executed against a manufactured prototype module and are documented below.

---

## 2. Environment

| Field | Value |
|-------|-------|
| Git commit SHA | `[insert]` |
| Test jig / socket model | [insert] |
| DMM model + serial | [insert] |
| Oscilloscope model | [insert] |
| Logic analyzer model | [insert, or N/A] |
| Bench power supply model | [insert] |
| Python version | [insert] |
| OS | [insert] |
| Script versions | generate_probe_sequence.py v1.0.0, validate_continuity_log.py v1.0.0 |
| Ambient temperature | [insert] °C |

---

## 3. Module Under Test

| Field | Value |
|-------|-------|
| OMI module version | OMI v1 DDR4 UDIMM |
| PCB revision | [insert] |
| BOM variant | [insert] |
| Module serial / ID | [insert] |
| Notes | [insert] |

---

## 4. Check Results & Evidence

| Check Category | Criteria | Status | Evidence File |
|----------------|----------|--------|---------------|
| **GND Resistance** | All VSS pins ≤1 Ω | PASS / FAIL | `evidence/continuity_report.json` |
| **Signal Continuity** | All DQ/DQS, CA/CLK, SPD pins connected | PASS / FAIL | `evidence/continuity_report.json` |
| **NC Pin Isolation** | All NC pins ≥1 MΩ to neighbors | PASS / FAIL | `evidence/continuity_report.json` |
| **Power Rail Continuity** | Pin-to-pin within each rail | PASS / FAIL | `evidence/continuity_report.json` |
| **Rail-to-Rail Isolation** | ≥10 kΩ between isolated rails | PASS / FAIL | `evidence/continuity_report.json` |
| **Rail Voltage** | VDD=1.2V±5%, VPP=2.5V±5%, VDDSPD=2.2-3.6V | PASS / FAIL | `evidence/continuity_report.json` |
| **SPD Bus Integrity** | SCL/SDA/SA/VDDSPD connected to EEPROM | PASS / FAIL | `evidence/continuity_report.json` |

**Overall L1 Status:** PASS / FAIL

---

## 5. Deviations & Documented Waivers

> List any measurement anomalies or waivers applied during L1 testing.
> Each waiver must include an engineering justification.

- **Waiver 1:** [Signal/Net name] — [Description]
  - **Justification:** [Why this is acceptable for DDR4 1R x8 architecture]

- *(Add additional waivers as needed, or write "None" if no waivers applied)*

---

## 6. Evidence Package

### Automated Script Outputs

| File | Description | SHA-256 |
|------|-------------|---------|
| `probe_sequence.csv` | Generated probe sequence (313 points) | `[hash]` |
| `probe_checklist.md` | Printable probe checklist | `[hash]` |
| `continuity_report.json` | Validation results | `[hash]` |
| `l1_summary.json` | Unified L1 summary | `[hash]` |

### Manual Evidence (Measurements)

| File | Description | SHA-256 |
|------|-------------|---------|
| `measurement_log.csv` | Tester's measurement log (all 288 pins) | `[hash]` |
| `scope_vdd_*.png` | VDD rail voltage screenshot | `[hash]` |
| `scope_vpp_*.png` | VPP rail voltage screenshot | `[hash]` |
| `scope_vddspd_*.png` | VDDSPD rail voltage screenshot | `[hash]` |
| `scope_i2c_*.png` | SCL/SDA waveform capture | `[hash]` |

---

## 7. Reproduction Instructions

```bash
# Clone and checkout the exact commit
git clone https://github.com/The-Open-Memory-Initiative-OMI/omi.git
git checkout [commit-hash]

# Run L1 validation suite
python docs/08_validation_and_review/scripts/l1_runner.py \
  --reference design/connector/ddr4_udimm_288_pinmap.csv \
  --measurements path/to/measurement_log.csv \
  --output-dir validation/evidence
```

---

## 8. Sign-Off

| Field | Value |
|-------|-------|
| Reported by | [Name / Handle] |
| Date | YYYY-MM-DD |
| Run ID | `RUN-YYYYMMDD-PLATFORM-L1-001` |
| Result | PASS / FAIL |
| Linked PR / Issue | [link] |
