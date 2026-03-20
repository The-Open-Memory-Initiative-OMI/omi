# Stage 8.06 — Stage 8 Closure Criteria (OMI v1)

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
Draft

## Purpose
Define what "Stage 8 complete" means so the project can move to Stage 9 (Minimal Reference Schematic) with confidence. Stage 8 is not open-ended — this document establishes its exit conditions, what it explicitly does not require, and what it hands off to the next stage.

---

## 1. Stage 8 Exit Criteria

All conditions in this table must be TRUE to declare Stage 8 fully closed.

| # | Criterion | Evidence Required | Status |
|---|-----------|-------------------|--------|
| 1 | L0 validation complete and documented | L0 scripts pass (`verify_pinmap.py`, `verify_naming.py`); L0 report committed per [L0 report template](./templates/L0_validation_report.md); peer review completed per [L0 peer review checklist](./templates/L0_peer_review_checklist.md) | Pending |
| 2 | Test point plan defined and ready for layout integration | [08_01_test_point_and_dft_plan.md](./08_01_test_point_and_dft_plan.md) committed and reviewed; test point locations traceable to pin map CSV | Pending |
| 3 | At least one validation platform identified with full documentation | Platform record completed per [08_02_validation_platform_strategy.md](./08_02_validation_platform_strategy.md) §5 template; platform verified with known-good DIMM | Pending |
| 4 | Bring-up procedure written and self-contained | [08_03_bringup_procedure.md](./08_03_bringup_procedure.md) committed; another engineer could follow it without oral instructions | Pending |
| 5 | Success criteria and failure modes documented | [08_04_success_criteria_and_failure_modes.md](./08_04_success_criteria_and_failure_modes.md) committed; failure reporting template usable | Pending |
| 6 | Review checklists and reporting templates published | [08_05_review_checklists.md](./08_05_review_checklists.md) committed; pre-fabrication checklist ready to execute | Pending |
| 7 | All Stage 8 documents committed to `docs/08_validation_and_review/` | All `08_0N` files plus existing `08-N` files in repository | Pending |
| 8 | README.md updated to index all Stage 8 documents | [README.md](./README.md) lists both foundational (`08-N`) and operational (`08_0N`) series | Pending |

### Criterion interpretation

- Criteria 1 is a hard gate that requires script execution and peer review. It cannot be waived.
- Criteria 2–8 are documentation gates. They require committed, reviewed markdown files — not fabricated hardware.
- "Reviewed" means at least one engineer other than the author has read the document and confirmed it is complete and self-consistent.

---

## 2. What Stage 8 Does NOT Require

The following are explicitly **not required** for Stage 8 closure. Stating these boundaries prevents scope creep.

| Not Required | Why Not |
|-------------|---------|
| **Fabricated hardware** | Hardware is produced after Stage 10 (Layout). Stage 8 is a planning and documentation stage. |
| **Physical validation runs (L1–L4)** | L1–L4 require a manufactured module. Stage 8 defines the procedures; execution happens post-fabrication. |
| **Detailed L4 stress procedures** | L4 procedures depend on real failure data that does not exist yet. Intent and pass criteria are documented in [08_03_bringup_procedure.md](./08_03_bringup_procedure.md) §6; detailed procedures will be written post-fabrication. |
| **FPGA validation platform setup** | FPGA-based testing (Class B) is a stretch goal per [08_02_validation_platform_strategy.md](./08_02_validation_platform_strategy.md) §3. It is not required for Stage 8 or v1 closure. |
| **Signal integrity simulation** | OMI v1 has no SI simulation infrastructure. Eye quality will be measured empirically at L3/L4. |
| **Power integrity simulation** | Same as SI — no PDN simulation infrastructure. Rail quality will be measured at test points. |
| **Performance characterization** | OMI v1 validates correctness, not performance. Bandwidth benchmarks, latency measurements, and overclocking are out of scope. |
| **Multi-platform validation** | One Class A platform is sufficient for Stage 8 closure. Cross-platform replication is recommended but not gating. |
| **Commercial qualification** | No JEDEC compliance certification, reliability qualification, or vendor approval is required for v1. |
| **Temperature variance testing (T7)** | T7 is optional per [08-3_test_matrix.md](./08-3_test_matrix.md). Not required for any stage closure. |

---

## 3. Handoff to Stage 9

When Stage 8 closes, Stage 9 (Minimal Reference Schematic) receives the following from Stage 8:

### 3.1 Test Point Requirements for Layout

From [08_01_test_point_and_dft_plan.md](./08_01_test_point_and_dft_plan.md):

- 10 must-have test point locations with specific net names, pin references, and pad size recommendations
- 3 needed-for-L3+ test points for signal integrity measurement
- 4 nice-to-have test points for secondary debug
- Explicit DFT philosophy: test point stubs are acceptable for v1; optimize for probe access, not SI purity

**Stage 9 action:** Incorporate test point pad footprints into the schematic symbol library and netlist. Layout (Stage 10) must place these pads with adequate probe clearance.

### 3.2 Impedance and Stackup Constraints

From [08_02_validation_platform_strategy.md](./08_02_validation_platform_strategy.md) and the overall DDR4 design:

