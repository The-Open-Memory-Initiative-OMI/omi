# Crosstalk and Noise: When Other Signals Become the Problem

This document explains **crosstalk and noise coupling** in DDR systems, why high-speed signals interfere with each other, and how this interference silently erodes timing and voltage margins.

Many memory failures are not caused by a single signal behaving badly, but by **many signals interacting simultaneously**.

---

## What Crosstalk Is

**Crosstalk** is unwanted coupling between signals.

It occurs when:

- Energy from one signal couples into a neighboring signal
- The victim signal's voltage or timing is disturbed
- The disturbance depends on activity elsewhere

Crosstalk is not random noise.
It is **deterministic interference caused by geometry and activity**.

---

## Why Crosstalk Exists on PCBs

Signals on a PCB are not isolated.

They interact through:

- **Capacitive coupling** (electric fields)
- **Inductive coupling** (magnetic fields)
- **Shared return paths**

At DDR speeds:

- Edges are fast
- Fields are strong
- Margins are small

Coupling becomes unavoidable.

---

## Capacitive Coupling (Electric Field)

Capacitive crosstalk occurs when:

- Two traces run close together
- Voltage changes on one trace induce charge on the other

Characteristics:

- Strongly dependent on trace spacing
- Proportional to edge rate
- Affects voltage levels directly

Capacitive coupling mainly causes:

- Voltage shifts
- False threshold crossings

---

## Inductive Coupling (Magnetic Field)

Inductive crosstalk occurs when:

- Rapid current changes create magnetic fields
- Fields induce voltage in nearby loops

Characteristics:

- Dependent on current magnitude
- Strongly affected by return path geometry
- Sensitive to loop area

Inductive coupling often causes:

- Timing shifts
- Ringing
- Burst-related errors

---

## Near-End and Far-End Crosstalk

Crosstalk manifests differently depending on observation point.

### Near-End Crosstalk (NEXT)

- Appears at the same end as the aggressor driver
- Often strongest immediately
- Affects launch timing

### Far-End Crosstalk (FEXT)

- Appears at the far end of the trace
- Depends on length and coupling symmetry
- Affects sampling directly

Both are relevant in DDR systems.

---

## Simultaneous Switching Noise (SSN)

When many signals switch at once:

- Large transient currents flow
- Power and ground planes bounce
- Reference levels shift temporarily

This is known as **simultaneous switching noise**.

SSN:

- Is data-pattern dependent
- Increases with bus width and speed
- Couples power integrity into signal integrity

DDR bursts make SSN unavoidable.

---

## Ground Bounce and Reference Shift

High transient currents cause:

- Local ground potential to rise or fall
- Effective reference voltage to move

Consequences:

- Logic thresholds shift dynamically
- Signals appear early or late
- Eye openings shrink

This is especially dangerous for:

- DQS sampling
- Vref-based receivers

---

## Crosstalk Is Data-Dependent

Crosstalk depends on:

- Which signals are switching
- How many switch together
- The direction of switching
- The timing alignment of edges

This causes failures that:

- Appear only under specific patterns
- Disappear under simple tests
- Change with workload

This is why memory bugs look "random".

---

## Why Crosstalk Shrinks Margins, Not Just Signals

Crosstalk does not usually flip bits directly.

Instead, it:

- Adds noise to edges
- Shifts crossing points
- Reduces setup and hold windows

When combined with:

- Reflections
- Skew
- Power noise

Margins collapse.

---

## Crosstalk vs Reflections (Important Distinction)

Reflections:

- Come from impedance mismatch
- Are self-interference
- Repeat predictably

Crosstalk:

- Comes from other signals
- Depends on activity
- Varies dynamically

Both must be controlled independently.

---

## Mitigation Strategies (Conceptual)

Crosstalk is reduced by:

- Increasing spacing between traces
- Maintaining continuous reference planes
- Minimizing loop areas
- Reducing parallel run lengths
- Controlling edge rates
- Proper return path design

Exact rules depend on stack-up and topology and are addressed later.

---

## Implications for DIMM Design

On a DIMM:

- Dense routing increases coupling
- Byte lanes switching together amplify noise
- Poor plane design worsens SSN
- Over-aggressive length matching can increase coupling

Design is always a trade-off.

Signal integrity cannot be optimized signal-by-signal.
It must be optimized **system-wide**.

---

## Why Crosstalk Is Hard to Simulate Perfectly

Crosstalk depends on:

- Real activity patterns
- Simultaneous switching behavior
- Manufacturing variation
- Environmental conditions

Simulations help, but:

- Worst-case combinations are hard to enumerate
- Margins must be conservative

Validation must assume reality is worse than models.

---

## Why OMI Documents Crosstalk Explicitly

OMI documents crosstalk because:

- It explains activity-dependent failures
- It connects geometry to unpredictability
- It demystifies "random" memory corruption

Open memory requires understanding interference, not just signals.

---

## Takeaway

At DDR speeds:

- Signals do not live alone
- Neighbors matter
- Activity creates interference
- Margins disappear quietly

Crosstalk is why memory correctness is a system problem.

OMI exists to make that system visible.

---

Next documents in this stage:
- `eye_diagrams_and_margins.md`
