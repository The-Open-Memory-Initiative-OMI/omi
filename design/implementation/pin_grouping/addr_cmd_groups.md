# Address and Command Pin Grouping

This document defines the **logical pin grouping** for address and command signals in the OMI v1 DIMM design.

It specifies:
- How address/command nets are grouped into schematic-friendly bundles
- Naming conventions for rank-related signals
- Which signals are treated as shared buses vs rank-specific lines
- How these groups map to internal blocks and interfaces

This document does not define exact pin numbers or connector mapping.
It provides a stable grouping scheme for schematic capture and review.

---

## Purpose of Pin Grouping

Pin grouping exists to:
- Reduce ambiguity in schematics
- Make signal intent visible at a glance
- Prevent accidental mixing of unrelated nets
- Support consistent connector and device symbol design

Grouping is not topology.
Grouping is how we represent the topology safely in implementation artifacts.

---

## High-Level Group Structure

Address and command signals are represented as:

1. **Global Address Bus**
2. **Global Command/Control Group**
3. **Rank Select Group**
4. **Optional/Reserved Control Group (if applicable)**

These groups are driven by the host memory controller and received by all DRAM devices.

---

## 1. Global Address Bus

### Description
The address bus represents the set of address bits used to encode:
- row/column selection
- bank and bank group selection (generation-dependent)

### Grouping Rule
All address bits are grouped as a single bundle:

- `A[ ]` for address bits

### Notes
- The exact width of `A[ ]` is defined by the chosen DDR generation and DRAM density.
- The schematic must preserve the bus structure rather than listing bits as unrelated nets.

### Block Mapping
- External: DIMM connector → Address bus
- Internal: Address bus → DRAM array block (distributed to all devices per fly-by topology)

---

## 2. Global Command and Control Group

### Description
This group encodes DDR commands and global control intent.

### Grouping Rule
Command/control signals are grouped as a named bundle:

- `CMD_*` and `CTRL_*` lines

Examples (conceptual naming only):
- `CMD_*` for command-encoding lines
- `CTRL_*` for global control lines that are sampled with commands

### Notes
- Exact signal names depend on DDR generation, but grouping remains stable.
- These signals are shared across all devices in a rank.

### Block Mapping
- External: DIMM connector → Command/control group
- Internal: Command/control group → DRAM array block (distributed per fly-by topology)

---

## 3. Rank Select Group

### Description
Rank select lines determine which rank responds to shared commands.

### Grouping Rule
Rank select signals are grouped per rank:

- `CS_n[rank]` (chip select per rank)

If the design supports multiple ranks, these are represented explicitly as:
- `CS_n0`, `CS_n1`, ... (or equivalent rank-indexed naming)

### Notes
- Rank select signals are not part of the generic command encoding; they gate it.
- Rank selection must be kept visually separate in schematics to avoid confusion.

### Block Mapping
- External: DIMM connector → Rank select lines
- Internal: Rank select → DRAM array block, per-rank boundary

---

## 4. Reset and Initialization Controls (Boundary Note)

Reset/control signals are grouped with clock/control in a separate document.
However, address/command logic must treat them as global inputs.

This document assumes:
- Reset-related lines are not part of the address/command bundle
- They are represented and reviewed separately

---

## Shared vs Rank-Specific: Explicit Rule

- `A[ ]`, `CMD_*`, and `CTRL_*` are **shared** across all ranks (electrically distributed)
- `CS_n[rank]` is **rank-specific**
- Any signal that gates command acceptance must be rank-identified if multiple ranks exist

This rule prevents accidental shorting of rank select behavior.

---

## Schematic Representation Rules

To keep schematics reviewable:

- Use bus notation for `A[ ]`
- Use clearly named bundles for command/control
- Place rank select lines adjacent to the DRAM rank blocks they control
- Avoid listing address bits as unrelated single nets
- Avoid mixing command/control signals into the data plane symbols

The schematic should show intent, not just connectivity.

---

## Consistency and Naming Conventions

The design uses:
- Uppercase functional prefixes (`A`, `CMD_`, `CTRL_`, `CS_`)
- Explicit rank indices where needed
- No vendor-specific naming

Consistency is required for:
- documentation review
- future pin assignment
- contributor collaboration

---

## Relationship to Topology

This grouping must remain consistent with Stage 5 topology decisions:

- Address/command distributed as a shared bus (fly-by topology)
- Rank select lines gating shared commands
- No ad hoc replication of command signals per device

Grouping does not override topology.
Grouping expresses topology safely.

---

## What This Document Does NOT Decide

This document does not define:
- Exact bus widths
- Exact DDR-generation signal names
- Connector pin assignments
- Length matching values
- Termination implementation

Those are handled elsewhere.

---

## Takeaway

Address and command pins are grouped to make the control plane explicit:

- One shared address bus
- One shared command/control bundle
- Explicit rank select lines

This grouping prevents schematic ambiguity and preserves architectural intent.

---

Next pin grouping documents:
- `data_byte_lanes.md`
- `clock_and_control.md`
