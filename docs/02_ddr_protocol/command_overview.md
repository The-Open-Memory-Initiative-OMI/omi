# DDR Command Overview: Controlling DRAM Safely

This document introduces the **DDR command protocol** at a conceptual level.

It explains **what commands exist**, **what architectural actions they trigger**, and **why the protocol is structured the way it is**.

Timing details are intentionally deferred to later documents.

---

## What DDR Actually Is

DDR (Double Data Rate) is often described as a "memory technology".

In practice, DDR is:

- A **command protocol**
- A **timing contract**
- A **signaling discipline**

Layered on top of DRAM's physical architecture.

DDR exists to ensure that:

- Destructive reads are restored correctly
- Rows and banks are accessed safely
- Electrical and timing constraints are never violated

---

## Separation of Concerns in DDR

DDR cleanly separates two functions:

1. **Command and address control**
2. **Data transfer**

This separation allows:

- Predictable sequencing
- Safe overlap of operations
- Enforcement of architectural constraints

The protocol assumes the DRAM array behaves exactly as described in Stage 1.

---

## The Core DDR Commands

At a high level, DDR exposes a small set of fundamental commands.

These commands are not arbitrary.
Each exists to protect a specific architectural invariant.

---

### ACT (Activate)

**Purpose:**  
Open a row in a specific bank.

**What it does:**

- Raises the wordline for the selected row
- Connects all cells in that row to sense amplifiers
- Begins sensing and restoration

**Architectural implication:**

- One row becomes active in the selected bank
- The row buffer is populated

ACT is expensive and slow relative to other commands.

---

### READ

**Purpose:**  
Retrieve data from the active row.

**What it does:**

- Selects columns within the active row
- Transfers data from the row buffer to the I/O circuitry
- Outputs data in bursts

**Key point:**

- READ does **not** activate a row
- A row must already be active

READ relies on the destructive-read-and-restore mechanism.

---

### WRITE

**Purpose:**  
Store data into the active row.

**What it does:**

- Selects columns within the active row
- Drives data into the row buffer
- Overwrites stored charge in cells

WRITE also requires an already active row.

---

### PRE (Precharge)

**Purpose:**  
Close the currently active row.

**What it does:**

- Disconnects cells from sense amplifiers
- Returns bitlines to a neutral state
- Prepares the bank for the next activation

PRE is mandatory before activating a different row in the same bank.

---

### REF (Refresh)

**Purpose:**  
Preserve data by restoring charge.

**What it does:**

- Internally activates rows
- Restores stored data
- Ensures retention guarantees are met

REF commands are issued periodically and block normal access.

---

## The Command Lifecycle

A typical access sequence looks like:

1. ACT — open the row
2. READ or WRITE — access data
3. (optional additional READ/WRITE)
4. PRE — close the row

Every step exists because of DRAM's physical behavior.

Skipping steps does not degrade performance.
It destroys correctness.

---

## Visual Example: DDR Command Timing

The following diagram illustrates how DDR commands are sequenced over time, showing ACT, READ/WRITE operations, and timing constraints between commands:

![DDR Command Timing Diagram](C:/Users/senso/.gemini/antigravity/brain/84527a44-3244-4aed-8e9b-4c34373a169f/ddr_command_timing.png)

This timing diagram shows:

- Multiple ACT commands activating rows in different banks
- READ/WRITE commands accessing open rows
- Timing intervals (tRRD, tFAW) that must be respected
- How commands overlap across different banks

---

## Why DDR Is So Strict

DDR protocols are strict because:

- DRAM reads are destructive
- Rows cannot be multiplexed freely
- Sense amplifiers are shared resources
- Timing margins are narrow

The protocol prevents:

- Multiple rows in one bank being active
- Incomplete restoration
- Electrical contention
- Silent corruption

What looks like rigidity is actually protection.

---

## Bursts and Efficiency

DDR transfers data in **bursts** rather than single words.

Reasons:

- Row buffers contain large amounts of data
- Column access is cheap once a row is open
- Bus turnaround costs are high

Burst behavior matches DRAM's architectural strengths.

---

## Visibility to Software

Software never sees DDR commands directly.

Instead:

- CPUs issue abstract loads and stores
- Memory controllers translate them into DDR commands
- Timing rules are enforced in hardware

This abstraction is powerful — and dangerous.

When memory fails, software has no visibility into why.

---

## Why This Matters for OMI

OMI treats DDR commands as:

- A formalized contract between controller and memory
- An expression of DRAM's physical limits
- A design constraint for modules and layouts

Understanding the command set is required before:

- Interpreting timing parameters
- Understanding signal groups
- Designing termination and routing

---

## Takeaway

DDR is not just a fast bus.

It is a **carefully constrained command language** designed to keep fragile memory cells correct.

Every DDR command exists because DRAM demands it.

OMI documents this protocol so memory stops being magic.

---

**Reference:**  
ASIC implementation of DDR SDRAM Memory Controller - ResearchGate
