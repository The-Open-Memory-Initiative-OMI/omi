# OMI v1 — DDR3 vs DDR4 Technical Comparison

## Purpose

This document evaluates DDR3 and DDR4 as candidate memory technologies for OMI v1, using criteria aligned with the project's stated goals: openness, reproducibility, accessibility, and disciplined execution.

The objective is not to identify the "best" memory technology in general, but to determine which option best supports a first complete, buildable, and independently verifiable open DDR module design.

**Performance leadership and commercial competitiveness are explicitly out of scope.**

---

## Evaluation Criteria

The comparison is performed across the following axes:

- Platform availability and accessibility
- Tooling and documentation accessibility
- Signal integrity complexity and risk
- Validation and bring-up feasibility
- Contributor accessibility and educational value
- Longevity, relevance, and risk balance

Each axis is evaluated relative to OMI v1 objectives.

---

## Option A — DDR3

### Platform Availability

DDR3 is supported by a wide range of legacy and transitional PC platforms, including multiple generations of Intel and AMD consumer chipsets. While modern platforms are phasing it out, DDR3 systems remain widely available in secondary markets and academic environments.

BIOS-level configuration and SPD behavior are generally well understood, with extensive community documentation.

**Assessment:** High availability, decreasing future support.

### Tooling and Documentation

DDR3 benefits from long-standing public documentation, application notes, and community-level troubleshooting knowledge. Measurement expectations, termination schemes, and routing practices are broadly understood.

Publicly accessible reference material is more abundant relative to DDR4.

**Assessment:** Very strong documentation accessibility.

### Signal Integrity Complexity

DDR3 operates at lower data rates and voltages compared to DDR4. As a result:

- Timing margins are wider
- Routing constraints are more forgiving
- SI failures are more diagnosable

This reduces risk for a first open implementation and simplifies validation.

**Assessment:** Lower SI risk and complexity.

### Validation and Bring-Up

DDR3 bring-up is generally tolerant to minor layout and parameter imperfections. Training behavior is simpler, and failures are more likely to be observable and repeatable.

This makes DDR3 attractive for a community-driven validation effort with heterogeneous tooling.

**Assessment:** High feasibility, low barrier to validation.

### Contributor Accessibility & Educational Value

DDR3 aligns well with educational objectives:

- Easier to explain end-to-end
- More approachable for first-time DDR designers
- Lower tooling and platform barriers

However, some contributors may perceive DDR3 as less relevant to current industry practice.

**Assessment:** Excellent accessibility, moderate perceived relevance.

### Longevity and Risk Balance

DDR3 is a mature and stable technology but is no longer the industry's forward direction. The primary risk is reduced long-term applicability rather than technical uncertainty.

**Assessment:** Low technical risk, higher obsolescence risk.

---

## Option B — DDR4

### Platform Availability

DDR4 is supported by a wide range of modern and currently shipping PC platforms. It is the dominant memory technology for contemporary desktop and laptop systems.

However, platform behavior (especially training and SPD handling) can be more platform-specific and opaque.

**Assessment:** Very high availability, higher platform variability.

### Tooling and Documentation

While DDR4 standards are publicly available, practical implementation details are often more fragmented. Many reference designs and best practices exist primarily behind vendor documentation or NDAs.

Community-level open documentation is less comprehensive than DDR3.

**Assessment:** Adequate but less transparent documentation.

### Signal Integrity Complexity

DDR4 introduces:

- Higher data rates
- Lower voltage swings
- Tighter timing margins
- Increased sensitivity to layout and PDN quality

This significantly increases the risk surface for a first open design.

**Assessment:** High SI complexity and tighter margins.

### Validation and Bring-Up

DDR4 bring-up depends heavily on memory training algorithms implemented in firmware and memory controllers. Failures can be less deterministic and harder to isolate without advanced tools.

This raises the bar for reproducibility across contributors.

**Assessment:** Feasible but higher validation risk.

### Contributor Accessibility & Educational Value

DDR4 offers strong relevance to modern systems and future work. However, the increased complexity may discourage less experienced contributors or slow early momentum.

**Assessment:** High relevance, lower accessibility.

### Longevity and Risk Balance

DDR4 offers better medium-term relevance and continuity. The risk lies not in obsolescence, but in increased execution difficulty for a first iteration.

**Assessment:** High relevance, higher execution risk.

---

## Comparative Summary

| Criterion                  | DDR3      | DDR4      |
|----------------------------|-----------|-----------|
| Platform accessibility     | High      | Very high |
| Documentation openness     | Very high | Moderate  |
| SI complexity              | Lower     | Higher    |
| Bring-up risk              | Lower     | Higher    |
| Contributor accessibility  | Very high | Moderate  |
| Educational clarity        | High      | High      |
| Long-term relevance        | Lower     | Higher    |
| Overall execution risk     | Lower     | Higher    |

---

## Alignment with OMI v1 Goals

OMI v1 prioritizes:

- A completed design over an ambitious one
- Reproducibility over performance
- Transparency over novelty

Under these constraints:

- **DDR3** minimizes execution and validation risk
- **DDR4** maximizes relevance but increases technical and organizational risk

This trade-off defines the core decision.

---

## Non-Implications of This Decision

Selecting either DDR3 or DDR4 for OMI v1:

- Does **not** imply exclusion of other DDR generations in future versions
- Does **not** represent a judgment on technical superiority
- Does **not** constrain future scope expansion

It is a **v1 scoping decision only**.

---

## Decision Record

The final decision and its justification will be recorded here once Issue #1 is resolved. The rejected option will be documented with explicit reasoning to preserve institutional memory.

---

**Status:** Draft — used to support Stage 5.1 decision discussion  
**Owner:** OMI Maintainers  
**Scope:** OMI v1 only
