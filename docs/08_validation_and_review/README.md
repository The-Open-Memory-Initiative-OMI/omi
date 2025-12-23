# Stage 8 — Validation & Review Playbook

Stage 8 defines **how the OMI v1 design is validated and reviewed** before, during, and after schematic and layout work.

Its purpose is to:
- Detect architectural violations early
- Prevent silent margin erosion
- Make failures explainable instead of mysterious
- Enable disciplined, repeatable review by multiple engineers

This stage validates *correctness*, not performance.

---

## Why Validation Comes Before Reference Schematics

Memory systems rarely fail because of one large mistake.
They fail because of **many small, individually "acceptable" violations**.

Without a validation framework:
- Errors hide across sheets
- Responsibility becomes unclear
- Reviews become subjective
- Failures appear late and intermittently

Stage 8 exists to ensure:
> **Every important rule has a place where it is checked.**

---

## Validation Philosophy

OMI validation follows four principles:

1. **Structural correctness first**
2. **Timing margin preservation**
3. **Power integrity visibility**
4. **Failure must be explainable**

If a design fails and you cannot point to *which rule was violated*, validation failed.

---

## Validation Layers

Validation is performed in **layers**, each with a clear goal:

1. Architecture compliance
2. Schematic correctness
3. Constraint adherence
4. Power integrity sanity
5. Failure containment

Each layer catches different classes of errors.

---

## Layer 1 — Architecture Compliance Review

### Objective
Ensure that no schematic or layout artifact violates Stage 5 architecture.

### Checklist

- [ ] Data topology is point-to-point per byte lane
- [ ] Address/command topology is shared (fly-by intent preserved)
- [ ] Clock topology is shared and differential
- [ ] Byte lanes are independent timing domains
- [ ] No undocumented architectural behavior exists

### Failure Indicators

- Shared DQ nets
- Replicated command drivers
- Local clock buffering
- Cross-lane connections

Any violation here is a **hard stop**.

---

## Layer 2 — Schematic Structure Review

### Objective
Ensure schematics encode intent structurally, not implicitly.

### Checklist

- [ ] Each byte lane has its own schematic sheet
- [ ] DQS is adjacent to its DQ bundle
- [ ] Address/command buses are not exploded unnecessarily
- [ ] Rank boundaries are explicit
- [ ] No implicit power pins are used

### Failure Indicators

- Mixed-lane symbols
- Hidden power connections
- Ambiguous net naming
- "We'll fix it in layout" comments

If intent is not visible, the schematic is invalid.

---

## Layer 3 — Constraint Adherence Review

### Objective
Ensure Stage 5 constraints survive implementation.

### Timing Constraints

- [ ] DQ within a lane is grouped and treated as matched
- [ ] DQS-to-DQ association is one-to-one
- [ ] No artificial lane-to-lane matching constructs appear
- [ ] Clock path is global and unambiguous

### Power Constraints

- [ ] VDD, VDDQ, Vref, VTT are never merged
- [ ] Vref is not used as a supply
- [ ] VTT is only used for termination-related functions

### Failure Indicators

- Serpentine implied in schematics
- Rails shorted "for convenience"
- Reference nets used as power

Constraint violations are correctness violations.

---

## Layer 4 — Power Integrity Sanity Review

### Objective
Ensure power behavior is electrically plausible.

### Checklist

- [ ] Each rail has visible decoupling intent
- [ ] Decoupling is rail-specific
- [ ] No rail is under-defined
- [ ] Auxiliary power is isolated from high-speed domains

### Failure Indicators

- Single capacitor used "for everything"
- Missing decoupling placeholders
- Vref tied to noisy domains
- SPD powered from DRAM rails

Power issues often appear as timing failures later.

---

## Layer 5 — Failure Containment Review

### Objective
Ensure failures are localized and diagnosable.

### Checklist

- [ ] Byte-lane failures do not affect other lanes
- [ ] SPD failures do not affect DRAM operation electrically
- [ ] Power rail instability is traceable to a domain
- [ ] No single-point failure silently breaks the entire system

### Failure Indicators

- Shared nets where isolation is expected
- Global dependence on auxiliary logic
- Hidden coupling paths

A failure that spreads uncontrollably is a design failure.

---

## Validation Artifacts

Every validation pass should produce:

- A completed checklist (this document)
- Annotated schematic screenshots
- Clear pass/fail notes
- Explicit waivers (if any), with justification

Validation without artifacts is opinion, not engineering.

---

## Review Roles (Recommended)

- **Architect reviewer**  
  Verifies architectural compliance

- **Implementation reviewer**  
  Verifies schematic correctness and clarity

- **Power/PI reviewer**  
  Verifies rail behavior and decoupling intent

One person may fill multiple roles, but the roles must exist conceptually.

---

## When Validation Occurs

Validation is not a single event.

It must occur:
- Before schematic capture (design readiness)
- After schematic capture (implementation correctness)
- Before layout begins
- After layout completion (against constraints)

Skipping a stage creates blind spots.

---

## What This Stage Does NOT Do

Stage 8 does not:
- Simulate signals
- Measure margins
- Optimize performance
- Certify the design

It ensures the design is **eligible** for those activities.

---

## Takeaway

Validation is how you turn "I think it's right" into "I know why it's right."

Stage 8 ensures that:
- Mistakes are caught early
- Reviews are objective
- Failures are explainable
- OMI v1 remains trustworthy

A design that cannot be reviewed is already broken.

---

Next Stage:
- Stage 9 — Minimal Reference Schematic (Correctness-First)
