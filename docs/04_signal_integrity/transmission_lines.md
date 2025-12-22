# Transmission Lines: When Wires Stop Behaving Like Wires

This document explains **what a transmission line is**, when a PCB trace must be treated as one, and why this matters critically for DDR memory systems.

Most signal integrity problems begin with misunderstanding this single concept.

---

## The Dangerous Assumption: "It's Just a Wire"

At low speeds, it is reasonable to think of a PCB trace as:

- An ideal wire
- Zero delay
- Instantaneous voltage change

At DDR speeds, this assumption is **false**.

A PCB trace behaves as a **distributed electrical system**, not a lumped connection.

This change in behavior is the root cause of:

- Reflections
- Ringing
- Skew
- Timing collapse

---

## When a Trace Becomes a Transmission Line

A trace must be treated as a transmission line when:

> The signal's rise time is comparable to, or faster than, the signal's propagation delay along the trace.

This condition is **always true for DDR**.

---

## Propagation Delay: Signals Are Not Instantaneous

Electrical signals propagate at a finite speed.

On a PCB:

- Signals travel at roughly **half to two-thirds the speed of light**
- This corresponds to approximately **150–180 ps per centimeter**, depending on the stack-up

This means:

- A few centimeters of trace introduce hundreds of picoseconds of delay
- At DDR speeds, this is a significant fraction of the timing budget

The signal exists **simultaneously at different points with different voltages**.

---

## Distributed Behavior: Resistance, Capacitance, Inductance

A transmission line is not a single component.

It is a continuous distribution of:

- Resistance (R)
- Capacitance (C)
- Inductance (L)
- Conductance (G, often negligible for PCB traces)

Each infinitesimal segment contributes to the signal's behavior.

This is why:

- The entire trace matters
- Local changes affect global behavior
- Geometry is electrical design

---

## Characteristic Impedance

A transmission line has a property called **characteristic impedance (Z₀)**.

Key points:

- Z₀ is determined by trace geometry and dielectric properties
- Z₀ is **not** the same as DC resistance
- Z₀ exists even if the trace is infinitely long

Typical DDR traces are designed for:

- Controlled, known impedance
- Predictable behavior when driven and terminated

If impedance is uncontrolled, signal behavior becomes unpredictable.

---

## What Happens When a Signal Is Launched

When a driver switches:

- It launches a voltage wave into the transmission line
- The wave travels down the trace toward the receiver
- The receiver does not "see" the source directly
- It sees the wave arriving after propagation delay

Until the wave reaches the receiver, the far end knows nothing has changed.

This is a fundamental shift from low-speed thinking.

---

## The Receiver Does Not See the Whole Trace at Once

At any moment:

- Different points on the trace have different voltages
- The signal edge occupies physical space
- The transition is moving, not global

This is why:

- Reflections occur
- Termination matters
- Length matching matters

The signal is a **traveling wave**, not a static level.

---

## Why Reflections Exist (Preview)

If a traveling wave encounters a change in impedance:

- Part of the wave continues forward
- Part of the wave reflects backward

Reflections are not noise.
They are **energy conservation in action**.

We will analyze this deeply in the next document.

---

## Why Transmission Line Effects Break Timing

DDR timing assumes:

- Signals arrive within defined windows
- Setup and hold times are respected
- Voltage thresholds are crossed cleanly

Transmission line effects:

- Distort edges
- Delay arrivals
- Create ringing
- Introduce uncertainty

These effects **directly reduce timing margins**.

---

## Why Short Traces Are Not "Safe"

A common myth:

> "My trace is short, so I don't need to worry."

This fails because:

- Rise times are extremely fast
- Even short traces have non-negligible delay
- DDR margins are very small

If rise time < 2 × propagation delay, transmission line behavior dominates.

For DDR, this condition is always met.

---

## Return Paths Matter

A transmission line is not just the signal trace.

It includes:

- The return current path
- Reference planes
- Via transitions

If the return path is disrupted:

- Inductance increases
- Effective impedance changes
- Signal integrity degrades

Signal and return must be treated as a pair.

---

## Implications for DIMM Design

On a DIMM:

- Trace length directly affects timing
- Trace geometry affects impedance
- Layer changes affect return paths
- Every routing decision affects signal behavior

Transmission line effects cannot be fixed in firmware.
They must be designed correctly.

---

## Why OMI Starts Signal Integrity Here

OMI starts signal integrity with transmission lines because:

- All other SI concepts depend on this
- Reflections, crosstalk, and skew all originate here
- Without this model, rules feel arbitrary

Understanding transmission lines turns:

- Layout rules into reasoning
- Constraints into engineering
- "Black magic" into physics

---

## Takeaway

At DDR speeds:

- A trace is not a wire
- A signal is not instantaneous
- Geometry is timing
- Physics enforces correctness

Transmission lines are the language DDR speaks.

OMI exists to teach that language openly.

---

Next documents in this stage:
- `reflections_and_matching.md`
