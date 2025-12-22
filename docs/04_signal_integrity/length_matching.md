# Length Matching and Skew: When Geometry Becomes Timing

This document explains **why trace length matters in DDR systems**, how length mismatch creates skew, and why skew directly consumes timing margin.

In high-speed memory systems, **geometry is timing**.

---

## What Skew Is

**Skew** is the difference in arrival time between two signals that are intended to be interpreted together.

In DDR systems, skew arises primarily from:

- Differences in trace length
- Differences in propagation paths
- Layer changes and via usage

Even when signals switch at the same instant at the source, they may arrive at different times at the receiver.

---

## Why Skew Matters in DDR

DDR timing margins are extremely tight.

Signals must:

- Arrive within defined setup windows
- Remain stable during hold windows
- Cross voltage thresholds cleanly

Skew reduces the effective size of these windows.

If skew becomes too large:

- Setup time is violated
- Hold time is violated
- Data is sampled incorrectly

There is no recovery mechanism.

---

## Propagation Delay and Length

Electrical signals propagate along traces at a finite speed.

On typical PCB materials:

- Propagation delay is on the order of **150–180 ps per centimeter**

This means:

- A few millimeters of extra length translate into tens of picoseconds
- Tens of picoseconds are significant in DDR timing budgets

Length mismatch directly converts into timing error.

---

## Not All Signals Are Equal

DDR does not require all signals to be matched equally.

Different signal groups have **different timing sensitivities**.

Understanding this distinction is critical.

---

## Data Signals (DQ): The Strictest Matching

Data signals:

- Are sampled relative to a strobe
- Operate at the highest toggle rates
- Carry the actual payload

DQ signals within a byte lane must:

- Arrive very closely aligned
- Remain within tight skew limits

Mismatch here:

- Shrinks the data eye
- Causes bit errors within bursts
- Corrupts cache lines

This is why data byte lanes are matched aggressively.

---

## Data Strobes (DQS): The Timing Reference

DQS signals:

- Act as timing references for data capture
- Define the sampling window
- Are used to align DQ sampling dynamically

DQ signals are typically matched **to their associated DQS**, not globally.

If DQS–DQ skew is excessive:

- Sampling occurs too early or too late
- Valid data is missed
- Errors appear immediately

DQS matching is among the most critical constraints.

---

## Address and Command Signals: Different Rules

Address and command signals:

- Are not sampled continuously
- Are latched at specific command boundaries
- Often benefit from fly-by topology

As a result:

- Absolute arrival times matter less
- Relative ordering matters more

Controllers compensate for known skew using timing calibration.

However:

- Excessive skew still reduces margin
- Mismatch still causes command interpretation errors

Matching is important, but less aggressive than for data.

---

## Clock Signals: Global Timing Anchors

Clock signals:

- Define global timing reference
- Must maintain low skew across loads
- Are sensitive to asymmetry

Clock skew:

- Shifts all timing relationships
- Affects every signal group simultaneously

Clock routing is therefore:

- Highly constrained
- Carefully balanced
- Closely tied to topology and termination

---

## Skew Accumulation and Burst Behavior

DDR burst transfers amplify skew effects.

During a burst:

- Errors can accumulate over multiple cycles
- Marginal skew may pass early beats
- Failures appear mid-burst

This is why:

- Systems may pass simple tests
- Fail under sustained load
- Show pattern-dependent corruption

---

## Matching Is About Windows, Not Equality

Length matching does not aim to make all traces identical.

It aims to:

- Keep skew within the valid timing window
- Preserve setup and hold margins
- Ensure predictable sampling

Perfect matching is unnecessary.
Sufficient matching is mandatory.

---

## The Cost of Over-Matching

Over-aggressive matching can:

- Introduce unnecessary serpentine routing
- Increase crosstalk
- Increase inductance
- Create new problems

Matching must balance:

- Timing needs
- Signal integrity
- Routing practicality

Blind matching is as dangerous as no matching.

---

## Implications for DIMM Design

On a DIMM:

- Trace length differences directly affect skew
- Routing topology constrains achievable matching
- Layer transitions must be minimized and controlled

Matching decisions must be:

- Intentional
- Documented
- Justified by timing requirements

OMI treats matching as an engineering decision, not a checklist.

---

## Why Skew Causes "Random" Errors

Skew-related failures:

- Depend on temperature
- Depend on voltage
- Depend on activity patterns

They may:

- Pass at low speed
- Fail at rated speed
- Appear intermittently

This randomness is only apparent.
The cause is geometric.

---

## Why OMI Documents Length Matching Explicitly

OMI documents length matching because:

- It connects physical layout to protocol timing
- It explains why millimeters matter
- It demystifies "timing margin" discussions

Open memory requires open geometry.

---

## Takeaway

At DDR speeds:

- Distance is time
- Geometry is timing
- Skew steals margin silently

Length matching is how designers defend timing windows.

OMI exists to make this defense explicit.

---

Next documents in this stage:
- `crosstalk_and_noise.md`
