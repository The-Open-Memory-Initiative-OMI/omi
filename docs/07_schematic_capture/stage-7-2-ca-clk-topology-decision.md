# Stage 7.2 — Address / Command / Clock Topology Decision

## Project
Open Memory Initiative (OMI) — OMI v1 DDR4 UDIMM

## Status
✅ Locked

## Date
2026-01-27

---

## Decision Summary

For **Stage 7.2 (Address / Command / Clock schematic capture)**, the CA/CLK topology is represented as a:

> **Simplified Star (Logical Point-to-Point) Topology**

This decision applies **only to the schematic representation**.

JEDEC fly-by behavior is **explicitly deferred** to later stages (layout and signal-integrity constraints).

---

## Scope of This Decision

This decision governs:
- How CA/CLK nets are **drawn and connected in the schematic**
- How signal intent is communicated at **Stage 7 (Schematic Capture)**

This decision does **not** govern:
- Physical routing order
- Trace length matching
- Termination placement
- Signal integrity optimization

Those are handled in later stages.

---

## Options Considered

### Option A — JEDEC Fly-By Topology (Schematic-Level)

**Description**  
CA/CLK signals are daisy-chained from DRAM to DRAM, with termination at the end of the chain.

**Advantages**
- Matches JEDEC physical routing recommendations
- Reflects production-grade DDR implementations

**Disadvantages**
- Introduces schematic-level ordering constraints prematurely
- Increases complexity for early-stage learning and review
- Couples schematic intent tightly to layout decisions
- Harder to reason about and maintain in an open, educational project

---

### Option B — Simplified Star / Logical Point-to-Point (Chosen)

**Description**  
Each CA/CLK signal is represented as a single net connecting:
- The host interface
- All DRAM devices

No daisy-chain ordering is implied in the schematic.

**Advantages**
- Clear and readable schematic intent
- Easier review and onboarding for new contributors
- Decouples schematic correctness from physical routing
- Preserves flexibility for enforcing fly-by later
- Common practice in early-stage and educational designs

**Disadvantages**
- Does not visually encode JEDEC fly-by behavior
- Requires later documentation to avoid misinterpretation

---

## Rationale for Selection

The Open Memory Initiative prioritizes:
- Learning clarity
- Architectural transparency
- Incremental complexity

At Stage 7:
- The schematic's role is to define **connectivity and intent**
- Physical topology is better enforced at:
  - Stage 8 — Validation & Review
  - Stage 10 — Layout & SI/PI Guidelines

Representing fly-by at the schematic level would:
- Increase cognitive load
- Obscure functional understanding
- Encourage cargo-cult implementation without context

Therefore, **Option B** is the correct choice for OMI v1.

---

## Explicit Constraint (Important)

> **This schematic representation does NOT imply star routing on the PCB.**

JEDEC fly-by requirements for CA/CLK signals **must be enforced during PCB layout and signal-integrity analysis**, regardless of schematic topology.

This requirement will be addressed in:
- Stage 8 — Validation & Bring-Up Strategy
- Stage 10 — Layout SI/PI Guidelines

---

## Implementation Guidance for Stage 7.2

- Each CA/CLK signal is drawn as a **single named net**
- The net connects to:
  - Host connector CA/CLK pin
  - Corresponding pins on all DRAM devices
- No daisy-chain wiring is drawn in the schematic
- No termination networks are placed at this stage

---

## Lock Statement

This decision is **locked** for OMI v1.

Any change to CA/CLK topology representation must:
- Open a new design decision record
- Clearly justify the educational and architectural impact

---

*End of decision document*
