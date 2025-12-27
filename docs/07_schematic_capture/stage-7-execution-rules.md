# Stage 7 — Schematic Capture Execution Rules (OMI v1)

## Status
Locked for OMI v1

## Scope
Applies to **Stage 7 — Schematic Capture only**

## Authority
OMI Maintainers

---

## 1. Purpose

This document defines the **execution rules** for Stage 7 — Schematic Capture.

Its purpose is to:
- Prevent scope creep
- Eliminate ambiguity
- Enforce review discipline
- Ensure that schematic work is a **faithful implementation** of Stage 6

This document is **procedural**, not architectural.  
It does not introduce design decisions — it governs *how* decisions are implemented.

---

## 2. Preconditions (Hard Gate)

Stage 7 work may proceed **only if**:

- Stage 5 (Scope Locking) is complete
- Stage 6.1–6.7 (Technical Decomposition) is complete
- Stage 6 closure has been explicitly declared
- No open architectural questions remain

If any assumption is unclear, schematic work must stop and documentation must be updated **before continuing**.

---

## 3. Schematic Page Structure (Locked)

The schematic MUST be organized into the following pages, in this order:

1. **Power & PDN**
   - All power rails, references, grounding, decoupling intent
2. **Address / Command / Clock**
   - CA signals, CK/CK#, CKE, CS#, RESET#, ODT
3. **Data Byte-Lane — Template**
   - One complete x8 DRAM device
4. **Data Byte-Lane — Replication**
   - Replicated lanes only, no unique logic
5. **SPD & I²C**
   - SPD EEPROM, pull-ups, addressing
6. **Connector / Edge Interface**
   - UDIMM edge fingers, external connectivity
7. **Notes & References**
   - JEDEC notes, assumptions, cross-references

### Rules
- No page may mix unrelated concerns
- Power signals must not be defined on non-power pages
- Replicated pages must explicitly state that they are replicated
- New pages may not be added without review

---

## 4. Naming Conventions (Locked)

### 4.1 Power Nets

JEDEC-standard names must be used exactly:

- `VDD`
- `VDDQ`
- `VPP`
- `VREF`
- `GND`

Rules:
- No aliases or local variants without justification
- All power consumers must connect to one of these named rails
- No implied power connections

---

### 4.2 Address / Command / Clock Signals

Use JEDEC naming conventions:

- Address: `A[ ]`
- Bank: `BA[ ]`, `BG[ ]`
- Commands: `RAS#`, `CAS#`, `WE#`
- Clock: `CK`, `CK#`
- Control: `CS#`, `CKE`, `RESET#`, `ODT`

Rules:
- Active-low signals must include `#`
- No renaming for convenience
- All signals must be explicitly connected or explicitly unused

---

### 4.3 Data Byte-Lanes

Lane-based naming is mandatory:

- `DQ0[0..7]`, `DQS0`, `DQS0#`
- `DQ1[0..7]`, `DQS1`, `DQS1#`
- …
- `DM0`, `DM1`, etc., if applicable

Rules:
- No data signal may exist outside a byte-lane context
- All lanes must be logically equivalent
- Any asymmetry is a bug unless documented

---

### 4.4 Page Naming

- Page names reflect **function**, not author preference
- Replicated pages must clearly indicate replication
- Notes pages must not introduce new connectivity

---

## 5. Review Cadence (Locked)

Stage 7 uses **page-gated reviews**.

| Page | Review Required Before Proceeding |
|----|----------------------------------|
| Power & PDN | **Yes (hard gate)** |
| Address / Command / Clock | Yes |
| Data Byte-Lane — Template | **Yes (hard gate)** |
| Data Byte-Lane — Replication | Spot-check |
| SPD & I²C | Yes |
| Connector / Edge Interface | Yes |
| Notes & References | Optional |

### Review Rules
- Downstream pages may not begin until upstream pages are approved
- Approval means:
  - No undocumented assumptions
  - No floating pins
  - Behavior explainable without oral context
- Approved pages are considered **frozen**

---

## 6. Change Management

Once a schematic page is approved:

- It is considered frozen
- Changes require:
  - A documented reason
  - Identification of impacted assumptions
  - Explicit reviewer acknowledgment

Silent fixes are not permitted.

---

## 7. Prohibited Behaviors

The following are explicitly prohibited during Stage 7:

- Adding features or options
- Changing topology
- Introducing "just in case" circuitry
- Relying on layout to resolve ambiguity
- Assuming controller or BIOS behavior without documentation

If a decision feels creative, Stage 7 has already been violated.

---

## 8. Completion Criteria for Stage 7

Stage 7 is considered complete only when:

- A full, reviewable schematic exists
- Every Stage 6 block is traceable in the schematic
- No undocumented assumptions remain
- At least one structured schematic review has passed
- The schematic is explicitly frozen

Only then may the project proceed to **Stage 8 — Validation & Bring-Up Execution**.

---

## 9. One-Sentence Anchor

> **Stage 7 execution exists to eliminate ambiguity, not to invent solutions.**

---

*End of document*
