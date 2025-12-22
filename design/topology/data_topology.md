# Data Topology

This document defines the **topology used for data (DQ) and data strobe (DQS) signals** in the OMI v1 DIMM design.

It explains:

- Which topology is chosen
- Why it is chosen
- What constraints it imposes
- What failure modes it prevents

This document does not define routing geometry, impedance values, or timing numbers.

---

## Why Data Topology Is Special

Data signals are the **most fragile signals** on the DIMM.

They are:

- Bidirectional
- Sampled at very high speeds
- Dependent on tight timing alignment
- Sensitive to noise, skew, and reflections

Unlike address and command signals, **data errors do not usually crash the system**.
They silently corrupt information.

This makes data topology a correctness decision, not a performance one.

---

## Topology Options Considered

At a high level, data signals could be structured as:

1. Multi-drop shared buses
2. Fly-by routing
3. Point-to-point connections

Each option has radically different implications for signal integrity and timing.

---

## Chosen Topology: Point-to-Point per Byte Lane

For OMI v1, **data and strobe signals use point-to-point topology**, organized by byte lane.

This means:

- Each data byte lane connects the controller to one DRAM device group
- No stubs or branches exist on DQ or DQS lines
- Each lane has a dedicated timing relationship

This is the only topology that reliably supports DDR data rates.

---

## Why Point-to-Point Is Mandatory for Data

Point-to-point topology is chosen because it:

- Eliminates stubs entirely
- Minimizes reflections
- Simplifies termination
- Preserves eye opening
- Enables precise DQS-based sampling

Any form of multi-drop data topology:

- Creates unavoidable reflections
- Complicates bidirectional turnaround
- Shrinks timing margins beyond recovery

For data signals, **sharing is not acceptable**.

---

## Relationship Between DQ and DQS

Each byte lane consists of:

- A group of DQ signals
- One associated DQS (and its complement, if applicable)

In OMI v1:

- DQ and DQS for a lane follow the same topology
- They share the same physical path characteristics
- Their relative delay is tightly controlled

This pairing is fundamental to DDR operation.

---

## Bidirectional Nature and Turnaround

Data signals change direction dynamically:

- During WRITE:
  - Controller drives DQ and DQS
  - DRAM samples relative to DQS

- During READ:
  - DRAM drives DQ and DQS
  - Controller samples relative to DQS

Point-to-point topology ensures:

- Clean direction changes
- Predictable impedance environment
- Stable termination behavior

Without this, turnaround errors dominate.

---

## Termination Strategy (Conceptual)

Data termination depends on direction:

- When the controller drives data:
  - Termination is effective at the DRAM end

- When the DRAM drives data:
  - Termination is effective at the controller end

Point-to-point topology allows:

- Dynamic termination
- On-die termination (ODT)
- Predictable energy absorption

Shared topologies break this symmetry.

---

## Byte Lane Independence

Each byte lane is treated as an independent timing domain.

This allows:

- Lane-by-lane calibration
- Compensation for placement differences
- Scalable data width

However, this also means:

- Lane-to-lane skew must be controlled
- Power and noise coupling must be managed system-wide

Independence improves timing, not isolation.

---

## What This Topology Protects Against

Point-to-point data topology prevents:

- Stub reflections
- Mid-burst ringing
- Data-pattern-dependent corruption
- Unstable turnaround behavior
- Eye collapse under load

These are the dominant causes of silent memory errors.

---

## What This Topology Does NOT Solve

Point-to-point topology does not eliminate:

- Crosstalk
- Power integrity issues
- Poor reference routing
- Excessive skew due to layout

Those are handled by:

- Constraints
- Power architecture
- Careful PCB design

Topology provides the foundation, not the full solution.

---

## Design Intent for OMI v1

For OMI v1:

- All DQ and DQS signals use point-to-point topology
- Data is organized strictly by byte lane
- No data bus sharing is permitted
- Conservative, standards-aligned assumptions are used

This prioritizes correctness, simplicity, and reproducibility.

---

## What This Document Does NOT Decide

This document does not define:

- Number of byte lanes
- Data width
- Trace lengths or matching values
- Impedance targets
- Specific termination mechanisms

Those are defined in later design documents.

---

## Takeaway

Data signals carry truth.
Truth cannot tolerate ambiguity.

Point-to-point topology gives data:

- A clean path
- A predictable environment
- Preserved timing margins

For OMI v1, this topology is not optional.
It is required.

---

Next documents in this directory:
- `clock_topology.md`
