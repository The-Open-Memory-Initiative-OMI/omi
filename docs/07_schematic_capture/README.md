# Stage 7 — Schematic Capture Guide

Stage 7 defines **how schematics must be captured** for the OMI v1 DIMM design.

This guide exists to ensure that:
- Architectural intent is preserved during schematic capture
- Constraints remain visible and enforceable
- Reviews can detect errors early
- No schematic decision silently redefines the design

This stage is about *how to draw*, not *what to invent*.

---

## What Stage 7 Is

Stage 7 is a **process and discipline guide**.

It explains:
- How to structure schematic sheets
- How to represent blocks and interfaces
- How to express topology and constraints visually
- How to avoid common schematic-level failures

Stage 7 assumes all architectural decisions are already complete.

---

## What Stage 7 Is NOT

Stage 7 does **not** include:
- Component selection
- Value tuning
- Electrical optimization
- Layout guidance
- Performance enhancement

If a decision affects architecture, it belongs in Stage 5 — not here.

---

## Golden Rule of Schematic Capture

> **A schematic must make incorrect implementations visually uncomfortable.**

If a reviewer can't *see* that something is wrong,
the schematic is not good enough.

---

## Recommended Schematic Sheet Structure

Schematics should be split into **functional sheets**, not convenience sheets.

Recommended structure:



01_dimm_connector.sch
02_power_distribution.sch
03_dram_array_overview.sch
04_byte_lane_0.sch
05_byte_lane_1.sch
...
NN_spd_and_aux.sch


Each sheet must have a clear ownership boundary.

---

## Sheet 1 — DIMM Connector

**Purpose:**
- Represent the system boundary
- Show signal grouping explicitly

Rules:
- No DRAM devices on this sheet
- No decoupling on this sheet
- Signals must be grouped exactly as defined in Stage 6
- Buses must be used for address and data groups

This sheet defines the contract with the host system.

---

## Sheet 2 — Power Distribution

**Purpose:**
- Make power domains explicit
- Prevent rail mixing

Rules:
- One rail = one named net
- No implicit power pins
- VDD, VDDQ, Vref, VTT, and auxiliary rails must be separate
- Decoupling placeholders must be visible per rail

If power domains are unclear here, the schematic is invalid.

---

## Sheet 3 — DRAM Array Overview

**Purpose:**
- Show rank structure
- Show byte-lane partitioning
- Show shared vs point-to-point intent

Rules:
- No pin-level detail
- Byte lanes must appear as distinct blocks
- Address/command and clock must appear shared
- Data must appear lane-isolated

This sheet is the architectural sanity check.

---

## Byte Lane Sheets (One per Lane)

**Purpose:**
- Capture the most timing-critical interfaces correctly

Rules:
- One byte lane per sheet
- Only one DQ group and one DQS group per sheet
- No cross-lane signals allowed
- DQS must be adjacent to its DQ group
- Power pins must reference explicit rails

If two lanes touch on a sheet, it is a violation.

---

## SPD and Auxiliary Sheet

**Purpose:**
- Support configuration and discovery
- Remain isolated from high-speed domains

Rules:
- Only auxiliary/standby power allowed
- No connection to VDD/VDDQ/Vref/VTT
- Low-speed bus only
- No DDR signals allowed

This sheet must remain boring — and that is good.

---

## Signal Representation Rules

### Buses and Bundles

- Address must be drawn as a bus
- DQ must be drawn as lane-indexed bundles
- Command and control must be grouped logically
- No exploding buses into single nets unless required

Bundles preserve intent.

---

### Naming Discipline

- Every net name must encode its role
- Lane index must be visible in every data-related net
- Rank index must be visible where applicable
- No ambiguous abbreviations

If a net name requires a legend, it is wrong.

---

## Power and Decoupling Representation

- Decoupling must be present but abstracted
- Show intent (bulk vs local vs HF) without values
- Decoupling must be rail-specific
- No "generic" decoupling symbols

Decoupling is part of correctness, not decoration.

---

## What to Avoid at All Costs

Do **not**:
- Combine multiple byte lanes on one sheet
- Hide power pins using implicit connections
- Merge power rails for convenience
- Rely on layout to "fix" schematic ambiguity
- Encode timing assumptions in comments only

If it's important, it must be structural.

---

## Review Checklist (Schematic-Level)

A schematic set is acceptable only if:

- Every byte lane is isolated and traceable
- DQS–DQ pairing is unambiguous
- Clock distribution is global and clear
- Power domains are explicit and separated
- No architectural assumptions are implicit

If a reviewer has to ask "what did you mean here?",
the schematic is not ready.

---

## Relationship to Layout

Schematic capture defines:
- What layout *must* respect
- What layout *cannot* reinterpret

Layout should only:
- Implement
- Optimize within constraints
- Never decide architecture

If layout needs to guess, schematic capture failed.

---

## Takeaway

Stage 7 is where architecture meets ink.

A good schematic:
- Makes the right thing obvious
- Makes the wrong thing difficult
- Protects intent under pressure

If Stage 5 defined truth,
and Stage 6 preserved it,
Stage 7 ensures it survives contact with humans.

---

Next Stage:
- Stage 8 — Reference Schematic (Minimal, Correctness-First)
- or Stage 8 — Validation & Review Playbook
