# OMI v1 — DDR4 Acceptance Conditions

## Status
Proposed

## Scope
OMI Version 1 only

## Authority
OMI Maintainers

## Related
- Stage 5.1 — DDR Generation Decision
- GitHub Issue #1 — DDR3 vs DDR4 Selection

---

## 1. Purpose

This document defines the **non-negotiable acceptance conditions** under which **DDR4** is selected as the memory technology for **OMI v1**.

These conditions exist to ensure that choosing a more modern and complex technology does **not violate** OMI's core principles of:

- Openness  
- Reproducibility  
- Engineering transparency  
- Completion over ambition  

DDR4 is accepted **only insofar as all conditions in this document are respected**.

If these conditions cannot be upheld, the DDR generation decision **must be revisited**.

---

## 2. Scope Containment (No Feature Drift)

OMI v1 DDR4 **MUST** be constrained to a single, conservative operating point.

The design MUST include:

- Exactly one JEDEC data rate  
- Exactly one voltage point  
- Exactly one JEDEC timing profile  

The design MUST NOT include:

- XMP, EXPO, or vendor-specific extensions  
- Overclocking or performance tuning  
- Multiple selectable operating modes  

**Rationale:**  
Multiple operating points obscure failure analysis and undermine reproducibility.

---

## 3. Platform Assumptions Must Be Explicit

OMI v1 DDR4 is **NOT REQUIRED** to operate on all DDR4-capable systems.

The project MUST explicitly document:

- A reference platform class  
- CPU generation assumptions  
- Chipset assumptions  
- BIOS / firmware behavioral dependencies  

Platform behavior MUST be treated as a **variable**, not a guarantee.

**Rationale:**  
Universal compatibility is not achievable without vendor cooperation.  
Reproducibility under stated conditions is sufficient.

---

## 4. Memory Training Is Not a Black Box

DDR4 memory training MUST be treated as an **observable and documentable system**.

The project MUST:

- Document training success cases  
- Document training failure cases  
- Record platform-specific training behavior  
- Treat failure to train as valid engineering data  

The project MUST NOT:

- Hide training failures  
- Assume training behavior without evidence  

**Rationale:**  
Memory training is one of the least transparent aspects of modern DDR systems.  
OMI documents reality, not idealized behavior.

---

## 5. Signal Integrity Conservatism

Design decisions MUST bias toward **margin and robustness**, not density or speed.

The design MUST favor:

- Conservative routing constraints  
- Conservative impedance targets  
- Conservative PDN assumptions  

No design choice may be justified solely by "expected behavior" or "industry norm" without documented rationale.

Where trade-offs exist, the safer option MUST be preferred unless evidence supports increased risk.

**Rationale:**  
Tighter margins are the primary technical risk of DDR4 and must be managed explicitly.

---

## 6. Failure Is a First-Class Outcome

OMI v1 DDR4 does **NOT** define success as universal operability.

Valid outcomes include:

- Partial platform compatibility  
- Platform-specific failures  
- Marginal or conditional behavior  

All failures MUST be documented with the same rigor as successful operation.

**Rationale:**  
Unreported failure is technical debt.  
Documented failure is engineering knowledge.

---

## 7. Tooling Reality and Openness

OMI v1 DDR4 MUST NOT assume access to:

- NDA-restricted documentation  
- Proprietary validation tools  
- Vendor-only measurement equipment  

Validation procedures MUST be reproducible using:

- Public documentation  
- Standard lab equipment  

If advanced tooling is beneficial, the project MUST document:

- Why it is beneficial  
- What limitations exist without it  

**Rationale:**  
An open design that requires closed tools is not open in practice.

---

## 8. Educational Value Over Optimization

The DDR4 design MUST remain explainable end-to-end.

The project MUST:

- Document design intent in human-readable terms  
- Explain trade-offs explicitly  
- Preserve clarity over sophistication  

Complexity MUST serve understanding, not optimization.

**Rationale:**  
OMI exists to transfer understanding, not to demonstrate technical bravado.

---

## 9. Completion Takes Priority Over Perfection

If a design decision threatens timely completion of a:

- Buildable  
- Documented  
- Validated  

artifact, it MUST be reconsidered.

This includes risks related to:

- Component availability  
- Validation dead-ends  
- Platform dependencies that cannot be documented  

**Rationale:**  
An incomplete modern design helps fewer people than a completed conservative one.

---

## 10. Non-Implications of DDR4 Selection

Selecting DDR4 for OMI v1 does **NOT** imply:

- Performance competitiveness with commercial DIMMs  
- Coverage of all DDR4 platforms  
- Industrial best-practice optimization  
- Commitment to future DDR generations  

This is a **v1 execution decision**, not a roadmap guarantee.

---

## 11. Closing Statement

DDR4 is accepted for OMI v1 **not because it is newer**, but because it can be explored **honestly, conservatively, and transparently** within the constraints defined in this document.

If these constraints cannot be maintained, the DDR generation decision must be re-evaluated.

---

*End of document*
