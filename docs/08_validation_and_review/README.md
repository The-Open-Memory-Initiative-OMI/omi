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

## Next

Stage 8 continues into platform selection + bring-up reporting templates, then:

- Stage 9 — Minimal Reference Schematic (Correctness-First)
