# Clock and Control Pin Grouping

This document defines the **logical pin grouping** for clock and global control signals in the OMI v1 DIMM design.

It specifies:
- How clock signals are grouped and represented
- How reset and global control signals are grouped
- How these groups are kept distinct from data and command planes
- How grouping preserves timing and control intent

This document does not define exact pin numbers, electrical values, or connector assignments.
It provides a stable grouping scheme for schematic capture and review.

---

## Purpose of Clock and Control Grouping

Clock and control signals:
- Define global timing
- Define global state
- Affect every DRAM device simultaneously

Grouping exists to:
- Make global signals visually and structurally distinct
- Prevent accidental mixing with data or command planes
- Preserve timing and control intent through implementation

Mistakes here are system-wide and catastrophic.

---

## High-Level Group Structure

Clock and control signals are grouped into:

1. **Global Clock Group**
2. **Global Reset Group**
3. **Global Control Group**

These groups are shared across all ranks and devices.

---

## 1. Global Clock Group

### Description

The global clock group provides the primary timing reference for DDR operation.

### Grouping Rule

Clock signals are grouped as a differential pair bundle:

- `CK` and `CK_n` (conceptual naming)

Rules:
- Clock signals are always represented as a differential pair
- The pair is never split across symbols or sheets
- Clock signals are never bundled with non-clock signals

---

### Scope and Sharing

- Driven by the host memory controller
- Received by all DRAM devices
- Shared across all ranks

Clock signals are global by definition.

---

### Schematic Representation Rules

- Place clock pairs prominently and consistently
- Keep clock grouping visually separate from address/command
- Do not interleave clock pins with data lane pins

Clock grouping must make global timing obvious at a glance.

---

## 2. Global Reset Group

### Description

Reset signals place DRAM devices into a known, valid state during bring-up.

### Grouping Rule

Reset-related signals are grouped as:

- `RESET_*` (conceptual naming)

Rules:
- Reset signals are grouped together
- They are not mixed with command encoding signals
- They are not lane-scoped

---

### Scope and Behavior

- Driven by the host or system logic
- Observed by all DRAM devices
- Change infrequently
- Not timing-critical during normal operation

Despite low speed, reset signals must be unambiguous.

---

## 3. Global Control Group

### Description

Global control signals influence DRAM behavior but are not part of the command encoding itself.

Examples include:
- Clock enable–type signals
- Mode-related global controls
- Power or operational state indicators

(The exact signal set is DDR-generation dependent.)

---

### Grouping Rule

Global control signals are grouped as:

- `CTRL_GLOBAL_*` (conceptual naming)

Rules:
- Control signals are grouped separately from command encoding
- They are shared across all devices
- They are visually distinct from data and strobe signals

---

## Separation from Address and Command Groups

Although some control signals are sampled synchronously with commands:

- They are not encoded as part of the command bus
- They must remain visually and structurally distinct
- Their grouping reflects their global scope

This separation prevents command/control ambiguity.

---

## Relationship to Data and Byte Lanes

Clock and control signals:
- Are not lane-indexed
- Are not replicated per lane
- Must never appear inside byte lane symbols

They form the **global timing and state plane**, not the data plane.

---

## Relationship to Topology Decisions

This grouping preserves Stage 5 topology intent:

- Shared clock topology
- Shared reset and control behavior
- Global distribution coordinated with address/command fly-by

Grouping expresses topology safely at the schematic level.

---

## Naming and Consistency Rules

The design uses:
- Clear functional prefixes (`CK`, `RESET_`, `CTRL_`)
- No lane indices
- No rank indices

If a signal affects all devices, it must look global.

---

## What This Document Does NOT Decide

This document does not define:
- Exact signal list per DDR generation
- Electrical characteristics
- Termination strategy
- Pin counts or pin numbers
- Connector layout

Those are handled in later stages.

---

## Takeaway

Clock and control signals define **when** and **how** memory operates.

By grouping them explicitly and globally:
- Timing intent is preserved
- State control is unambiguous
- Implementation mistakes are harder to make

If byte lanes are the truth plane,
clock and control are the laws of physics.

---

This completes the pin grouping definitions for Stage 6.
