# Stage 8.05 — Review Checklists (OMI v1)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
Draft

## Purpose
Provide structured, repeatable checklists for pre-fabrication design review and post-fabrication pre-insertion inspection. These checklists ensure that review quality is consistent regardless of who performs it — review is a process, not a personality.

---

## Relationship to Existing Documents

- [templates/L0_peer_review_checklist.md](./templates/L0_peer_review_checklist.md) — L0-specific peer review (artifact integrity). This document does not duplicate it.
- [templates/L1_peer_review_checklist.md](./templates/L1_peer_review_checklist.md) — L1-specific peer review (bench electrical). This document does not duplicate it.
- [08-4_reporting_template.md](./08-4_reporting_template.md) — Validation run report format. This document extends it with a quick-report variant.
- [08_01_test_point_and_dft_plan.md](./08_01_test_point_and_dft_plan.md) — Test point plan referenced in the pre-fab checklist.

**What this document adds:** A pre-fabrication design review checklist (run before sending Gerbers to fab), a post-fabrication pre-insertion checklist (run before putting a module in a DIMM slot), and a validation run report template.

---

## 1. Pre-Fabrication Design Review Checklist

Run this checklist **before sending Gerbers to the PCB fabricator.** Every item must be checked by at least one reviewer who did not author the corresponding design artifact. A failed item is a hard stop — do not fabricate until resolved or explicitly waived with documented justification.

### Schematic Integrity (8 items)

- [ ] **Pin map complete:** `ddr4_udimm_288_pinmap.csv` has 288 rows, 288 unique pin numbers, zero missing pins. Verified by running `scripts/verify_pinmap.py`.
- [ ] **Net naming rules pass:** All net names match patterns in [L0_artifact_integrity/naming_rules.md](./L0_artifact_integrity/naming_rules.md). Verified by running `scripts/verify_naming.py`.
- [ ] **ERC clean:** KiCad Electrical Rules Check (or equivalent) returns zero errors, zero unresolved warnings. ERC report committed as artifact.
- [ ] **Byte lanes isolated:** Each DRAM device connects only to its assigned byte lane (D0 through D7). No cross-lane DQ or DQS connections exist.
- [ ] **Rank-1 signals mapped to NC:** All rank-1 pins (CS1_n, CKE1, ODT1, CK1_t/CK1_c) are mapped to NC in the pin map with explicit notes. No floating rank-1 nets.
- [ ] **ECC/CB lane pins mapped to NC:** All CB0–CB7, DQS8_t/c, and DM8_n pins mapped to NC for non-ECC x64 configuration.
- [ ] **Power domains distinct:** VDD, VDDQ, VPP, VREF, VTT, VDDSPD, and GND are seven separate nets with no merges or aliases.
- [ ] **SPD EEPROM address correct:** SA0/SA1/SA2 strap configuration selects I²C address 0x50 (all straps low for default single-DIMM operation). WP tied to GND per Stage 7.4 decision.

### Power Delivery (5 items)

- [ ] **Decoupling capacitor plan defined:** Each power rail (VDD, VDDQ, VPP, VDDSPD) has a documented decoupling strategy — capacitor values, quantities, and placement intent per DRAM device.
- [ ] **VPP sequencing accommodated:** The design does not prevent VPP from being present before or simultaneously with VDD. No series regulation on VPP that would delay it behind VDD.
- [ ] **VREF source documented:** VREF is host-supplied (Option A, locked in Stage 7.1). Module distributes but does not generate VREF. No on-module VREF divider exists unless explicitly documented and justified.
- [ ] **VTT source identified:** VTT is host-supplied via edge connector. Module does not generate VTT. VTT is used only for termination-related functions.
- [ ] **VDDSPD isolated from DRAM rails:** VDDSPD (2.2–3.6V range) is a separate net from VDD (1.2V). No direct connection between VDDSPD and any DRAM power net.

### Signal Integrity (4 items)

