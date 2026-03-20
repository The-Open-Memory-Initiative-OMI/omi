# Stage 8 — Validation & Review Playbook (OMI v1)

Stage 8 defines **how OMI v1 is validated and reviewed** before, during, and after schematic and layout work.

Its purpose is to:

- Detect architectural violations early
- Prevent silent margin erosion
- Make failures explainable instead of mysterious
- Enable disciplined, repeatable review by multiple engineers

This stage validates *correctness*, not performance.

---

## Why Validation Comes Before Build Claims

Memory systems rarely fail because of one large mistake.
They fail because of **many small, individually "acceptable" violations**.

Stage 8 exists to ensure:

> **Every important rule has a place where it is checked — and produces artifacts.**

Validation without artifacts is opinion, not engineering.

(Testing/measurement contributions must include platform details, tools, procedures, and results incl. failures.)

---

## Validation Philosophy

OMI validation follows four principles:

1. **Structural correctness first**
2. **Timing margin preservation**
3. **Power integrity visibility**
4. **Failure must be explainable**

If a design fails and you cannot point to *which rule was violated*, validation failed.

---

## Validation Ladder (Evidence Levels)

Stage 8 is not a single event. Evidence accumulates in levels:

- **L0 — Artifact Integrity:** ERC sanity, pin map integrity (288/288), naming consistency
- **L1 — Bench Electrical:** continuity, rail presence/behavior, SPD bus read
- **L2 — Host Enumeration:** SPD read in a host, BIOS reports plausible config
- **L3 — Training + Boot:** training completes, OS boots and uses RAM
- **L4 — Stress + Soak:** long memory tests, repeatability, documented failures

---

## Layer 0 — Artifact Integrity Review (Hard Gate)

### Objective

Ensure artifacts are internally consistent and reviewable.

### Checklist

- [ ] Pin map CSV is complete (288/288), no duplicate pins, no missing pins
- [ ] Net manifest matches schematic net names (no aliases)
- [ ] Decisions are referenced where relevant (VREF Option A, CA/CLK schematic topology, DQ naming, SPD WP policy)
- [ ] If something is uncertain, it is stated explicitly

### Failure indicators

- Missing/duplicated pin numbers in CSV
- Hidden renames ("same net with different names")
- Undocumented tie-offs or "magic" assumptions

Hard stop until fixed.

---

## Layer 1 — Architecture Compliance Review

### Objective

Ensure no artifact violates Stage 5 architecture.

### Checklist

- [ ] **DQ naming is per-lane/per-DRAM (D0..D7)** and prevents shared DQ nets
- [ ] CA/CLK nets are shared across DRAMs (connectivity correct)
- [ ] Clocks are differential and unambiguous
- [ ] Rank boundaries and unused rank-1 connector pins are explicitly handled (NC + notes)
- [ ] No undocumented architectural behavior exists

### Failure indicators

- Shared DQ nets across multiple lanes/devices
- Cross-lane connections
- Local clock buffering / multiple clock domains (without justification)

Hard stop.

---

## Layer 2 — Schematic Structure Review

### Objective

Ensure schematics encode intent structurally, not implicitly.

### Checklist

- [ ] Lane boundaries are explicit (D0..D7 naming; no cross-lane ambiguity)
- [ ] DQS is adjacent/clearly associated with its DQ bundle (by naming and grouping)
- [ ] CA/CLK/control signals are not duplicated as separate drivers
- [ ] Power nets are explicit and not "hidden by assumption"
- [ ] Notes exist where the schematic uses abstraction (e.g., simplified star representation)

### Failure indicators

- Ambiguous or inconsistent net naming
- "We'll fix it in layout" used to justify unclear connectivity
- Hidden coupling paths not obvious in schematic

---

## Layer 3 — Constraint Adherence Review

### Objective

Ensure Stage 5 constraints survive implementation.

### Timing constraints (schematic-level intent)

- [ ] DQ within a lane is treated as a group (lane-based naming)
- [ ] DQS-to-DQ association is one-to-one per lane
- [ ] No artificial lane-to-lane matching constructs appear

### CA/CLK topology (important clarification)

- [ ] **Schematic may use simplified star representation**
- [ ] **Fly-by ordering is enforced at layout/constraints stage**, not by schematic wiring

### Power constraints

- [ ] VDD, VDDQ, VREF, VTT are never merged
- [ ] VREF is not used as a supply
- [ ] VTT is only used for termination-related functions (connector-level rail)

---

## Layer 4 — Power Integrity Review (Split)

### 4A — Schematic PI sanity

