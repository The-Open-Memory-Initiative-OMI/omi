# Eye Diagrams and Margins: Seeing Signal Integrity Holistically

This document explains **eye diagrams**, what they represent, and why they are the most important tool for understanding signal integrity in DDR systems.

An eye diagram is not just a visualization.
It is a **summary of every physical effect acting on a signal**.

---

## Why Eye Diagrams Matter

DDR systems fail when:

- Signals are sampled at the wrong time
- Voltages cross thresholds incorrectly
- Timing or noise margins collapse

Eye diagrams show **how close the system is to failure**.

They combine the effects of:

- Transmission line behavior
- Reflections and impedance mismatch
- Length mismatch and skew
- Crosstalk and noise
- Power integrity issues
- Jitter and timing uncertainty

If something harms signal integrity, it harms the eye.

---

## What an Eye Diagram Is

An eye diagram is created by:

- Repeating a signal over many cycles
- Overlaying the waveforms on top of each other
- Aligning them in time

The result is a composite image that shows:

- All possible transitions
- All timing variations
- All voltage variations

The "eye" opening represents **where valid data can be safely sampled**.

---

## The Eye Opening

The eye has two critical dimensions:

### Vertical Opening (Voltage Margin)

- How far the signal stays away from logic thresholds
- Indicates noise tolerance
- Shrinks due to noise, crosstalk, reflections, and power instability

### Horizontal Opening (Timing Margin)

- How long the signal remains stable in time
- Indicates setup and hold margin
- Shrinks due to skew, jitter, reflections, and propagation delay

Both margins must exist simultaneously for correctness.

---

## Where Sampling Happens

DDR receivers sample data:

- At very specific points in time
- Relative to a clock or strobe (DQS)
- Assuming the eye is open at that moment

If sampling occurs:

- Too early → setup violation
- Too late → hold violation
- At low voltage margin → bit error

The eye diagram shows **whether a safe sampling point exists**.

---

## How Each SI Effect Attacks the Eye

### Transmission Line Effects

- Spread transitions in time
- Introduce delay uncertainty
- Reduce horizontal opening

---

### Reflections

- Cause ringing
- Create false crossings
- Reduce both voltage and timing margin

---

### Length Mismatch and Skew

- Shift signals relative to the sampling point
- Reduce horizontal opening
- Cause lane-to-lane misalignment

---

### Crosstalk and Noise

- Add voltage variation
- Create data-dependent eye closure
- Reduce vertical opening unpredictably

---

### Power Integrity Issues

- Shift reference levels
- Introduce ground bounce
- Collapse both margins simultaneously

---

## Jitter: The Invisible Enemy

Jitter is variation in signal timing.

Sources include:

- Power noise
- Crosstalk
- Clock instability
- Thermal effects

Jitter:

- Smears the eye horizontally
- Reduces effective setup and hold windows
- Accumulates across bursts

DDR tolerates very little jitter.

---

## Why Passing Is Not Binary

A common misconception:

> "If the eye is open, the system works."

Reality:

- Eye opening shrinks with temperature
- Shrinks with voltage variation
- Shrinks under load
- Shrinks with aging

A design that "just passes" has **no safety margin**.

OMI treats margin as a first-class requirement.

---

## Margins Are Not Evenly Consumed

Different effects eat different margins:

- Skew mostly consumes timing margin
- Crosstalk mostly consumes voltage margin
- Reflections consume both
- Power noise shifts the entire eye

Designers must know **which margin is weakest**.

---

## Why Eye Diagrams Predict Real Failures

Eye diagrams explain why systems:

- Pass lab tests
- Fail in the field
- Fail only under stress
- Fail intermittently

The eye closes *before* failure occurs.
Errors are simply the first visible symptom.

---

## Why Software Never Sees the Eye

Software sees:

- Loads
- Stores
- Crashes
- Corruption

It never sees:

- Margins shrinking
- Timing windows collapsing
- Noise increasing

This is why hardware signal integrity problems masquerade as software bugs.

---

## Implications for DIMM Design

For a DIMM:

- Every routing decision shapes the eye
- Every power decision shifts the eye
- Every termination choice controls ringing

There is no single "fix" for a bad eye.
Only disciplined design preserves it.

---

## Why OMI Uses Eye Diagrams Conceptually

OMI uses eye diagrams to:

- Unify physical effects
- Explain failure modes
- Justify conservative design choices
- Teach margin-based thinking

Even when no oscilloscope is present, the **eye model must exist in the designer's head**.

---

## Takeaway

An eye diagram is the truth.

It shows:

- How much margin you really have
- How close you are to failure
- Whether your assumptions are valid

When the eye closes, memory lies.

OMI exists to keep the eye open — and to explain how.

---

This concludes Stage 4: Signal Integrity.
