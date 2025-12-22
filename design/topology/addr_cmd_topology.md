# Address and Command Topology

This document defines the **topology used for address and command signals** in the OMI v1 DIMM design.

It explains:

- Which topology is chosen
- Why it is chosen
- What constraints this topology imposes
- What problems it avoids

This document does not define routing geometry, termination values, or timing numbers.

---

## Purpose of Address and Command Topology

Address and command signals form the **control plane** of the memory system.

Their topology must ensure:

- All DRAM devices interpret commands correctly
- Timing relationships are predictable
- Reflections and signal distortion are controlled
- Setup and hold margins are preserved under worst-case conditions

Errors in this signal group cause **immediate and catastrophic failure**.

---

## Topology Options Considered

At a high level, address and command signals could be structured as:

1. Multi-drop with stubs
2. Point-to-point with replication
3. Fly-by routing

Each option has different electrical and timing implications.

---

## Chosen Topology: Fly-By Routing

For OMI v1, **fly-by topology** is chosen for address and command signals.

In fly-by topology:

- Signals originate at the memory controller
- They pass sequentially by each DRAM device
- Each device taps the signal in order
- Termination is placed at the far end of the line

This topology is widely used in modern DDR systems.

---

## Why Fly-By Is the Correct Choice

Fly-by routing is chosen because it:

- Minimizes stubs and branch lengths
- Reduces reflection magnitude
- Enables higher signal speeds
- Produces predictable, monotonic signal arrival
- Aligns with DDR protocol expectations

Compared to multi-drop topologies, fly-by significantly improves signal integrity.

---

## Managed Skew as a Feature, Not a Bug

In fly-by routing:

- Each DRAM device sees the signal at a slightly different time
- This introduces deterministic skew along the chain

This skew is:

- Predictable
- Calibratable
- Accounted for by the memory controller

The DDR protocol explicitly supports this behavior.

---

## Relationship to Clock Distribution

Address and command signals are sampled relative to the clock.

In OMI v1:

- Clock signals are distributed consistently with address/command signals
- Topology choices are coordinated to preserve relative timing

This coordination ensures that:

- Setup and hold margins are maintained
- No device samples commands prematurely or too late

---

## Termination Strategy (Conceptual)

Fly-by topology requires termination at the **end of the line**.

Conceptually:

- Termination absorbs remaining signal energy
- Prevents reflections from returning upstream
- Stabilizes voltage levels for all receivers

Exact termination implementation is defined in later documents.

---

## What This Topology Protects Against

Fly-by routing reduces or avoids:

- Large stubs
- Strong reflections
- Multiple reflection paths
- Unpredictable ringing
- Data-pattern-dependent command errors

These failure modes are common in poorly designed multi-drop buses.

---

## What This Topology Does NOT Solve

Fly-by routing does not eliminate:

- Skew (it manages it)
- Noise coupling
- Power integrity issues

These are addressed through:

- Matching constraints
- Power architecture
- Careful layout

Topology is necessary but not sufficient.

---

## Constraints Imposed by This Topology

Choosing fly-by topology implies:

- Ordered device placement
- Consistent signal direction
- Explicit consideration of arrival order
- Coordinated termination placement

These constraints are intentional and beneficial.

---

## Design Intent for OMI v1

For OMI v1:

- Fly-by routing is used for all address and command signals
- No alternative topologies are supported
- Conservative assumptions are applied
- Alignment with industry-standard DDR practices is maintained

This choice prioritizes correctness, clarity, and reproducibility.

---

## What This Document Does NOT Decide

This document does not define:

- Physical routing paths
- Trace impedance values
- Exact termination resistor values
- Length matching limits
- Device ordering on the PCB

Those decisions belong to later stages.

---

## Takeaway

Address and command signals require:

- Shared visibility
- Predictable timing
- Controlled reflections

Fly-by topology provides these properties reliably.

For OMI v1, fly-by routing is not an optimization.
It is a correctness requirement.

---

Next documents in this directory:
- `data_topology.md`
- `clock_topology.md`
