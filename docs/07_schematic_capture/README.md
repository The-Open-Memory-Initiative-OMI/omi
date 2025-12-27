# 07 — Schematic Capture

## Purpose

This directory contains the **schematic implementation** of **OMI v1**.

Stage 7 exists to **translate the fully locked architectural intent of Stage 6 into a complete, reviewable electrical schematic**.  
No new architecture, features, or assumptions are introduced here.

This is an **execution stage**, not a design exploration stage.

---

## Entry Conditions (Hard Gate)

Work in this directory may begin **only if**:

- Stage 5 (scope locking) is complete  
- Stage 6.1–6.7 (technical decomposition) is complete  
- Stage 6 closure has been explicitly declared  
- No open architectural or scope questions remain  

If any assumption is unclear, work must pause and documentation must be updated **before continuing**.

---

## Scope

This directory covers **schematic capture only**.

### Included
- Electrical schematics implementing all Stage 6 blocks  
- Explicit connectivity for power, signals, configuration, and connector  
- Clear signal naming, grouping, and documentation  
- Reviewable schematic artifacts (native files and PDFs)  

### Explicitly Excluded
- PCB layout or routing  
- Signal integrity or power integrity simulation  
- BOM cost optimization  
- Validation execution or testing  

Those belong to later stages.

---

## Design Philosophy

Schematic capture in OMI v1 follows these principles:

- **Fidelity over creativity**  
- **Completeness over speed**  
- **Clarity over compactness**  
- **Explicit behavior over implicit assumptions**  

A schematic that "probably works" but cannot be explained is considered incorrect.

---

## Rules of Engagement (Non-Negotiable)

While working in Stage 7:

- No new features may be added  
- No topology changes may be introduced  
- No assumptions may remain undocumented  
- No "just in case" circuitry is allowed  
- No optimization for performance is permitted  

If a schematic decision requires creativity, **stop** and revisit documentation.

Stage 7 implements decisions — it does not make them.

---

## Required Schematic Structure

Schematic pages **must mirror Stage 6 blocks**.

The expected page structure is:

1. **Power & PDN**
2. **Address / Command / Clock**
3. **Data Byte-Lane (template)**
4. **Data Byte-Lane Replication**
5. **SPD & I²C**
6. **Connector / Edge Interface**
7. **Notes & References**

Mixing unrelated concerns on the same page is not allowed.

---

## Review Philosophy

Schematic review focuses on:

- Conformance to Stage 6 documentation  
- Internal consistency and completeness  
- Signal traceability end-to-end  
- Power-up and reset behavior clarity  
- Debuggability and observability  

Performance, cost, or optimization are **not** review criteria at this stage.

A schematic passes review only if a reviewer can explain its behavior **without oral context**.

---

## Change Management

Once a schematic page is reviewed and accepted:

- It is considered **frozen**
- Changes require:
  - A documented reason
  - Identification of impacted Stage 6 assumptions
  - Explicit reviewer acknowledgment

Silent fixes are not allowed.

---

## Expected Outputs

Stage 7 produces:

- Complete schematic files
- PDF exports for review
- Review notes and resolutions
- A frozen, copper-ready schematic package

These outputs authorize progression to **Stage 8 — Validation & Bring-Up Execution**.

---

## Common Failure Modes (Avoid These)

- Starting with data lanes before power is defined  
- Relying on layout to "fix" schematic ambiguity  
- Leaving pins floating without explanation  
- Assuming controller behavior without documentation  
- Treating schematics as art instead of proof  

---

## Completion Criteria

Stage 7 is complete only when:

- Every Stage 6 block is traceable in the schematic  
- No undocumented assumptions remain  
- At least one structured schematic review is passed  
- The schematic is frozen for layout  

---

## One-Sentence Anchor

> **Stage 7 is where ambiguity is eliminated, not deferred.**

---

*This directory marks the transition from architectural intent to physical reality.*
