# Stage 8.04 — Success Criteria & Failure Modes (OMI v1)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
Draft

## Purpose
Consolidate pass/fail definitions across all validation levels into a single reference, extend the existing failure signature catalog with diagnostic decision trees, and document honest unknowns that cannot be resolved until hardware exists.

---

## Relationship to Existing Documents

This document **consolidates and extends** three existing references:

- [08-2_bringup_ladder.md](./08-2_bringup_ladder.md) — Authoritative pass/fail criteria per level (L0–L4). This document summarizes but does not replace those definitions.
- [08-3_test_matrix.md](./08-3_test_matrix.md) — Test categories (T1–T7), durations, and failure taxonomy (deterministic/intermittent/environment).
- [08-5_failure_signatures.md](./08-5_failure_signatures.md) — Six failure signatures (FS-01 through FS-06) with symptom-to-cause mappings.

**What this document adds:**
1. A consolidated success criteria summary table for quick reference
2. A failure mode catalog organized by validation level (not by signature number)
3. Diagnostic decision trees for each level
4. A failure reporting template
5. An honest unknowns register

---

## 1. Consolidated Success Criteria

This table provides a quick-reference summary. For full pass/fail criteria and required artifacts, see [08-2_bringup_ladder.md](./08-2_bringup_ladder.md).

| Level | Gate | One-Line Success Criterion | Key Evidence | Ref |
|-------|------|---------------------------|-------------|-----|
| **L0** | Artifact Integrity | All 288 pins mapped, net names consistent, no TBDs in frozen artifacts | CSV integrity output, naming audit log | [08-2 §L0](./08-2_bringup_ladder.md) |
| **L1** | Bench Electrical | All functional nets have continuity, all power rails isolated, no shorts | Continuity log, rail isolation measurements | [08-2 §L1](./08-2_bringup_ladder.md) |
| **L2** | Host Enumeration | SPD EEPROM readable, returns correct DDR4 configuration, host recognizes module | Raw SPD hex dump, BIOS POST screenshot | [08-2 §L2](./08-2_bringup_ladder.md) |
| **L3** | Training + Boot | Host trains at DDR4-2400, OS boots, correct capacity reported, short memtest passes | BIOS training log, OS memory report, memtest screenshot | [08-2 §L3](./08-2_bringup_ladder.md) |
| **L4** | Stress + Soak | Zero errors in extended memtest (≥2 passes), stable under sustained load for ≥1 hour | memtest86+ result, stress log, thermal data | [08-2 §L4](./08-2_bringup_ladder.md) |

### What "PASS" means at each level

- **L0 PASS:** Automated scripts (`verify_pinmap.py`, `verify_naming.py`) return zero errors. Peer review checklist completed with no unresolved findings.
- **L1 PASS:** All 288 pins probed per [measurement_procedures.md](./L1_bench_electrical/measurement_procedures.md). Zero opens on functional nets, zero shorts between distinct nets, all rails isolated.
- **L2 PASS:** SPD read completes on at least one Class A platform. Key SPD fields match expected values: DDR4, 8 GB, 1Rx8, DDR4-2400, non-ECC.
- **L3 PASS:** Training completes, OS boots, `dmidecode` reports correct capacity, memtest runs ≥10 minutes with zero errors.
- **L4 PASS:** memtest86+ runs ≥2 full passes with zero errors. System stable under memory stress for ≥1 hour. No thermal anomalies.

### What "FAIL" means

A failure at any level is a **hard stop**. Do not proceed to the next level. A failure is also a **valid engineering result** — it narrows the problem space and informs the design. Failures must be documented with the same rigor as passes.

---

## 2. Expected Failure Mode Catalog

This catalog organizes failure modes by the validation level where they are most likely to surface. For detailed symptom-to-cause mappings, see [08-5_failure_signatures.md](./08-5_failure_signatures.md).

### L1 Failures — Bench Electrical

