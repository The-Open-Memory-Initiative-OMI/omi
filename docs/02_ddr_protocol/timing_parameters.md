# DDR Timing Parameters: Why These Numbers Exist

This document explains the **purpose and meaning of DDR timing parameters**.

Rather than listing values, it focuses on **why each class of timing constraint exists**, what architectural or physical reality it protects, and what happens when it is violated.

DDR timings are not performance knobs.  
They are **correctness constraints**.

---

## Why DDR Needs Timing Parameters at All

DRAM is not a synchronous digital register file.

It is:

- Analog at its core
- Physically fragile
- Sensitive to voltage, noise, and temperature
- Dependent on shared internal resources

DDR timing parameters exist to ensure that:

- Destructive reads are fully restored
- Sense amplifiers settle correctly
- Rows are isolated safely
- Charge retention guarantees are preserved

Violating timing does not degrade gracefully.
It corrupts data.

---

## Categories of DDR Timing Parameters

DDR timings can be grouped by **what they protect**:

1. Row activation and restoration
2. Row switching and isolation
3. Column access and data transfer
4. Refresh and retention
5. Bus and turnaround behavior

Each category maps directly to DRAM architecture.

---

## Row Activation Timings

### tRCD - Row to Column Delay

**What it protects:**  
Time required for sense amplifiers to fully detect and amplify cell charge after activation.

**Why it exists:**  
After ACT:

- Voltage differences are extremely small
- Sense amplifiers need time to settle
- Restoration must begin before column access

**If violated:**  

- Data is read before it is stable
- Incorrect values may be latched
- Errors may be silent or delayed

---

### tRAS - Row Active Time

**What it protects:**  
Minimum time a row must remain active to ensure full restoration.

**Why it exists:**  
Restoration of charge into DRAM cells takes time.
Closing a row too early leaves cells undercharged.

**If violated:**  

- Data may appear correct initially
- Retention time is reduced
- Errors occur later, far from the cause

---

## Row Switching Timings

### tRP - Row Precharge Time

**What it protects:**  
Time required to safely close a row and neutralize bitlines.

**Why it exists:**  
Precharge:

- Disconnects cells from sense amplifiers
- Equalizes bitlines
- Prepares the bank for the next activation

**If violated:**  

- Residual charge interferes with next activation
- Data corruption occurs across rows

---

### tRC - Row Cycle Time

**What it protects:**  
Complete ACT → access → PRE cycle.

**Why it exists:**  
It ensures:

- Restoration completes
- Isolation completes
- The array is in a known-safe state

tRC is not arbitrary; it is the full cost of a row operation.

---

## Column Access Timings

### CAS Latency (CL)

**What it protects:**  
Time between READ command and valid data availability.

**Why it exists:**  
After column selection:

- Data must propagate from row buffer
- Through internal multiplexers
- Onto the external bus

**If violated:**  

- Data is sampled before it is valid
- Bit errors appear immediately

---

### tWR - Write Recovery Time

**What it protects:**  
Time required to safely store written data before closing the row.

**Why it exists:**  
WRITE operations overwrite stored charge.
Cells must stabilize before precharge.

**If violated:**  

- Written data may decay prematurely
- Corruption may occur on subsequent reads

---

## Bank and Parallelism Timings

### tRRD - Row-to-Row Delay

**What it protects:**  
Power and current limits during multiple activations.

**Why it exists:**  
Activating rows draws significant current.
Too many simultaneous activations cause:

- Voltage droop
- Sense amplifier instability

**If violated:**  

- Data corruption across banks
- System-wide instability

---

### tFAW - Four Activate Window

**What it protects:**  
Aggregate power integrity.

**Why it exists:**  
Limits the number of ACT commands in a time window.

This is a **power integrity constraint**, not a logical one.

---

## Refresh Timings

### tREFI - Refresh Interval

**What it protects:**  
Maximum allowable time between refreshes.

**Why it exists:**  
Cells leak charge continuously.
Worst-case retention determines refresh frequency.

**If violated:**  

- Gradual data decay
- Silent corruption

---

### tRFC - Refresh Cycle Time

**What it protects:**  
Time required to refresh rows internally.

**Why it exists:**  
Refresh blocks normal access and performs:

- Activation
- Sensing
- Restoration

**If violated:**  

- Incomplete refresh
- Long-term data loss

---

## Why Timing Violations Are So Dangerous

Timing violations often:

- Do not fail immediately
- Affect only marginal cells
- Appear workload-dependent
- Surface long after the violation

This disconnect between cause and effect is why:

- Memory bugs are hard to debug
- Marginal designs pass basic tests
- Validation must be conservative

---

## Why Timing Parameters Are Conservative

DDR timings assume:

- Worst-case silicon
- Highest temperature
- Lowest voltage
- Maximum noise
- Long-term aging

These margins are not inefficiency.
They are survival buffers.

---

## Implications for Module-Level Design

At the module level:

- Signal integrity affects setup/hold margins
- Power integrity affects activation timing
- Skew affects perceived timing relationships

Poor module design effectively **shrinks timing margins**.

OMI documents timing to show:

- Which margins are structural
- Which are design-dependent
- Which are negotiable and which are not

---

## Takeaway

DDR timing parameters are not tuning values.
They are **encoded physics and architecture constraints**.

Every timing exists because:

- DRAM is fragile
- Reads are destructive
- Restoration is slow
- Margins are narrow

Understanding timings is understanding DRAM itself.
