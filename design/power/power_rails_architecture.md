# Power Rails Architecture

This document defines the **power rail architecture** for the OMI v1 DIMM design.

It explains:

- Which power rails exist
- What each rail powers
- Why each rail is necessary
- How power domains are conceptually separated

This document is architectural in nature and does not define component values,
placement, or PCB implementation details.

---

## Role of Power Architecture in Memory Correctness

In DDR systems, power is not a background utility.
It is an **active participant in signal integrity and timing correctness**.

Power integrity affects:

- Signal thresholds
- Timing margins
- Noise susceptibility
- Calibration stability

Many memory failures originate from power instability rather than logic errors.

---

## Guiding Principles

The OMI v1 power architecture follows these principles:

- Separate rails for separate electrical roles
- Clear distinction between supply, reference, and termination
- Conservative, standards-aligned structure
- Predictable behavior over performance optimization

Power rails are defined by **function**, not convenience.

---

## Primary Power Rails

### 1. DRAM Core Supply (VDD)

**Role:**

- Powers the internal logic and memory cells of DRAM devices

**Characteristics:**

- Supplies the majority of operating current
- Sensitive to noise and droop
- Directly affects data retention and sensing margins

**Design intent:**

- Stable, low-noise supply
- Adequate decoupling close to DRAM devices
- Treated as a critical rail

VDD instability directly causes data corruption.

---

### 2. I/O Supply (VDDQ)

**Role:**

- Powers the I/O drivers and receivers of DRAM devices
- Defines signal swing levels for DQ, DQS, address, and command signals

**Characteristics:**

- High transient current during switching
- Strong coupling to signal integrity
- Sensitive to simultaneous switching noise

**Design intent:**

- Isolated conceptually from core supply
- Designed to handle dynamic load changes
- Closely tied to signal integrity constraints

VDDQ quality directly shapes the eye diagram.

---

## Reference and Bias Rails

### 3. Reference Voltage (Vref)

**Role:**

- Defines the comparison threshold for signal sampling
- Used by receivers to interpret logic levels

**Characteristics:**

- Carries negligible current
- Extremely sensitive to noise
- Must remain stable relative to VDDQ

**Design intent:**

- Treated as an analog reference
- Isolated from switching noise
- Never used as a power source

Vref noise reduces voltage margin silently.

---

### 4. Termination Supply (VTT)

**Role:**

- Provides a bias point for signal termination
- Absorbs signal energy to reduce reflections

**Characteristics:**

- Sources and sinks current dynamically
- Responds to signal activity
- Strongly tied to address/command integrity

**Design intent:**

- Stable midpoint reference
- Capable of dynamic current response
- Conceptually separate from logic supplies

VTT instability causes ringing and threshold shift.

---

## Auxiliary and Control Rails

### 5. Standby / Auxiliary Power

**Role:**

- Powers low-speed components such as SPD EEPROM
- Enables configuration and discovery before DRAM operation

**Characteristics:**

- Low current
- Always available during system standby

**Design intent:**

- Isolated from high-speed noise
- Reliable across power states

This rail enables correct bring-up behavior.

---

## Power Domain Separation

The OMI v1 design treats the following as **distinct power domains**:

- DRAM core operation (VDD)
- I/O signaling (VDDQ)
- Signal reference (Vref)
- Termination biasing (VTT)
- Configuration and standby logic

These domains are separated to:

- Prevent noise coupling
- Localize disturbances
- Preserve timing and voltage margins

Domain separation is a correctness decision.

---

## Relationship to Signal Integrity

Power rails directly influence:

- Edge timing
- Threshold stability
- Jitter
- Crosstalk susceptibility

Poor power architecture:

- Shrinks eye openings
- Increases data-dependent failures
- Defeats otherwise correct topology

Signal integrity and power integrity are inseparable.

---

## Design Intent for OMI v1

For OMI v1:

- All standard DDR power rails are explicitly defined
- No rail is overloaded with multiple roles
- Conservative separation is maintained
- No power optimization shortcuts are taken

This prioritizes clarity, predictability, and reproducibility.

---

## What This Document Does NOT Decide

This document does not define:

- Voltage levels
- Regulator selection
- Capacitor values
- Placement or routing
- Transient response targets

Those belong to later implementation and validation stages.

---

## Takeaway

Power rails define the electrical environment in which memory operates.

If that environment is unstable, memory correctness cannot be guaranteed.

For OMI v1, power architecture is explicit, conservative, and intentional.

---

Next document in this directory:
- `decoupling_strategy.md`