- [ ] **DQS-to-DQ association verified:** Each DQS pair (D{n}_DQS_t/c) is associated exclusively with its corresponding DQ bits (D{n}_DQ0–DQ7). One-to-one per byte lane.
- [ ] **Clock distribution topology documented:** CK_t/CK_c distribution from edge connector to all 8 DRAM devices is documented. Schematic uses simplified star; fly-by ordering is noted as a layout constraint.
- [ ] **CA bus fly-by ordering noted:** Address/command/control signal routing order (fly-by topology) is documented as a layout constraint. The schematic does not enforce routing order, but a note or constraint file exists.
- [ ] **Test points incorporated:** Test point pads from [08_01_test_point_and_dft_plan.md](./08_01_test_point_and_dft_plan.md) are included in the schematic as named net-tie pads or dedicated symbols. At minimum, all P1 (must-have) test points are present.

### Mechanical (3 items)

- [ ] **PCB stackup defined:** Stackup specification exists with layer count (minimum 4), copper weights, dielectric thicknesses, and impedance targets. DDR4-2400 requires ~40 Ω single-ended (DQ), ~80 Ω differential (CK/DQS).
- [ ] **Edge connector footprint verified:** 288-pin UDIMM edge connector footprint matches JEDEC MO-303 mechanical specification. Pin pitch, contact width, and board edge offset are correct. Verified against footprint datasheet.
- [ ] **Board outline within JEDEC envelope:** PCB dimensions conform to JEDEC UDIMM height and length specification. Notch position and key location are correct for DDR4 (different from DDR3).

### Documentation (3 items)

- [ ] **BOM frozen and version-tagged:** Bill of materials is committed with specific manufacturer part numbers, quantities, and at least one alternate source per critical component. BOM has a version tag (e.g., `BOM-v1.0`).
- [ ] **All design decisions traceable:** Every design choice in the schematic can be traced to a Stage 5, 6, or 7 document. No undocumented design decisions exist.
- [ ] **Waivers documented:** Any deviation from JEDEC spec, OMI naming rules, or Stage 5/6 architecture decisions is documented with engineering justification. Waivers are listed in a dedicated section of the design review record.

### Additional Items (3 items)

- [ ] **No proprietary or NDA-gated components:** Every component in the BOM is available from public distributors without NDA or licensing restrictions. No vendor-locked parts.
- [ ] **SPD hex image defined:** The SPD EEPROM content (256 bytes) is defined, committed as a hex file, and matches the intended DDR4-2400 / 8 GB / 1Rx8 / non-ECC configuration per JESD21C.
- [ ] **Gerber/drill file generation verified:** Gerber files are generated from the final design files (not a stale export). File checksums are recorded. Fabrication notes include stackup, surface finish, and impedance control requirements.

**Total pre-fabrication checklist items: 26**

---

## 2. Post-Fabrication Pre-Insertion Checklist

Run this checklist **before inserting a fabricated module into any DIMM slot.** A failed item at this stage means the module should not be powered on until the issue is resolved.

### Visual Inspection (10 items)

- [ ] **No solder bridges visible:** Inspect all DRAM BGA land areas, decoupling capacitor pads, SPD EEPROM pads, and edge connector fingers under 10x magnification. No solder bridges between adjacent pads.
- [ ] **All DRAM devices present:** Correct number of DRAM devices populated (8 for 1Rx8 configuration). No empty DRAM positions.
- [ ] **DRAM device orientation correct:** Pin 1 indicator (dot or notch) on each DRAM device matches the PCB silkscreen/footprint orientation. Rotated devices will short power to signal.
- [ ] **SPD EEPROM present and oriented correctly:** EEPROM device is populated in the correct orientation. Pin 1 matches silkscreen.
- [ ] **Edge connector gold fingers clean:** No solder splashes, flux residue, or contamination on the 288 gold finger contacts. Clean with isopropyl alcohol if needed.
- [ ] **All decoupling capacitors present:** Visual comparison against BOM — all decoupling cap positions are populated. No missing components.
- [ ] **PCB silkscreen legible:** Board revision, OMI branding, and reference designators are readable. Board revision matches expected version.
- [ ] **No damaged or lifted pads:** No pads peeling from the PCB substrate. No visible trace damage.
- [ ] **Board dimensions correct:** Module fits the JEDEC UDIMM mechanical envelope. No oversized or undersized boards.
- [ ] **Module seats in test jig without force:** If using a Class C jig or DIMM socket, the module inserts smoothly. Binding or resistance indicates mechanical mismatch.

