# Reflections and Impedance Matching: Why Signals Ring

This document explains **signal reflections**, why they occur on DDR interconnects, and how impedance matching is used to control them.

Reflections are not noise or defects.
They are a direct consequence of how energy propagates on transmission lines.

---

## What a Reflection Is

A reflection occurs when a traveling voltage wave encounters a change in impedance.

At that point:

- Part of the wave continues forward
- Part of the wave reflects back toward the source

This behavior follows directly from:

- Energy conservation
- Boundary conditions in electromagnetic systems

Reflections are inevitable when impedances do not match.

---

## Where Impedance Changes Occur

On a DIMM or motherboard, impedance changes appear at:

- Driver output impedance
- Receiver input impedance
- Via transitions
- Connector interfaces
- Stubs and branches
- Termination resistors
- Changes in trace geometry or reference planes

Even small discontinuities matter at DDR speeds.

---

## Why Reflections Cause Ringing

When reflections bounce back and forth:

- Multiple wavefronts superimpose
- Voltage overshoot and undershoot appear
- The signal "rings" before settling

Ringing is not a steady-state problem.
It is a **time-domain problem** that affects sampling moments.

If the signal has not settled when sampled:

- The wrong logic value may be captured
- Setup or hold margins are violated

---

## The Reflection Coefficient (Conceptual)

The amount of reflection depends on how large the impedance mismatch is.

Conceptually:

- Perfect match → no reflection
- Large mismatch → strong reflection

The **reflection coefficient** expresses:

- How much energy is reflected
- With what polarity (positive or negative)

Exact equations are less important than the intuition:

> Bigger mismatch → bigger reflection → smaller margin.

---

## Source vs Load Reflections

Reflections behave differently depending on where the mismatch occurs.

### Load-End Reflections

- Occur when the wave reaches the receiver
- Reflect back toward the source
- Affect voltage at the receiver first

### Source-End Reflections

- Occur when reflected energy reaches the driver
- Can re-reflect back toward the receiver
- Create additional ringing cycles

This back-and-forth continues until energy is dissipated.

---

## Why DDR Is Especially Sensitive

DDR systems are sensitive to reflections because:

- Timing windows are very narrow
- Voltage swings are small
- Sampling occurs at precise moments
- Bursts amplify cumulative effects

A reflection that would be harmless in slower systems can be fatal in DDR.

---

## Impedance Matching: What It Really Means

Impedance matching does NOT mean:

- Eliminating all reflections
- Creating a perfectly flat waveform

Instead, matching aims to:

- Reduce reflection amplitude
- Ensure the signal settles quickly enough
- Preserve setup and hold margins

The goal is **predictable settling**, not perfection.

---

## Common Matching Strategies in DDR

### Source Series Termination

- A resistor near the driver
- Matches driver + resistor to trace impedance
- Reduces initial reflection

Used often for unidirectional signals.

---

### Parallel Termination

- A resistor to VTT or ground at the receiver
- Absorbs incoming energy
- Prevents reflection back toward the source

Common for address and command signals.

---

### On-Die Termination (ODT)

- Termination implemented inside DRAM devices
- Dynamically enabled or disabled
- Absorbs reflections near the load

ODT simplifies layouts but does not remove topology constraints.

---

## Why Fly-By Routing Works with Termination

In fly-by topology:

- Each device sees a slightly delayed version of the signal
- Termination at the far end absorbs energy
- Reflections are minimized

Timing calibration compensates for arrival skew.
Termination controls reflection amplitude.

Both are required.

---

## Why Stubs Are Reflection Factories

A stub creates:

- A local impedance discontinuity
- A short transmission line branch
- Stored energy that reflects back later

Even very short stubs:

- Create delayed reflections
- Distort edges
- Reduce eye opening

This is why DDR routing aggressively avoids stubs.

---

## Reflections vs Crosstalk (Important Distinction)

Reflections:

- Originate from impedance mismatch
- Are self-interference
- Depend on topology and termination

Crosstalk:

- Originates from neighboring signals
- Is coupling-based interference

Both shrink margins, but they are solved differently.

---

## Why Reflections Cause Data-Dependent Failures

Reflections interact with:

- Data patterns
- Burst activity
- Simultaneous switching

This makes failures:

- Pattern-dependent
- Load-dependent
- Temperature-sensitive

Which is why they appear random from software's perspective.

---

## Implications for Timing Margins

Reflections:

- Shift effective edge timing
- Cause false threshold crossings
- Reduce usable eye width

A system may pass basic tests yet fail under:

- High throughput
- Specific access patterns
- Worst-case environmental conditions

---

## Why OMI Treats Matching as Core Knowledge

OMI documents reflections and matching because:

- They explain why layout rules exist
- They connect physics to timing parameters
- They demystify "signal integrity issues"

Without this understanding:

- Designers over-trust simulations
- Margins are assumed instead of proven
- Failures become untraceable

---

## Takeaway

Reflections are not accidents.
They are physics responding to mismatch.

Impedance matching does not eliminate reflections.
It controls them enough to preserve correctness.

At DDR speeds:

- Small mismatches matter
- Small reflections steal margin
- Margin loss becomes data corruption

OMI exists to make these relationships explicit.

---

Next documents in this stage:
- `length_matching.md`