| Failure Mode | Symptoms | Likely Root Cause | Diagnostic Steps | Severity |
|-------------|----------|-------------------|-----------------|----------|
| Power rail short (VDD-to-GND) | DVM reads < 1 Ω between VDD and GND | Solder bridge on DRAM power pins; shorted decoupling capacitor | Visual inspection under magnification; isolate by removing components | **Critical** — do not power on |
| Power rail cross-contamination | DVM reads < 10 kΩ between VDD and VPP (or other rail pair) | PCB manufacturing defect; solder bridge between adjacent power vias | Measure all rail pairs per [measurement_procedures.md](./L1_bench_electrical/measurement_procedures.md) Session 2 | **Critical** — do not power on |
| Open circuit on functional net | DVM shows no continuity from edge pin to DRAM pad | Missing solder joint; PCB trace break; component not placed | Probe at intermediate points along the trace to localize the break | **Critical** — L1 blocker |
| I²C bus pull-up missing | SDA/SCL measure 0V or float (no pull-up to VDDSPD) | Pull-ups are host-side in OMI v1; check if host provides pull-ups. If testing with Class C jig, external pull-ups are required | Measure resistance from SDA (pin 285) to VDDSPD (pin 284); expect 2.2–4.7 kΩ if pull-up present | **High** — L2 will fail |

### L1/L2 Failures — SPD

| Failure Mode | Symptoms | Likely Root Cause | Diagnostic Steps | Severity |
|-------------|----------|-------------------|-----------------|----------|
| SPD EEPROM not responding | `i2cdetect` shows no device at 0x50; BIOS skips DIMM slot | See [FS-01](./08-5_failure_signatures.md) — VDDSPD missing, SA address wrong, SDA/SCL open, pull-ups missing, EEPROM blank | Follow FS-01 diagnostic sequence: probe VDDSPD → check SA pins → check SDA/SCL continuity | **Critical** — L2 blocker |
| SPD returns garbage data | SPD bytes are all-0x00 or all-0xFF; or random-looking data | EEPROM not programmed (blank chip); SDA noise; I²C bus contention from other devices | Dump raw 256 bytes; check if pattern is uniform (blank) or random (noise); scope SDA waveform | **Critical** — L2 blocker |
| SPD reports incorrect configuration | SPD reads successfully but reports wrong capacity, speed, or type | SPD content programming error; wrong hex image burned to EEPROM | Compare SPD bytes against expected values per JEDEC DDR4 SPD spec (JESD21C); reprogram if wrong | **High** — L3 will fail |

### L3 Failures — Training and Boot

| Failure Mode | Symptoms | Likely Root Cause | Diagnostic Steps | Severity |
|-------------|----------|-------------------|-----------------|----------|
| Host refuses to train module | Boot loop; BIOS error code; system hangs during POST | See [FS-02](./08-5_failure_signatures.md) — VDD/VDDQ marginal, RESET_n stuck, CKE not asserting, CK absent, CS0_n not asserted | Follow FS-02 sequence: probe VDD → RESET_n → CKE0 → CK_t/CK_c → CS0_n | **Critical** — L3 blocker |
| Training succeeds but wrong capacity | BIOS reports 4 GB instead of 8 GB | See [FS-03](./08-5_failure_signatures.md) — DQ lane open, address bit open, SPD capacity field wrong | Identify which half of memory is missing; check corresponding DQ lanes or address bits | **Critical** — L3 blocker |
| SPD OK but training fails | BIOS reads SPD correctly, then fails during training | See [FS-06](./08-5_failure_signatures.md) — SPD timing bytes incorrect, CK marginal, platform doesn't support programmed speed, VREF marginal | Force DDR4-2133 in BIOS; if training passes, SPD speed profile needs adjustment | **Critical** — L3 blocker |
| Module works on one platform but not another | Trains on Intel, fails on AMD (or vice versa) | Different memory controller training algorithms; different impedance calibration ranges; different timing tolerance | **This is not necessarily an OMI design flaw.** Document both results with full platform details. Compare SPD timing values against both vendors' supported ranges. | **High** — investigate, do not assume OMI fault |

### L3/L4 Failures — Data Integrity

| Failure Mode | Symptoms | Likely Root Cause | Diagnostic Steps | Severity |
|-------------|----------|-------------------|-----------------|----------|
| Deterministic bit errors (same address every run) | memtest reports stuck bit at fixed address | See [FS-04](./08-5_failure_signatures.md) — DQ pin open/shorted, DQS not reaching DRAM, DM pin fault, per-device VDD marginal | Identify failing lane: `lane = error_bit // 8`; check continuity on that DQ pin | **Critical** — L4 blocker |
| Intermittent bit errors under stress | Errors appear after extended soak; may be thermally correlated | See [FS-05](./08-5_failure_signatures.md) — marginal solder joint, VDD droop under load, SI marginal at temperature | Record error onset time and temperature; scope VDD ripple under load; test with active cooling | **High** — do not waive |
| Thermal issues under sustained load | DRAM device temperature exceeds 85°C (DDR4 max operating); errors increase with temperature | Insufficient airflow; excessive power dissipation; PCB thermal design issue | Measure DRAM case temperature with IR thermometer; add active cooling; retest | **High** — L4 blocker |