### Electrical Pre-Check (5 items)

- [ ] **VDD not shorted to GND:** DVM between VDD test point and GND reads > 100 kΩ (no short). Expected: high resistance (capacitor charge effect may show low initial reading that rises).
- [ ] **VDDQ not shorted to GND:** DVM between VDDQ test point and GND reads > 100 kΩ.
- [ ] **VPP not shorted to GND:** DVM between VPP (pin 142) and GND reads > 100 kΩ.
- [ ] **I²C pull-up resistance within range:** DVM from SDA (pin 285) to VDDSPD (pin 284) reads 2.2–10 kΩ (host pull-up present, or external pull-up if using jig). SCL (pin 141) to VDDSPD same range.
- [ ] **Edge connector pins visually aligned:** No bent, bridged, or missing gold finger contacts. All 288 positions present.

### Administrative (2 items)

- [ ] **Module labeled with build ID and date:** A physical label or marking on the PCB identifies the module (e.g., `OMI-V1-BUILD-001-20260320`). This ID is used in all validation run reports.
- [ ] **Pre-insertion checklist recorded:** This completed checklist is saved as an artifact in `validation/runs/[PLATFORM_ID]/L1/` with the module build ID and date.

**Total post-fabrication checklist items: 17**

---

## 3. Validation Run Report Template

### Full Report

For complete validation runs, use the standardized report format in [08-4_reporting_template.md](./08-4_reporting_template.md). That template is authoritative and must be used for all formal submissions.

### Quick Report (Informal / Community Testing)

For informal community testing or early-stage experiments where the full template would be disproportionate, use this reduced format. Quick reports are valuable but are not a substitute for formal reports when pursuing Stage 8 closure.

```markdown
## Quick Validation Report

**Run ID:** [Per 08-4 scheme: RUN-YYYYMMDD-PLATFORM-LEVEL-SEQ]
**Date:** [YYYY-MM-DD]
**Tester:** [Name or handle]

### Platform
| Field | Value |
|-------|-------|
| Board | [Manufacturer + model] |
| BIOS version | |
| CPU | |
| OS | |

### Module
| Field | Value |
|-------|-------|
| Build ID | |
| PCB revision | |

### What Was Tested
- Level: L1 / L2 / L3 / L4
- Tests run: [List test categories from 08-3]
- Duration: [Total test time]

### Result
**Overall: PASS / FAIL / PARTIAL**

| Test | Result | Notes |
|------|--------|-------|
| [Test name] | PASS/FAIL | [Brief note] |

### Failures (if any)
[Describe each failure: symptom, suspected cause, what was tried]

### Evidence Attached
- [ ] [List files: screenshots, logs, dumps]

### Notes
[Anything unusual, observations, suggestions for next steps]
```

> **When to use quick vs. full report:** Use the quick report for exploratory testing, community contributions where the full template is a barrier, or intermediate checkpoints during a longer validation session. Use the full report ([08-4_reporting_template.md](./08-4_reporting_template.md)) for any result that will be cited in Stage 8 closure evidence.

---

## Cross-References

- [templates/L0_peer_review_checklist.md](./templates/L0_peer_review_checklist.md) — L0-specific peer review
- [templates/L1_peer_review_checklist.md](./templates/L1_peer_review_checklist.md) — L1-specific peer review
- [08-4_reporting_template.md](./08-4_reporting_template.md) — Full validation report template (authoritative)
- [08_01_test_point_and_dft_plan.md](./08_01_test_point_and_dft_plan.md) — Test point plan (referenced in pre-fab checklist §SI)
- [L0_artifact_integrity/naming_rules.md](./L0_artifact_integrity/naming_rules.md) — Net naming regex patterns
- [08_06_stage8_closure_criteria.md](./08_06_stage8_closure_criteria.md) — What closure requires from these checklists

---

*This document defines what to check. For how to perform validation measurements, see [08_03_bringup_procedure.md](./08_03_bringup_procedure.md). For what pass/fail means, see [08-2_bringup_ladder.md](./08-2_bringup_ladder.md).*
