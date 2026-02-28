# Stage 8.2 — Bring-Up Ladder (OMI v1)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
Draft

## Purpose
Convert the Stage 8 validation layers into a concrete, stepwise bring-up ladder.
Each level has a definition, pass/fail criteria, required artifacts, and stop conditions.

> **Rule:** Do not proceed to the next level until the current level is fully passed and artifacts are committed.

---

## L0 — Artifact Integrity (Pre-Hardware Gate)

### Definition
All design artifacts are internally consistent, complete, and reviewable before any hardware is touched.

### Pass Criteria
- [ ] `ddr4_udimm_288_pinmap.csv` — 288 rows, 288 unique pins, 0 missing, 0 duplicates
- [ ] Net manifest net names match schematic net labels exactly (no silent aliases)
- [ ] All tie-off decisions are explicit (`NC`, `NF`, `single-rank v1: unused`, etc.)
- [ ] No undocumented assumptions exist in any Stage 7 artifact

### Fail Criteria
- Any pin number missing or duplicated in CSV
- Net name in schematic that does not appear in the manifest
- Any "TBD" or placeholder in a frozen artifact

### Required Artifacts
- CSV integrity check output (row count, unique count, missing list)
- Completed Stage 7.5 / Stage 7.6 checklists

### Stop Condition
**Halt and open issue** if any fail criterion is met.
Do not proceed to L1 until L0 is fully green.

---

## L1 — Bench Electrical (Continuity + Rails)

### Definition
The physical module is inserted into a passive fixture (Class C) or scope-equipped jig. Continuity and power rail isolation are verified before any active host is used.

### Pass Criteria
- [ ] All 288 edge contacts show continuity to their mapped net (no open circuits)
- [ ] No shorts between adjacent pins (≥ 1 MΩ between non-connected nets)
- [ ] VDD, VDDQ, VPP, VREF, VTT, VDDSPD rails are isolated from each other
- [ ] GND contact resistance is ≤ 1 Ω across all VSS pins

### Fail Criteria
- Any open circuit on a functional signal net (DQ, DQS, DM, CA, CLK, control)
- Any short between two distinct signal nets
- Rail-to-rail resistance < 10 kΩ on rails that must be isolated

### Required Artifacts
- Continuity test log (pin-by-pin or net-group-by-group) — table or photo set
- DVM / oscilloscope screenshots for each rail showing isolation
- Platform: jig model, probe/DVM model, date

### Stop Condition
**Halt and open issue** if any short or open is detected on a functional net.
Document exact pin numbers and measured values.
Do not proceed to L2 until L1 is fully passed.

---

## L2 — Host Enumeration (SPD Read)

### Definition
The module is inserted into a Class A or Class B platform. The host reads the SPD EEPROM over SMBus. The result is compared against the expected SPD contents.

### Pass Criteria
- [ ] SPD read completes without errors (no SMBus timeout or NACK)
- [ ] EEPROM returns expected byte count (256 bytes for DDR4 SPD)
- [ ] Key SPD fields match expectations: module type, DRAM type, capacity, speed grade, manufacturer
- [ ] BIOS/host reports module as a valid DDR4 UDIMM

### Fail Criteria
- SMBus read fails or times out
- SPD bytes return all-zeros or all-0xFF (missing EEPROM or no pull-up)
- Module not recognized by host (no BIOS POST entry for this DIMM)

### Required Artifacts
- Raw SPD dump (hex bytes, 256 bytes, labeled by offset)
- BIOS POST screenshot or log showing module detection
- Platform: board model, BIOS version, slot used, OS or BIOS version string

### Stop Condition
**Halt and open issue** if SPD read fails.
Probable causes: VDDSPD missing, SA0–SA2 address incorrect, SDA/SCL open, missing host pull-up.
Label the issue with `L2-FAIL` and the symptom.

---

## L3 — Training + Boot

### Definition
The host trains against the module and the OS boots. Memory training completes without fatal errors. The OS reports the correct capacity and type.

### Pass Criteria
- [ ] BIOS memory training completes without error (no beep codes, no reboot loops)
- [ ] BIOS reports: correct capacity, DDR4, correct speed (at least rated XMP or JEDEC base)
- [ ] OS boots successfully and memory is fully accessible
- [ ] OS reports correct total RAM (within small rounding margin)
- [ ] No uncorrectable memory errors in OS logs at boot

### Fail Criteria
- Training loop (system reboots repeatedly during POST)
- BIOS halts with memory-related error code
- OS reports less than expected capacity (lane failures)
- Uncorrectable ECC/parity errors on a non-ECC module (indicates real data errors)

### Required Artifacts
- BIOS POST photo or log (training result, capacity shown)
- OS memory report screenshot (`dmidecode`, Windows Task Manager, or equivalent)
- Platform: board model, BIOS version, OS version, DDR speed trained at

### Stop Condition
**Halt and open issue** if training fails or capacity is wrong.
Probable causes: DQ lane open, DQS phase error, VDD/VDDQ marginal, RESET_n or CKE issue.
Label with `L3-FAIL` and symptom.

---

## L4 — Stress + Soak

### Definition
The module runs under sustained memory stress. No memory errors occur within the defined soak period.

### Pass Criteria
- [ ] `memtest86+` (or equivalent) passes ≥ 2 full passes with 0 errors
- [ ] OS-level memory benchmark completes without errors (e.g., `stress-ng --vm`, Windows Memory Diagnostic)
- [ ] System remains stable for ≥ 1 hour under sustained memory load
- [ ] No correctable or uncorrectable errors reported in OS ECC/event logs

### Fail Criteria
- Any single-bit error reported by memtest
- System crash or hang during stress
- Repeated correctable errors (indicates marginal signal integrity)

### Required Artifacts
- memtest86+ result screenshot (showing 0 errors, pass count, full capacity tested)
- Stress tool log with pass/fail summary
- Platform: board model, BIOS version, OS, tool version, ambient temperature
- Total soak duration and memory speed trained at

### Stop Condition
**Halt and open issue** if any error is detected.
Do not waive errors — a single bit error is a real failure.
Label with `L4-FAIL` and include error address, type, and test pass number.

---

## Summary Table

| Level | Gate type | Minimum platform | Key artifact |
|-------|-----------|-----------------|-------------|
| L0 | Pre-hardware | None | CSV integrity output + Stage 7 checklists |
| L1 | Physical | Class C jig | Continuity log + rail isolation measurements |
| L2 | Enumeration | Class A or B | SPD dump + BIOS POST screenshot |
| L3 | Functional | Class A | BIOS training log + OS memory report |
| L4 | Reliability | Class A | memtest86+ result + soak log |

---

*Next: `08-3_failure_modes.md` — failure mode reference and debug hooks.*