- [ ] Rails are defined and not merged
- [ ] VREF treated as noise-sensitive reference (not a "power rail")
- [ ] SPD supply is isolated from DRAM rails (VDDSPD exists and is mapped)

### 4B — Layout readiness gate (before layout begins)

- [ ] A decoupling plan exists per rail (rail-specific intent)
- [ ] Measurement points / debug hooks are planned (where feasible)

---

## Layer 5 — Failure Containment Review

### Objective

Ensure failures are localized and diagnosable.

### Checklist

- [ ] Byte-lane failures do not electrically affect other lanes
- [ ] SPD failures do not electrically affect DRAM operation
- [ ] Power rail instability is traceable to a domain
- [ ] No single-point failure silently breaks the entire system

---

## Validation Artifacts (Required)

Every validation pass produces:

- Completed checklist + pass/fail notes
- Annotated schematic screenshots (as needed)
- Explicit waivers (if any), with justification
- If testing/measurement is involved: platform details, tools, procedures, results incl failures

---

## Review Roles (Recommended)

- Architect reviewer (architecture compliance)
- Implementation reviewer (schematic clarity)
- Power/PI reviewer (rail correctness / PI readiness)

---

## Stage 8 Document Index

### Foundational Reference Documents

These define the validation framework — platform taxonomy, ladder levels, test categories, reporting format, and failure signatures.

| Document | Purpose |
|----------|---------|
| [08-1_validation_platforms.md](./08-1_validation_platforms.md) | Platform class taxonomy (Class A/B/C), minimum requirements, evidence capabilities |
| [08-2_bringup_ladder.md](./08-2_bringup_ladder.md) | Validation ladder (L0–L4) with pass/fail criteria and stop conditions |
| [08-3_test_matrix.md](./08-3_test_matrix.md) | Test categories (T1–T7), minimum durations, failure taxonomy |
| [08-4_reporting_template.md](./08-4_reporting_template.md) | Standardized validation report format, Run ID scheme, artifact naming |
| [08-5_failure_signatures.md](./08-5_failure_signatures.md) | Six failure signatures (FS-01 through FS-06) with symptom-to-cause mappings |

### Operational Documents

These operationalize the framework — specific test points, platform recommendations, step-by-step procedures, consolidated criteria, checklists, and closure definitions.

| Document | Purpose |
|----------|---------|
| [08_01_test_point_and_dft_plan.md](./08_01_test_point_and_dft_plan.md) | Test point locations, DFT philosophy, probe access requirements for layout |
| [08_02_validation_platform_strategy.md](./08_02_validation_platform_strategy.md) | Specific platform recommendations, cost estimates, phased strategy, risk register |
| [08_03_bringup_procedure.md](./08_03_bringup_procedure.md) | Step-by-step bring-up from bare PCB to OS boot |
| [08_04_success_criteria_and_failure_modes.md](./08_04_success_criteria_and_failure_modes.md) | Consolidated success criteria, failure catalog, diagnostic decision trees, honest unknowns |
| [08_05_review_checklists.md](./08_05_review_checklists.md) | Pre-fabrication (26 items) and post-fabrication (17 items) checklists, quick-report template |
| [08_06_stage8_closure_criteria.md](./08_06_stage8_closure_criteria.md) | Stage 8 exit criteria, what's not required, handoff to Stage 9 |

### Playbooks and Detailed Procedures

| Document | Purpose |
|----------|---------|
| [OMI Stage 8 L0 Playbook Development.md](<./OMI Stage 8 L0 Playbook Development.md>) | Comprehensive L0 playbook with 5 execution sessions and risk register |
| [OMI Stage 8 L1 Validation Guide.md](<./OMI Stage 8 L1 Validation Guide.md>) | Comprehensive L1 playbook with 3 bench sessions and equipment requirements |

### Supporting Artifacts

| Directory | Contents |
|-----------|----------|
| [L0_artifact_integrity/](./L0_artifact_integrity/) | L0 naming rules, README |
| [L1_bench_electrical/](./L1_bench_electrical/) | L1 measurement procedures, probe sequence CSV, measurement log template |
| [scripts/](./scripts/) | Automated validation scripts (l0_runner.py, l1_runner.py, verify_pinmap.py, etc.) |
| [templates/](./templates/) | L0/L1 report templates, peer review checklists, PR templates |

---

## Next

Stage 8 closure criteria are defined in [08_06_stage8_closure_criteria.md](./08_06_stage8_closure_criteria.md). When all exit criteria are met:

- Stage 9 — Minimal Reference Schematic (Correctness-First)
