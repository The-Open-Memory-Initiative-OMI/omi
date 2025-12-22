# Power Block

This document defines the **power block** for the OMI v1 DIMM design.

It describes:
- How power enters the DIMM
- How power rails are separated and distributed
- How power interfaces with functional blocks
- How power integrity intent is preserved during implementation

This document is block-level only.
It does not define regulators, capacitor values, or PCB placement.

---

## Purpose of the Power Block

The power block represents the **electrical foundation** of the DIMM.

Its purpose is to:
- Translate power architecture decisions into implementation structure
- Preserve power domain separation
- Prevent accidental rail mixing
- Make power integrity reviewable at schematic level

All other blocks depend on this block behaving correctly.

---

## Power Entry Interface

Power enters the DIMM through the **connector interface**.

At the block level:
- Power entry is treated as an external dependency
- No assumptions are made about upstream regulation quality
- Each rail is treated independently from entry onward

The power block does not generate rails.
It distributes and conditions them.

---

## Defined Power Rails

The power block manages the following distinct rails:

- **VDD** — DRAM core supply
- **VDDQ** — I/O supply
- **Vref** — reference voltage
- **VTT** — termination supply
- **Auxiliary / Standby** — low-speed logic power

Each rail is treated as a separate domain.

---

## Rail Separation and Domain Boundaries

Within the power block:
- Rails are never merged
- Rails are never repurposed
- Rails serve only their defined function

Domain separation is enforced structurally so that:
- Noise does not propagate unintentionally
- Decoupling strategies remain effective
- Signal integrity assumptions remain valid

Any violation of domain separation is a design error.

---

## Distribution to Functional Blocks

The power block exposes **clean, well-defined interfaces** to:

- DRAM array block
- SPD and auxiliary logic block

Each interface:
- Explicitly names the rail being delivered
- Preserves domain separation
- Makes power dependencies visible in schematics

No block is allowed to infer power implicitly.

---

## Relationship to the DRAM Array Block

The DRAM array block consumes:

- VDD for internal operation
- VDDQ for I/O signaling
- Vref for signal comparison
- VTT for termination behavior

The power block ensures:
- Each rail arrives independently
- Each rail can be decoupled appropriately
- Each rail can be reviewed independently

This structure prevents accidental coupling.

---

## Vref Handling (Conceptual)

Within the power block:
- Vref is treated as a **reference**, not a supply
- It is isolated from high-current paths
- It is protected from switching noise

Vref never powers logic.
It only defines thresholds.

---

## VTT Handling (Conceptual)

Within the power block:
- VTT is treated as a **dynamic bias rail**
- It is expected to source and sink current
- It is tightly coupled to signal termination behavior

VTT stability is critical for command and address integrity.

---

## Auxiliary and Standby Power

Auxiliary power supports:
- SPD EEPROM
- Configuration logic
- Low-speed interfaces

These loads:
- Are electrically isolated from high-speed domains
- Must remain stable during standby states
- Must not inject noise into DRAM rails

The power block enforces this isolation.

---

## Decoupling Responsibility Boundary

The power block:
- Defines **where** decoupling responsibility lies
- Exposes rails that require decoupling
- Does not implement decoupling itself

Decoupling strategy is defined in a separate document
and implemented across block boundaries.

This separation prevents confusion between architecture and layout.

---

## What This Block Explicitly Enforces

The power block enforces:

- Explicit rail naming
- Explicit rail boundaries
- Explicit power consumers
- Reviewable power paths

No rail may appear implicitly or accidentally.

---

## What This Block Does NOT Decide

This document does not define:
- Voltage levels
- Regulator topology
- Capacitor values
- Placement rules
- Thermal behavior

Those belong to later implementation and validation stages.

---

## Relationship to Stage 5 Decisions

This block directly implements:

- Power rail architecture
- Domain separation principles
- Decoupling intent
- Design assumptions

No new power behavior is introduced here.

---

## Takeaway

The power block ensures that power integrity intent survives implementation.

It makes power:
- Explicit
- Reviewable
- Isolated
- Predictable

Without this block, power integrity failures become invisible until too late.

---

Next block-level document:
- `spd_and_aux_block.md`