---

## 3. Diagnostic Decision Trees

These text-based decision trees guide first-response diagnostics. They complement (not replace) the detailed tables in [08-5_failure_signatures.md](./08-5_failure_signatures.md).

### L1 Decision Tree: Module fails continuity checks

```
START: Continuity check fails on one or more nets
  │
  ├─ Is the failure on a POWER net (VDD, VDDQ, VPP, GND)?
  │   ├─ YES → Is it a SHORT (< 1 Ω between distinct rails)?
  │   │         ├─ YES → DO NOT POWER ON. Visual inspection for solder bridges.
  │   │         │         Remove decoupling caps one at a time to isolate.
  │   │         └─ NO → Is it an OPEN (no continuity to DRAM)?
  │   │                   └─ Check intermediate via/trace points. Likely PCB defect.
  │   └─ NO → Is the failure on a DQ/DQS net?
  │             ├─ YES → Check specific DRAM device solder joints.
  │             │         This will cause partial capacity at L3 (FS-03).
  │             └─ NO → Is it a CA/CLK net?
  │                       └─ Check DRAM-side solder; this will cause training failure at L3 (FS-02).
```

### L2 Decision Tree: SPD read fails

```
START: Host does not detect module on I²C bus
  │
  ├─ Probe VDDSPD (pin 284): Is voltage 2.2–3.6V?
  │   ├─ NO → Host is not supplying VDDSPD. Check host board SPD power.
  │   │         If using Class C jig, provide external 3.3V to VDDSPD.
  │   └─ YES → Probe SDA (pin 285) and SCL (pin 141): Are pull-ups present?
  │               ├─ NO → Pull-ups are host-side. Verify host provides them.
  │               │         If Class C jig, add 4.7 kΩ pull-ups to VDDSPD.
  │               └─ YES → Check SA0 (pin 139), SA1 (pin 140), SA2 (pin 238):
  │                          What address are they selecting?
  │                          ├─ Wrong address → Fix SA strap resistors.
  │                          └─ Correct address (0x50) → Check EEPROM orientation.
  │                                                       Probe EEPROM VCC, GND, WP.
  │                                                       If all OK → EEPROM may be defective or blank.
```

### L3 Decision Tree: Training fails

```
START: BIOS enters boot loop or shows memory error
  │
  ├─ Did L2 pass (SPD read OK)?
  │   ├─ NO → Go back to L2 decision tree. Do not skip levels.
  │   └─ YES → Probe VDD (pin 64) and VDDQ: Are voltages correct under load?
  │               ├─ NO → Power delivery issue. Check host VRM and decoupling.
  │               └─ YES → Probe CK_t (pin 74) / CK_c (pin 75): Is clock present?
  │                          ├─ NO → Clock not reaching module. Check host clock driver.
  │                          └─ YES → Probe RESET_n (pin 58): Does it deassert (go HIGH)?
  │                                     ├─ NO → RESET stuck low. Check RESET trace continuity.
  │                                     └─ YES → Force DDR4-2133 in BIOS:
  │                                                ├─ Training passes → SPD speed profile issue (FS-06)
  │                                                └─ Training still fails → Check CS0_n (pin 84),
  │                                                    CKE0 (pin 60); if both active, suspect
  │                                                    DQ lane issue → probe D0_DQ0 (pin 5)
```

---

## 4. Failure Reporting Template

Use this template for every failure encountered during OMI v1 validation. Submit as a markdown file in the validation run directory and open a corresponding GitHub issue.

