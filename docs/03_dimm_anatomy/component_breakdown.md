# Component Breakdown: What Lives on a DIMM and Why

This document provides a **systematic breakdown of all functional components on a DDR DIMM**, explaining the role each component plays in correctness, signal integrity, power integrity, and system compatibility.

A DIMM is not a passive carrier.
Every component exists to satisfy a specific constraint imposed by DRAM physics, DDR protocol, or system-level assumptions.

---

## Overview: The DIMM as a System

A DDR DIMM integrates multiple subsystems onto a single PCB.

At a minimum, a DIMM contains:

1. DRAM devices
2. Power delivery components
3. Signal termination components
4. Reference voltage generation
5. Configuration and identification logic
6. Passive components for stability and integrity

Removing or misunderstanding any of these compromises correctness.

---

## 1. DRAM Devices

**Role:**  
Store data using DRAM cells and implement the DDR protocol internally.

**Key characteristics:**

- Contain rows, columns, banks, and sense amplifiers
- Perform destructive reads and restoration
- Require strict timing and voltage conditions

**What they do NOT provide:**

- Stable power delivery
- Proper signal termination
- System-level configuration

DRAM devices assume the DIMM provides a clean electrical environment.

---

## 2. Power Supply Rails and Distribution

DIMMs distribute multiple power rails, commonly including:

- **VDD**: Core supply for DRAM logic and arrays
- **VTT**: Termination voltage for address and command signals
- **Vref**: Reference voltage for signal thresholding

(Some generations include additional or renamed rails.)

**Why this matters:**

- DRAM operates with very narrow voltage margins
- Noise or droop directly affects sensing accuracy
- Power instability causes silent data corruption

Power delivery on the DIMM is a first-class design problem.

---

## 3. Decoupling Capacitors

**Role:**  
Stabilize power rails by supplying instantaneous current and filtering noise.

**Types:**

- Bulk capacitors (low-frequency stability)
- Ceramic capacitors (high-frequency noise suppression)

**Why they are critical:**

- DRAM draws sharp current bursts during activation
- Long power paths cannot respond fast enough
- Without local decoupling, voltage collapses occur

Decoupling placement and values directly affect memory reliability.

---

## 4. Signal Termination Components

**Role:**  
Control signal reflections and maintain impedance matching.

Termination may include:

- Series resistors
- Parallel resistors
- On-die termination (in combination with module-level components)

**Why termination exists:**

- DDR signals operate as transmission lines
- Impedance discontinuities cause reflections
- Reflections distort timing and voltage levels

Termination is essential to protect setup and hold margins.

---

## 5. Reference Voltage Generation (Vref)

**Role:**  
Provide a stable voltage reference for interpreting logic levels.

**Why Vref is special:**

- It defines the threshold between logical 0 and 1
- It must track supply variations precisely
- It must be extremely quiet

Even small noise on Vref:

- Shifts decision thresholds
- Causes bit errors
- Produces temperature- and pattern-dependent failures

Vref stability is non-negotiable.

---

## 6. SPD EEPROM (Serial Presence Detect)

**Role:**  
Store configuration and identification data used during system initialization.

SPD typically contains:

- Memory size and organization
- Timing parameters
- Voltage requirements
- Manufacturer information

**Why SPD is required:**

- The memory controller must configure DDR safely
- Hard-coded assumptions are not viable
- Systems must support many DIMM variants

Without SPD, reliable initialization is impossible.

---

## 7. I²C / SMBus Interface Components

**Role:**  
Enable communication between the system and the SPD EEPROM.

Includes:

- Pull-up resistors
- Address configuration
- Bus isolation (if needed)

Though low-speed, this interface is essential for system bring-up.

---

## 8. PCB Itself as a Component

The DIMM PCB is not just a substrate.

It defines:

- Signal impedance
- Trace length matching
- Return paths
- Crosstalk behavior
- Power plane stability

Poor PCB design negates even perfect component selection.

The PCB is an active electrical component.

---

## 9. Mechanical Keying and Edge Connector

**Role:**  
Ensure correct insertion and electrical compatibility.

Mechanical constraints influence:

- Pin ordering
- Signal grouping
- Ground placement

Pin assignment reflects electrical requirements, not convenience.

---

## What Is Intentionally Absent

A standard UDIMM does NOT include:

- Active logic (except SPD)
- Retimers or buffers
- Error correction logic
- Voltage regulation (usually external)

These absences are design choices that shift responsibility to the DIMM and motherboard.

---

## Why This Breakdown Matters for OMI

OMI documents each component because:

- Memory correctness is a system property
- Failures emerge from interactions, not parts
- "Optional" components often protect critical margins

Open memory design requires explaining:

- Why each component exists
- What happens if it is misdesigned
- How it contributes to overall correctness

---

## Takeaway

A DIMM is a carefully balanced system.

DRAM chips store data,  
but power integrity preserves it,  
signal integrity delivers it,  
reference voltages define it,  
and configuration logic enables it.

Understanding memory means understanding **all of these together**.

OMI exists to make this system visible.
