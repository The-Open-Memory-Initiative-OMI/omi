# Termination and Topology: Making High-Speed Signals Behave

This document explains **signal termination and routing topology on DDR DIMMs**, why they are required, and how incorrect choices lead to timing violations and silent data corruption.

At DDR speeds, signals do not behave like ideal digital wires.
They behave like **waves on transmission lines**.

---

## Why Termination and Topology Matter

DDR signals operate at:

- Very high edge rates
- Tight voltage margins
- Strict timing windows

At these speeds:

- Traces act as transmission lines
- Reflections are unavoidable without control
- Timing is affected by physical distance

Termination and topology exist to ensure that:

- Signals settle predictably
- Reflections are absorbed
- Receivers see stable logic levels

Without them, DDR does not fail loudly — it fails silently.

---

## Transmission Lines on a DIMM

A PCB trace becomes a transmission line when:

- Signal edge rise time is comparable to propagation delay
- Trace length is no longer negligible

On a DIMM:

- This condition is always true for DDR signals

As a result:

- Impedance must be controlled
- Reflections must be managed
- Signal paths must be intentional

---

## What Signal Reflections Do

When a signal encounters an impedance mismatch:

- Part of the signal reflects
- The reflected wave interferes with the original
- Voltage overshoot or undershoot occurs

Consequences include:

- Timing uncertainty
- False logic transitions
- Setup and hold violations

These effects worsen with:

- Longer traces
- Higher speeds
- Multiple loads

---

## The Purpose of Termination

Termination exists to:

- Match the impedance of the transmission line
- Absorb signal energy
- Prevent reflections from returning to the receiver

Proper termination ensures that:

- Signals settle quickly
- Voltage levels stabilize
- Timing margins are preserved

Termination is a **signal integrity requirement**, not an optimization.

---

## Types of Termination Used in DDR

DDR uses a combination of termination strategies.

### On-Die Termination (ODT)

- Implemented inside DRAM devices
- Dynamically enabled or disabled
- Absorbs reflections near the receiver

ODT reduces the need for external resistors but does not eliminate topology constraints.

---

### External Termination

- Implemented using resistors on the DIMM or motherboard
- Often tied to VTT
- Used primarily for command and address signals

External termination provides a stable reference and predictable behavior.

---

## Address and Command Topology: Fly-By Routing

Modern DDR DIMMs use **fly-by topology** for address and command signals.

In fly-by routing:

- Signals pass sequentially through each DRAM device
- Each device taps the line in order
- Termination is placed at the far end

### Why Fly-By Exists

Fly-by topology:

- Eliminates large stubs
- Reduces reflection magnitude
- Enables higher speeds

The cost is that:

- Each DRAM sees the signal at a slightly different time
- Controllers must compensate using timing calibration

---

## Data Topology: Point-to-Point

Data signals typically use **point-to-point topology**.

Reasons:

- Data timing margins are the tightest
- Bidirectional switching is frequent
- Burst transfers amplify errors

Each data byte lane:

- Has a direct path
- Is tightly length-matched
- Is carefully terminated

Data topology prioritizes timing precision over routing simplicity.

---

## Stubs: Small Lengths, Big Problems

A stub is a branch off the main signal path.

Even short stubs:

- Act as reflection sources
- Store and release energy
- Distort signal edges

In DDR:

- Stubs must be minimized or eliminated
- Fly-by topology exists largely to avoid them

Ignoring stubs is one of the most common DDR layout mistakes.

---

## Length Matching and Skew

Different trace lengths cause **skew**:

- Signals arrive at different times
- Timing windows shrink
- Margins collapse

On a DIMM:

- Address and command skew affects ACT and READ timing
- Data skew affects setup and hold at the receiver

Length matching is not about aesthetics.
It is about preserving correctness.

---

## Termination Voltage (VTT) Interaction

Termination is tied to VTT.

If VTT:

- Is noisy
- Is poorly decoupled
- Does not track correctly

Then:

- Termination effectiveness degrades
- Reflections worsen
- Signal thresholds shift

Termination and power integrity are inseparable.

---

## Why These Failures Are Hard to Debug

Topology and termination issues often:

- Appear only at high speed
- Depend on temperature
- Depend on access patterns
- Disappear when probed

This leads to:

- False attribution to software
- Platform-specific failures
- Fragile validation results

---

## Implications for OMI

OMI treats termination and topology as:

- Core design decisions
- Documented engineering trade-offs
- Reproducible constraints

Every routing choice must answer:

- Where does the signal reflect?
- Where is energy absorbed?
- How is skew controlled?

Open memory requires open signal paths.

---

## Takeaway

DDR signals are waves, not bits.

Topology decides where waves travel.
Termination decides where they die.

If either is wrong, memory lies quietly.

OMI exists to make these choices explicit.
