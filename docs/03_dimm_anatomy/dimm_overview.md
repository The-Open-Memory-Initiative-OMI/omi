# DIMM Overview: Memory as a Physical System

This document introduces the **DIMM (Dual Inline Memory Module)** as a physical system.

It explains what a DIMM contains, why it exists as a separate entity from the DRAM chips, and why **module-level design is the correct starting point for open memory**.

---

## What a DIMM Is (and Is Not)

A DIMM is **not** just a collection of DRAM chips.

A DIMM is:

- A high-speed electrical system
- A power distribution network
- A signal integrity environment
- A mechanical and connector interface
- A configuration and identification mechanism

The DIMM is where **DRAM physics meets the system bus**.

---

## Why DIMMs Exist at All

Early memory systems placed DRAM directly on the motherboard.

As speeds increased, this became impractical due to:

- Manufacturing constraints
- Upgrade limitations
- Yield and cost issues
- Signal integrity challenges

DIMMs solve these problems by:

- Standardizing form factor and pinout
- Allowing modular capacity scaling
- Separating memory manufacturing from motherboard design
- Enabling replaceability and testing

This modularity comes at a cost: **electrical complexity**.

---

## The DIMM as a Boundary Layer

The DIMM sits between:

- The memory controller (on the CPU)
- The DRAM devices themselves

It must translate:

- Controller assumptions
- DDR protocol requirements
- Electrical realities of the DRAM array

Into a system that works reliably across:

- Platforms
- Vendors
- Temperatures
- Workloads

This makes the DIMM a **critical boundary layer**, not a passive carrier.

---

## Major Functional Blocks on a DIMM

At a high level, a DIMM contains:

1. DRAM devices
2. Power delivery network
3. Signal routing and termination
4. Reference voltage generation
5. Configuration and identification logic
6. Mechanical and connector interface

Each of these is essential to correctness.

---

## DRAM Devices on the Module

The DRAM chips:

- Contain the memory cells
- Implement the DDR protocol internally
- Rely on the module for power quality and signal integrity

They do **not**:

- Handle system-level termination
- Control routing topology
- Guarantee signal margins on their own

Their correct operation depends on the DIMM design.

---

## Power Delivery Is a First-Class Concern

A DIMM distributes multiple power rails, typically including:

- Core supply (VDD)
- Termination supply (VTT)
- Reference voltages (Vref)

The DIMM must:

- Handle fast current transients
- Minimize noise
- Maintain stable reference levels

Power integrity failures manifest as **random memory errors**.

---

## Signal Integrity Is Not Optional

DDR signals:

- Operate at very high speeds
- Have tight timing margins
- Are sensitive to impedance discontinuities

The DIMM defines:

- Trace lengths and matching
- Topology (point-to-point, fly-by)
- Termination placement

Poor signal integrity cannot be corrected in software.

---

## Configuration and Identification (SPD)

DIMMs include an SPD (Serial Presence Detect) device that:

- Identifies memory characteristics
- Provides timing and configuration data
- Enables system initialization

Without SPD:

- The system cannot safely configure memory
- Conservative defaults must be used
- Compatibility breaks down

SPD is part of the DIMM, not the DRAM chips.

---

## Mechanical and Connector Constraints

The DIMM must also satisfy:

- Slot compatibility
- Mechanical tolerances
- Insertion reliability
- Signal pin ordering

Pin placement is not arbitrary.
It reflects:

- Signal grouping
- Return path requirements
- Crosstalk control

Mechanical design affects electrical behavior.

---

## Why DIMMs Are Hard to Design

A DIMM must:

- Meet DDR timing under worst-case conditions
- Work across many motherboards
- Survive variation in manufacturing
- Tolerate noise and skew

All while:

- Being physically small
- Cost-effective
- Manufacturable at scale

This is why DIMM design is traditionally closed and vendor-controlled.

---

## Why OMI Starts at the DIMM Level

OMI does **not** start with DRAM silicon because:

- Silicon design is legally and practically constrained
- Validation costs scale non-linearly
- Knowledge is heavily patented

OMI starts at the DIMM level because:

- It is buildable
- It is testable on commodity hardware
- It exposes real system-level constraints
- It teaches transferable engineering skills

Module-level design is the **narrowest point where openness is still meaningful**.

---

## Scope Reminder

In OMI v1:

- The DIMM is the primary design artifact
- All design decisions must be documented
- Assumptions must be explicit
- Validation must be reproducible

The DIMM is not an intermediate step.
It is the goal.

---

## Takeaway

A DIMM is not passive memory.

It is an engineered system that:

- Preserves fragile DRAM correctness
- Enforces invisible timing contracts
- Shields the CPU from analog reality

Understanding the DIMM is understanding real memory.

OMI exists to make that understanding open.
