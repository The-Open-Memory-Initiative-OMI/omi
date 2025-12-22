# DRAM Array Block

This document defines the **DRAM array block** for the OMI v1 DIMM design.

It describes:
- How DRAM devices are grouped
- How byte lanes are represented structurally
- How address, data, clock, and power interfaces enter the block
- How architectural topology decisions appear in implementation form

This document is block-level only.
It does not define pins, part numbers, or routing.

---

## Purpose of the DRAM Array Block

The DRAM array block represents **all memory storage devices on the DIMM** as a structured system.

Its purpose is to:
- Translate abstract signal groups into physical groupings
- Preserve topology and constraint intent
- Provide a clear schematic partition boundary

This block is the heart of the DIMM.

---

## High-Level Block View

Conceptually, the DRAM array block consists of:

- One or more **ranks**
- Each rank containing multiple **DRAM devices**
- Devices organized into **byte lanes**
- Shared control and clock interfaces
- Dedicated data and strobe interfaces per lane

The block is internally structured but externally well-defined.

---

## Rank Structure

A **rank** represents a group of DRAM devices that:
- Share address and command signals
- Share clock signals
- Respond to a common chip select
- Operate synchronously as a logical memory unit

OMI v1 supports:
- A conservative rank structure
- Clear rank boundaries
- No rank-level optimization tricks

Ranks are treated as independent logical blocks.

---

## DRAM Device Grouping

Within a rank:
- DRAM devices are grouped by **byte lane**
- Each device contributes a portion of the total data width
- Devices operate in lockstep under shared control signals

This grouping reflects:
- Data topology decisions (point-to-point)
- Length matching constraints
- Training and calibration behavior

Devices are not treated as interchangeable black boxes.

---

## Byte Lane Sub-Blocks

Each byte lane is represented as a **sub-block** within the DRAM array.

A byte lane sub-block includes:
- One group of DQ signals
- One associated DQS (and complement, if applicable)
- One DRAM device or device slice

Key properties:
- Byte lanes are independent timing domains
- Each lane has its own data/strobe interface
- Lanes share control and clock interfaces

This structure directly supports DDR training mechanisms.

---

## Address and Command Interface

The DRAM array block exposes a single **address and command interface** per rank.

Characteristics:
- Shared across all devices in the rank
- Unidirectional (controller → DRAM)
- Internally fanned out to each device

This interface reflects the **fly-by topology** chosen in Stage 5.

Ordering and physical routing are handled later.

---

## Clock Interface

The DRAM array block exposes a shared **differential clock interface**.

Characteristics:
- Driven externally by the memory controller
- Distributed internally to all devices
- Used as the global timing reference

Clock signals are not modified or regenerated within the block.

---

## Data and Strobe Interfaces

Each byte lane exposes:
- A dedicated DQ interface
- A dedicated DQS interface

Characteristics:
- Point-to-point connectivity
- Bidirectional operation
- Independent timing alignment

These interfaces preserve the **point-to-point data topology**.

---

## Power Interfaces

The DRAM array block consumes the following power rails:

- **VDD** — core DRAM operation
- **VDDQ** — I/O signaling
- **Vref** — signal reference
- **VTT** — termination bias

Power enters the block as **distinct domains**, not as a single supply.

Decoupling and regulation are handled outside the block boundary.

---

## Reset and Control Interface

The block includes:
- Reset and initialization inputs
- Global control signals required for bring-up

These signals:
- Are shared across devices
- Are low-speed relative to data
- Define operational state

They are conceptually grouped with control interfaces.

---

## What This Block Explicitly Enforces

This block structure enforces:

- Separation of control and data planes
- Byte-lane–based data organization
- Shared control, shared clock, isolated data
- Clear power domain boundaries

These properties are **not optional** in later stages.

---

## What This Block Does NOT Decide

This document does not define:
- Number of ranks
- Number of byte lanes
- Specific DRAM part selection
- Pin numbers or symbols
- PCB placement or routing

Those are resolved in later implementation steps.

---

## Relationship to Stage 5 Decisions

This block directly reflects:

- Signal map definitions
- Topology decisions
- Length matching intent
- Power rail architecture
- Design assumptions

No new architectural behavior is introduced here.

---

## Takeaway

The DRAM array block turns architecture into structure.

It ensures that:
- Data topology remains point-to-point
- Control remains shared and ordered
- Power domains remain explicit
- Timing intent survives schematic capture

If implemented correctly, this block makes it *hard* to build a broken DIMM.

---

Next block-level documents:
- `power_block.md`
- `spd_and_aux_block.md`
