# Stage 6 — Implementation Translation

Stage 6 is where the architectural decisions defined in Stage 5 are translated into **implementation-ready artifacts**.

This stage does not yet produce a finished schematic or PCB.
It produces **structures that make correct implementation inevitable**.

The purpose of Stage 6 is to bridge the gap between design intent and physical realization without losing correctness.

---

## What Stage 6 Is

Stage 6 is about **translation**, not invention.

It takes:

- Signals
- Topology
- Constraints
- Power architecture
- Assumptions

and converts them into:

- Block-level schematic structure
- Clear interface boundaries
- Implementation-safe groupings
- Layout-ready intent

Every artifact in this stage must trace directly back to Stage 5.

---

## What Stage 6 Is NOT

Stage 6 does **not** include:

- Final schematics
- PCB routing
- Component selection
- Value tuning
- Signal simulation
- Optimization or cost reduction

If a decision introduces *new architectural behavior*, it does not belong here.

---

## Why Stage 6 Exists

Without Stage 6:

- Schematics become ambiguous
- Layout decisions encode hidden assumptions
- Constraints are interpreted inconsistently
- Reviews become subjective

Stage 6 exists to:

- Make implementation reviewable
- Preserve architectural intent
- Reduce rework
- Enable collaboration

This stage ensures that **the PCB cannot accidentally violate the design**.

---

## Inputs to Stage 6

Stage 6 depends on the following completed work:

- Signal maps (Stage 5)
- Topology decisions (Stage 5)
- Length matching and skew constraints
- Power rails and decoupling strategy
- Explicit design assumptions

No document in Stage 6 may contradict these inputs.

---

## Outputs of Stage 6

Stage 6 produces **implementation guidance**, not hardware.

Typical outputs include:

- Block-level schematic diagrams
- Functional grouping of pins and nets
- Connector interface definitions
- Power distribution structure
- Constraint translation notes

These outputs are precise enough that:

> Two independent engineers would implement **functionally equivalent designs**.

---

## Rules for Stage 6 Documents

All Stage 6 documents must:

- Reference Stage 5 decisions explicitly
- Avoid numerical tuning unless unavoidable
- Avoid layout-specific language
- Avoid vendor-specific parts
- Be readable without CAD tools

If a document requires a schematic editor to understand, it is too late-stage.

---

## How to Read Stage 6

The recommended reading order is:

1. `blocks/`  
   Understand functional partitioning

2. `interfaces/`  
   Understand boundaries and ownership

3. `pin_grouping/`  
   Understand how signals are organized physically

4. `constraint_translation.md`  
   Understand how architecture constrains implementation

Skipping steps risks misinterpretation.

---

## Design Philosophy at This Stage

Stage 6 follows these principles:

- Architecture is already decided
- Implementation must obey, not reinterpret
- Ambiguity is a bug
- Simplicity beats cleverness
- Reproducibility beats optimization

If something feels like a "design choice" here, it probably belongs in Stage 5 instead.

---

## Completion Criteria for Stage 6

Stage 6 is complete when:

- All functional blocks are defined
- All interfaces are documented
- Pin groupings reflect signal intent
- Constraints are implementation-visible
- No architectural decisions remain implicit

Only after this stage should:

- Schematic capture begin
- Layout work begin
- Component selection occur

---

## Takeaway

Stage 6 ensures that:

- Architecture survives contact with reality
- Implementation is disciplined
- Mistakes are hard to make silently

Stage 5 defined **what must be true**.  
Stage 6 ensures it **stays true**.