- DDR4-2400 target speed requires controlled impedance traces: ~40 Ω single-ended (DQ), ~80 Ω differential (CK, DQS)
- PCB stackup must support these impedance targets; minimum 4-layer stackup recommended
- These constraints are not new to Stage 9 — they originate from Stage 6 block decomposition — but Stage 8 confirms they are testable via the test point plan

**Stage 9 action:** Include impedance targets in schematic notes and constraint files.

### 3.3 SPD Content Specification

From [08_04_success_criteria_and_failure_modes.md](./08_04_success_criteria_and_failure_modes.md):

- L2 validation requires SPD programmed with: DDR4, 8 GB, 1Rx8, DDR4-2400, non-ECC, JEDEC base timings (CL17-17-17-39)
- SPD vendor ID selection may affect platform acceptance (documented as honest unknown)
- SPD hex image must be defined, version-controlled, and referenced in the BOM

**Stage 9 action:** Define the SPD hex image as a design artifact. Include the EEPROM programmer and hex file in the BOM and build instructions.

### 3.4 Definition of "Done" for the Complete Design

Stage 8 establishes what a successfully validated module looks like:

- L3 pass on at least one Class A platform = minimum viable validation
- L4 pass = full confidence for the reference design
- All results documented per [08-4_reporting_template.md](./08-4_reporting_template.md)

**Stage 9 action:** Ensure the schematic is complete enough to fabricate, populate, and validate using the procedures defined in Stage 8.

---

## 4. Partial Closure

Stage 8 supports **partial closure** to allow parallel progress:

| Partial State | What's Done | What's Remaining | Stage 9 Can Start? |
|--------------|-------------|-----------------|-------------------|
| **L0 complete, docs committed** | L0 scripts pass; all 08_0N docs committed | L1–L4 procedures untested (no hardware) | **Yes** — Stage 9 schematic work can begin |
| **L0 + L1 complete** | L0 and L1 pass on fabricated module | L2–L4 require host platform | Yes — Stage 10 layout can begin in parallel |
| **Full closure** | L0 through L3 pass on at least one platform | L4 recommended but not gating | Stage 9/10 complete; ready for community release |

> **Why partial closure exists:** Waiting for full L3 validation before starting any Stage 9 work would serialize the project unnecessarily. The schematic (Stage 9) can be refined while waiting for fabrication, and validation procedures can be executed as soon as hardware arrives. Partial closure enables this parallelism while maintaining a clear record of what has been validated and what is still pending.

### Re-validation requirement

If Stage 8 validation reveals a design error that requires a schematic change:

1. The change is made in Stage 9
2. All affected validation levels must be re-run (e.g., a pin map change invalidates L0 and all subsequent levels)
3. A new validation run is opened with a new Run ID
4. The original failure is cross-referenced in the new run report

---

## 5. Stage 8 Document Index

For completeness, here is the full list of Stage 8 documents that must be committed for closure:

### Foundational Reference Series (08-N)

| File | Purpose |
|------|---------|
| `08-1_validation_platforms.md` | Platform class taxonomy (A/B/C) |
| `08-2_bringup_ladder.md` | Validation ladder (L0–L4) with pass/fail criteria |
| `08-3_test_matrix.md` | Test categories (T1–T7), durations, failure taxonomy |
| `08-4_reporting_template.md` | Standardized validation report format |
| `08-5_failure_signatures.md` | Failure signatures FS-01 through FS-06 |

### Operational Document Series (08_0N)

| File | Purpose |
|------|---------|
| `08_01_test_point_and_dft_plan.md` | Test point locations and DFT philosophy |
| `08_02_validation_platform_strategy.md` | Specific platform recommendations and phased strategy |
| `08_03_bringup_procedure.md` | Step-by-step bring-up from bare PCB to OS boot |
| `08_04_success_criteria_and_failure_modes.md` | Consolidated criteria, failure catalog, honest unknowns |
| `08_05_review_checklists.md` | Pre-fab and post-fab checklists, report templates |
| `08_06_stage8_closure_criteria.md` | This document — exit criteria and Stage 9 handoff |

### Supporting Artifacts

| Directory/File | Purpose |
|---------------|---------|
| `L0_artifact_integrity/` | L0 naming rules, README |
| `L1_bench_electrical/` | L1 measurement procedures, probe sequence, log template |
| `scripts/` | Automated validation scripts (l0_runner.py, l1_runner.py, etc.) |
| `templates/` | Report templates and peer review checklists |

---

## Cross-References

- [08-2_bringup_ladder.md](./08-2_bringup_ladder.md) — Validation ladder defining each level
- [08-4_reporting_template.md](./08-4_reporting_template.md) — Report format for all validation runs
- [08_01_test_point_and_dft_plan.md](./08_01_test_point_and_dft_plan.md) — Test point plan for Stage 9 handoff
- [08_02_validation_platform_strategy.md](./08_02_validation_platform_strategy.md) — Platform strategy and risk register
- [08_03_bringup_procedure.md](./08_03_bringup_procedure.md) — Bring-up procedure
- [08_04_success_criteria_and_failure_modes.md](./08_04_success_criteria_and_failure_modes.md) — Success/failure definitions
- [08_05_review_checklists.md](./08_05_review_checklists.md) — Review checklists

---

*This document defines when Stage 8 is done. For how to perform validation, start with [08_03_bringup_procedure.md](./08_03_bringup_procedure.md).*