```markdown
## Failure Report: [SHORT DESCRIPTIVE TITLE]

**Run ID:** [Per 08-4_reporting_template.md scheme]
**Date:** [YYYY-MM-DD]
**Platform:** [Platform ID from platform documentation template]
**Validation Level:** L1 / L2 / L3 / L4
**Failure Category:** DETERMINISTIC / INTERMITTENT / ENVIRONMENT
  (per 08-3_test_matrix.md §3 taxonomy)

### Symptom
[Exact observed behavior. Be specific: "BIOS shows error code 55 and reboots"
not "training failed".]

### Environment
| Field | Value |
|-------|-------|
| BIOS version | |
| OS version | |
| Ambient temperature | |
| Other DIMMs present | |
| BIOS memory settings | |

### Evidence
- [ ] Photo/screenshot: [filename]
- [ ] Measurement log: [filename]
- [ ] Scope capture: [filename]
- [ ] SPD dump: [filename]
[All evidence stored in validation/results/<RunID>/]

### Hypotheses (ranked by likelihood)
1. [Most likely cause — with reasoning]
2. [Second most likely — with reasoning]
3. [Third most likely — with reasoning]

### Diagnostic Steps Taken
1. [What you measured/checked]
2. [Result of that measurement]
3. [Next measurement based on result]

### Resolution
[If known: what fixed the issue. If unknown: state "Unresolved — further
investigation required" and list the next diagnostic steps to try.]

### GitHub Issue
[Link to opened issue, or "Pending — will open after peer review"]
```

---

## 5. Honest Unknowns

These are things the OMI project does not know and **cannot know** until fabricated hardware exists and is tested. They are not failures of planning — they are engineering realities that must be acknowledged honestly.

| Unknown | Why We Don't Know Yet | What Evidence Resolves It | At Which Level |
|---------|----------------------|--------------------------|---------------|
| **Actual VDD/VDDQ current draw under training** | No hardware to measure; DRAM datasheet gives typical/max but actual depends on PCB and host | Measure supply current at test points during L3 training; compare against datasheet IDD values | L3 |
| **Signal integrity eye quality at DDR4-2400** | No SI simulation has been performed (OMI v1 has no simulation infrastructure); eye quality depends on PCB stackup, trace geometry, and termination — all layout-stage decisions | Oscilloscope eye diagram measurement at D0_DQ0 test point; compare against JEDEC minimum eye opening | L3/L4 |
| **Platform-specific training sensitivity** | Intel and AMD memory controllers use different training algorithms with different tolerance ranges; behavior cannot be predicted without testing | Test on both Intel and AMD Class A platforms; document pass/fail per platform with full BIOS settings | L3 |
| **DRAM device-to-device timing variation** | Timing margins depend on the specific lot of DRAM devices populated; lot-to-lot variation is a manufacturing reality | If intermittent errors appear, test multiple modules built with different DRAM lots (requires multiple fabrication runs) | L4 |
| **Thermal behavior under sustained load** | No thermal modeling has been done; DRAM self-heating depends on data patterns, refresh rate, ambient conditions, and airflow | Measure DRAM case temperature during L4 soak testing with thermal camera or contact thermometer | L4 |
| **Whether conservative JEDEC timings will train reliably on consumer boards** | Some consumer board BIOSes are optimized for XMP profiles and may behave unexpectedly with strict JEDEC base timings | Attempt training with SPD programmed for JEDEC DDR4-2400 base profile (CL17-17-17-39); document result | L3 |
| **SPD vendor ID acceptance** | Some BIOSes may check the SPD manufacturer ID byte against a known-vendor list and refuse to train unknown vendors | Program SPD with the chosen vendor ID and test; if rejected, try alternative IDs and document findings | L2/L3 |
| **VPP power-up sequencing tolerance** | JEDEC specifies VPP must be present before VDD, but consumer boards may not enforce strict sequencing; the actual tolerance is host-dependent | Monitor VPP and VDD at test points during cold boot with a dual-channel scope; check sequencing compliance | L1/L3 |

> **Policy:** An unknown is not a defect. It is an engineering question that has a defined resolution path. Every unknown in this table has a specific measurement that will resolve it. The project commits to performing these measurements when hardware is available and documenting the results — including results that reveal problems.

---

## Cross-References

- [08-2_bringup_ladder.md](./08-2_bringup_ladder.md) — Authoritative pass/fail criteria per level
- [08-3_test_matrix.md](./08-3_test_matrix.md) — Test categories, durations, and failure taxonomy
- [08-5_failure_signatures.md](./08-5_failure_signatures.md) — Detailed failure signatures FS-01 through FS-06
- [08_01_test_point_and_dft_plan.md](./08_01_test_point_and_dft_plan.md) — Test point locations referenced in diagnostic steps
- [08_03_bringup_procedure.md](./08_03_bringup_procedure.md) — Step-by-step procedure where these failures may surface

---

*This document defines what success and failure look like. For how to perform validation, see [08_03_bringup_procedure.md](./08_03_bringup_procedure.md). For where to probe, see [08_01_test_point_and_dft_plan.md](./08_01_test_point_and_dft_plan.md).*
