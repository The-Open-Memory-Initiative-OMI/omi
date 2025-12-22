# Power Rails: Supplying Stability to Fragile Memory

This document explains the **power rails present on a DDR DIMM**, their roles, and why **power integrity is one of the dominant factors in memory correctness**.

Many memory failures that appear random, software-related, or unreproducible are in fact **power integrity failures**.

---

## Power Integrity Is Not Optional

DRAM does not fail loudly when power is marginal.
It fails silently.

Unlike digital logic with wide noise margins, DRAM:

- Operates with small voltage swings
- Depends on analog sensing
- Uses shared internal resources
- Has minimal redundancy

As a result:

> Even small power disturbances can corrupt data without immediate detection.

---

## Overview of DIMM Power Rails

A typical DDR DIMM distributes several distinct power rails, including:

- **VDD** — Core DRAM supply
- **VTT** — Termination supply
- **Vref** — Reference voltage

(Some DDR generations introduce additional or renamed rails, but the principles remain the same.)

Each rail serves a **different electrical purpose** and has different stability requirements.

---

## VDD: Core DRAM Supply

### What VDD Powers

VDD supplies:

- DRAM cell arrays
- Sense amplifiers
- Internal logic
- I/O drivers (in some generations)

VDD directly affects:

- Charge storage levels
- Sensing margins
- Timing stability

---

### Why VDD Stability Matters

DRAM sensing relies on detecting **very small voltage differences**.
If VDD:

- Drops suddenly
- Contains excessive ripple
- Exhibits ground bounce

Then:

- Sense amplifiers misinterpret data
- Restoration becomes incomplete
- Retention time is reduced

These effects may not cause immediate failure.

---

### Transient Current Demand

DRAM draws current in **bursts**, not smoothly.

High current events occur during:

- Row activation
- Sense amplification
- Write restoration
- Refresh operations

If the power delivery network cannot respond quickly:

- Voltage droop occurs
- Margins collapse
- Errors appear under load

This is why bulk and high-frequency decoupling are both required.

---

## VTT: Termination Supply

### What VTT Does

VTT supplies termination for:

- Address signals
- Command signals
- Control signals

It is typically centered around a mid-level voltage.

---

### Why Termination Needs Its Own Supply

DDR command and address buses are:

- Multi-drop
- Bidirectional
- High-speed

Proper termination:

- Absorbs signal energy
- Prevents reflections
- Maintains signal integrity

Using VDD directly would:

- Introduce noise coupling
- Shift logic thresholds
- Reduce timing margins

VTT isolates termination behavior from core supply noise.

---

### VTT Noise = Timing Errors

Instability on VTT causes:

- Reflection-related overshoot or undershoot
- Timing uncertainty
- Setup/hold violations

These failures often:

- Appear data-pattern dependent
- Appear temperature sensitive
- Only occur at high activity levels

They are notoriously difficult to diagnose.

---

## Vref: Reference Voltage

### What Vref Is

Vref defines the **decision threshold** for interpreting signal levels.

It is used by:

- Input receivers
- Sense comparators
- Timing logic

Vref is not a power rail in the traditional sense.
It is a **measurement reference**.

---

### Why Vref Is Extremely Sensitive

Unlike VDD or VTT:

- Vref does not deliver current
- Vref must track supply variations precisely
- Vref must be exceptionally quiet

Small noise on Vref:

- Shifts logic thresholds
- Skews timing decisions
- Causes bit errors

A few millivolts can be enough.

---

### Vref Tracking Requirement

Vref must:

- Track half of the relevant supply
- Maintain proportionality under load
- Remain stable across temperature

If Vref drifts:

- Timing calibration becomes invalid
- Data capture becomes unreliable

This is why Vref routing and filtering are critical.

---

## Interaction Between Power Rails

Power rails are **not independent**.

Noise on one rail can:

- Couple into others through parasitics
- Shift reference relationships
- Amplify errors during high activity

For example:

- VDD droop alters sensing margins
- Vref noise shifts decision thresholds
- VTT instability distorts command timing

Memory correctness depends on **relative stability**, not absolute voltage.

---

## Decoupling Strategy on the DIMM

DIMMs rely on multiple layers of decoupling:

### Bulk Capacitors

- Handle low-frequency fluctuations
- Supply sustained current

### Ceramic Capacitors

- Handle high-frequency transients
- Suppress switching noise

Placement matters as much as value.

Poor placement:

- Increases effective inductance
- Delays current delivery
- Shrinks timing margins

---

## Why Power Failures Look Random

Power integrity failures:

- Depend on workload
- Depend on access patterns
- Depend on temperature
- Depend on refresh timing

They often:

- Pass basic tests
- Fail under stress
- Disappear when observed

This creates the illusion of randomness.

---

## Implications for Module-Level Design

At the DIMM level:

- Power plane design defines noise behavior
- Via placement affects inductance
- Decoupling density affects transient response
- Rail isolation affects cross-coupling

Power integrity is not something that can be fixed later.
It must be designed in.

---

## Why OMI Treats Power as Core Knowledge

OMI documents power rails because:

- Memory correctness depends on them
- Most failures originate here
- They are rarely explained openly

Understanding power rails transforms:

- Debugging ability
- Design discipline
- Validation quality

Open memory requires open power design.

---

## Takeaway

DRAM does not tolerate sloppy power.

VDD preserves charge.
VTT preserves signal shape.
Vref preserves meaning.

If any of these fail, memory lies — quietly.

OMI exists to make that visible.
