# Clock Topology

This document defines the **topology used for clock signals** in the OMI v1 DIMM design.

It explains:

- How clock signals are distributed
- Why this topology is chosen
- How it interacts with address/command and data signals
- What constraints it imposes on the design

This document remains architectural and does not specify routing geometry, skew numbers, or electrical values.

---

## Role of the Clock in DDR Systems

The clock defines the **global timing reference** for the memory system.

It is used to:

- Sample address and command signals
- Establish phase relationships for data strobes (DQS)
- Anchor timing calibration and training
- Define valid timing windows for all synchronous operations

If the clock is unstable or poorly distributed, **no other signal group can be correct**.

---

## Clock Topology Requirements

A valid clock topology must ensure:

- Predictable arrival times at all DRAM devices
- Minimal skew between receivers
- High noise immunity
- Stable reference behavior under load and temperature variation

Unlike data signals, clock errors affect **every operation simultaneously**.

---

## Topology Options Considered

Conceptually, clock distribution could be implemented as:

1. Point-to-point replication
2. Multi-drop with stubs
3. Fly-by-style distribution

Each option has different implications for skew, reflections, and complexity.

---

## Chosen Topology: Shared Differential Distribution

For OMI v1, clock signals use a **shared, differential distribution topology**, coordinated with the address and command fly-by structure.

Key characteristics:

- Clock signals are driven only by the memory controller
- All DRAM devices receive the same clock
- Distribution is monotonic and ordered
- Differential signaling is used for noise immunity

This aligns with standard DDR practices.

---

## Why a Shared Clock Is Required

A shared clock is required because:

- Address and command signals are shared
- Command interpretation must be globally consistent
- Timing calibration assumes a common reference

Independent or replicated clocks would:

- Complicate timing relationships
- Break controller assumptions
- Increase calibration complexity

Consistency is more important than symmetry.

---

## Differential Signaling and Noise Immunity

Clock signals are differential to:

- Reject common-mode noise
- Reduce sensitivity to ground bounce
- Preserve edge integrity at high speeds

Differential clocks:

- Are less affected by crosstalk
- Maintain cleaner timing edges
- Improve jitter performance

Clock quality directly defines timing margin quality.

---

## Relationship to Address and Command Signals

Clock topology is coordinated with address/command topology:

- Both are shared
- Both are unidirectional
- Both are sampled synchronously

This coordination ensures that:

- Relative timing is predictable
- Setup and hold margins are preserved
- Fly-by skew is consistent and manageable

Clock and command signals must be considered together.

---

## Relationship to Data and Strobes

Data sampling relies on DQS, not directly on the global clock.

However:

- DQS phase is trained relative to the clock
- Clock stability affects DQS alignment
- Clock jitter propagates into data timing uncertainty

Thus, even though data is strobe-based, **clock integrity still matters**.

---

## Termination Strategy (Conceptual)

Clock topology requires:

- Controlled impedance
- Proper termination
- Minimal reflection paths

Termination strategy is designed to:

- Absorb energy cleanly
- Prevent ringing
- Preserve edge shape

Exact termination details are defined later.

---

## What This Topology Protects Against

The chosen clock topology protects against:

- Excessive skew between devices
- Common-mode noise sensitivity
- Jitter amplification
- Inconsistent command sampling

These failures are global and catastrophic.

---

## What This Topology Does NOT Solve

Clock topology does not eliminate:

- Crosstalk from adjacent signals
- Power-induced jitter
- Poor reference plane design

Those are addressed through:

- Signal integrity constraints
- Power architecture
- PCB stack-up decisions

Topology defines structure, not perfection.

---

## Design Intent for OMI v1

For OMI v1:

- Clock signals are shared and differential
- Distribution is coordinated with address/command topology
- Conservative, standards-aligned assumptions are used
- No custom clock conditioning is introduced on the DIMM

This prioritizes clarity, correctness, and reproducibility.

---

## What This Document Does NOT Decide

This document does not define:

- Clock frequency
- Phase offsets
- Skew budgets
- Routing geometry
- Termination component values

Those belong in later constraint and implementation stages.

---

## Takeaway

The clock is the spine of the memory system.

It must be:

- Shared
- Stable
- Predictable
- Quiet

A correct clock topology makes all other timing relationships possible.

For OMI v1, this topology is fixed deliberately and conservatively.

---

This completes the topology decisions for OMI v1.
