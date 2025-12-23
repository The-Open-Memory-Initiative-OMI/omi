# Stage 10 — Layout & SI/PI Guidelines

Stage 10 defines **layout, signal integrity (SI), and power integrity (PI) guidelines** for the OMI v1 DIMM design.

This stage does not provide routing recipes or numeric constraints.
It defines **physical design intent** so that layout decisions remain consistent with earlier architectural stages.

Stage 10 answers one question:
> How must the PCB be laid out so the design we already defined can actually work?

---

## Purpose of Stage 10

Stage 10 exists to:

- Translate architectural intent into physical behavior expectations
- Prevent layout from silently redefining the design
- Make SI/PI review possible before fabrication
- Ensure margin preservation across manufacturing and environment

Layout is not where architecture is decided.
Layout is where architecture either survives—or dies quietly.

---

## Scope and Non-Goals

### In Scope

- Routing intent
- Reference plane strategy
- Signal return behavior
- Crosstalk control philosophy
- Power distribution intent
- Decoupling placement philosophy
- Review criteria for SI/PI readiness

### Explicitly Out of Scope

- Numeric impedance targets
- Trace width / spacing values
- Stack-up specification
- Vendor-specific layout rules
- Simulation results

Those belong to execution and validation stages.

---

## Foundational Physical Assumptions

The following are assumed throughout Stage 10:

- Continuous reference planes exist
- Controlled impedance routing is available
- PCB manufacturing is standard, not exotic
- Layout engineer has authority to adjust geometry within intent

If these assumptions are not met, the design is not eligible for implementation.

---

## Signal Integrity (SI) Guidelines

### 1. Reference Plane Continuity

All high-speed signals must:
- Have a continuous reference plane
- Avoid crossing plane splits
- Avoid reference transitions without return paths

Broken return paths are timing errors in disguise.

---

### 2. Data (DQ/DQS) Routing Intent

Each byte lane must be treated as:
- An independent timing domain
- A tightly coupled signal group

Guidelines:
- Keep DQ signals of a lane physically close
- Keep DQS adjacent to its DQ group
- Avoid stubs and branching
- Preserve point-to-point topology strictly

If a DQ signal branches, the lane is already broken.

---

### 3. Lane-to-Lane Isolation

Byte lanes must be:
- Physically separable
- Not interwoven unnecessarily
- Protected from aggressive coupling

Guidelines:
- Avoid long parallel runs between different lanes
- Avoid serpentine interleaving across lanes
- Preserve visual and physical separation

Lane isolation supports both SI and failure containment.

---

### 4. Address and Command Routing Intent

Address and command signals are:
- Shared
- Unidirectional
- Fly-by distributed

Guidelines:
- Preserve monotonic routing order
- Avoid star or tree replication
- Maintain consistent relative spacing

Predictability matters more than symmetry.

---

### 5. Clock Routing Intent

Clock signals are:
- Global
- Differential
- Timing-critical for the entire system

Guidelines:
- Keep differential pairs tightly coupled
- Match within-pair lengths
- Minimize exposure to aggressor signals
- Route clocks with priority over other signals

Clock integrity defines global margin.

---

### 6. Crosstalk Management Philosophy

Crosstalk is managed by:
- Spacing
- Reference planes
- Routing order
- Avoiding unnecessary parallelism

Guidelines:
- Do not rely on simulation alone to justify risky adjacency
- Treat DQS and clock as sensitive victims
- Treat wide, fast buses as aggressors

If two signals must be close, they must be friends.

---

## Power Integrity (PI) Guidelines

### 7. Power Plane Strategy

Each power rail must:
- Have a low-impedance distribution path
- Remain isolated from other rails
- Be referenced to a stable ground system

Planes are preferred over long traces for high-current rails.

---

### 8. Decoupling Placement Philosophy

Decoupling exists to:
- Shorten current loops
- Localize transient demand
- Prevent noise propagation

Guidelines:
- Place high-frequency decoupling close to consumers
- Place bulk decoupling to support regional stability
- Do not treat all decoupling as interchangeable

Decoupling placement is part of timing correctness.

---

### 9. Vref Treatment

Vref must be treated as:
- An analog reference
- A noise-sensitive node
- A non-power rail

Guidelines:
- Isolate from switching currents
- Avoid adjacency to aggressor signals
- Filter and stabilize aggressively

Vref noise directly reduces voltage margin.

---

### 10. VTT Treatment

VTT must be treated as:
- A dynamic termination rail
- Capable of sourcing and sinking current

Guidelines:
- Provide low-inductance paths
- Avoid sharing impedance with logic supplies
- Keep termination return paths short

Termination instability shows up as ringing, not obvious power failure.

---

## Ground and Return Path Guidelines

Ground is not a single thing.

Guidelines:
- Maintain continuous ground reference
- Avoid narrow necks in ground paths
- Ensure return paths exist for all high-speed signals
- Treat ground vias as signal integrity components

Poor ground design invalidates good routing.

---

## Layout Review Checklist (SI/PI)

Before layout is considered acceptable:

### Signal Integrity

- [ ] No high-speed signal crosses a plane split
- [ ] Byte lanes are isolated and intact
- [ ] DQS is adjacent to its DQ group
- [ ] Clock routing is clear and protected
- [ ] No unintended stubs exist

### Power Integrity

- [ ] All rails are clearly separated
- [ ] Decoupling intent is visible and rational
- [ ] Vref is isolated and quiet
- [ ] VTT paths are short and well-defined
- [ ] Ground reference is continuous

If any answer is "unclear," layout is not ready.

---

## Relationship to Validation (Stage 8)

Stage 10 guidelines are validated by:
- Visual inspection
- Constraint consistency
- Power and signal sanity review

They are prerequisites for:
- SI simulation
- PI analysis
- Fabrication readiness

Simulation without discipline is false confidence.

---

## Takeaway

Stage 10 ensures that:
- Physics respects architecture
- Layout does not invent new behavior
- Margins are preserved intentionally
- Failures are not mysterious

Good layout does not make a bad design work.
But bad layout will absolutely break a good one.

---

Next possible stages:
- Stage 11 — SI Simulation Framework
- Stage 11 — PI Analysis Framework
- Stage 11 — Fabrication & Bring-Up Checklist
