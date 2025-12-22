# Decoupling Strategy

This document defines the **decoupling strategy** for the OMI v1 DIMM design.

It explains:

- Why decoupling is required
- What types of decoupling exist
- How different power rails are treated
- How decoupling preserves signal and timing margins

This document is architectural and does not specify component values,
placement rules, or PCB implementation details.

---

## Role of Decoupling in Memory Systems

Decoupling is not optional in DDR systems.

Its purpose is to:

- Supply instantaneous current during switching
- Maintain stable voltage levels
- Prevent noise from propagating across power domains
- Preserve timing and voltage margins

Without proper decoupling, even a perfectly routed design will fail.

---

## Why DDR Is Especially Sensitive to Decoupling

DDR systems exhibit:

- Fast edge rates
- High simultaneous switching activity
- Tight voltage and timing margins
- Strong coupling between power and signal integrity

These properties cause:

- Rapid transient current demand
- Local voltage droop
- Ground and reference bounce

Decoupling exists to absorb these effects locally.

---

## Decoupling as a Hierarchical Concept

Decoupling is not a single capacitor type or placement.

It is a **hierarchical strategy** spanning multiple frequency ranges:

- Bulk decoupling → low-frequency stability
- Local decoupling → mid-frequency transient response
- High-frequency bypassing → edge-rate support

Each level addresses a different physical effect.

---

## Bulk Decoupling (Low-Frequency Stability)

**Purpose:**

- Stabilize rail voltage over longer time scales
- Handle slow load changes
- Support overall rail regulation

**Characteristics:**

- Larger capacitance
- Slower response
- Fewer components

Bulk decoupling prevents large-scale voltage drift but cannot respond to fast edges.

---

## Local Decoupling (Mid-Frequency Transients)

**Purpose:**

- Supply current during normal switching activity
- Reduce local voltage droop
- Isolate disturbances between devices

**Characteristics:**

- Moderate capacitance
- Placed close to loads
- Responds to common DDR switching patterns

Local decoupling is the primary defense against simultaneous switching noise.

---

## High-Frequency Bypassing (Edge Support)

**Purpose:**

- Support very fast current demands
- Reduce high-frequency noise
- Preserve signal edge integrity

**Characteristics:**

- Small capacitance
- Very low inductance
- Effective at high frequencies only

High-frequency bypassing protects the eye diagram directly.

---

## Rail-Specific Decoupling Intent

### VDD (DRAM Core Supply)

**Decoupling intent:**

- Stable, low-noise operation
- Support internal DRAM logic and sensing

**Strategy:**

- Combination of bulk and local decoupling
- Emphasis on maintaining voltage stability over time
- Noise reduction prioritized over transient speed

Core instability causes data retention and sensing failures.

---

### VDDQ (I/O Supply)

**Decoupling intent:**

- Handle large, fast transient currents
- Preserve signal integrity and eye opening

**Strategy:**

- Strong local and high-frequency decoupling
- Focus on rapid response
- Close coupling to signal return paths

VDDQ noise directly distorts signal edges.

---

### Vref (Reference Voltage)

**Decoupling intent:**

- Absolute voltage stability
- Noise isolation from switching activity

**Strategy:**

- Minimal current path
- Heavy filtering and isolation
- No load-driving role

Vref is a reference, not a supply.
Any noise here directly reduces voltage margin.

---

### VTT (Termination Supply)

**Decoupling intent:**

- Support dynamic sourcing and sinking of current
- Maintain stable termination bias

**Strategy:**

- Responsive decoupling capable of bidirectional current flow
- Stability under rapidly changing signal patterns

VTT instability causes ringing and threshold shift.

---

### Standby / Auxiliary Rails

**Decoupling intent:**

- Reliable operation during configuration and idle states

**Strategy:**

- Simple, conservative decoupling
- Isolation from high-speed noise

These rails are low risk but must remain stable.

---

## Decoupling and Power Domain Isolation

Decoupling supports power domain separation by:

- Localizing noise
- Preventing rail-to-rail coupling
- Reducing shared impedance effects

Without proper decoupling:

- Power domains collapse into each other
- Noise propagates system-wide
- Timing margins shrink unpredictably

Isolation is achieved electrically, not just conceptually.

---

## Relationship to Signal Integrity

Decoupling directly affects:

- Jitter
- Edge timing
- Crosstalk susceptibility
- Eye opening

Poor decoupling:

- Turns power noise into timing noise
- Makes failures data-dependent
- Defeats otherwise correct topology and matching

Signal integrity cannot be fixed without power integrity.

---

## Design Intent for OMI v1

For OMI v1:

- Decoupling is treated as a system-level strategy
- All power rails receive appropriate, role-specific decoupling
- Conservative assumptions are used
- No rail is under-decoupled to save cost or space

Correctness takes priority over optimization.

---

## What This Document Does NOT Decide

This document does not define:

- Capacitor values
- Capacitor types
- Placement rules
- PCB stack-up
- Regulator specifications

Those belong to implementation and validation stages.

---

## Takeaway

Decoupling is how the power system keeps up with reality.

It absorbs current, suppresses noise, and protects margins.

For OMI v1, decoupling is not an afterthought.
It is a foundational design decision.

---

This completes the power architecture for Stage 5.
