# The Open Memory Initiative (OMI)

The **Open Memory Initiative (OMI)** is a community-driven engineering project focused on making system memory **understandable, reproducible, and buildable**.

OMI approaches memory as a *first-class architectural system*, not a black box.
The project emphasizes **documentation-first design**, explicit constraints, and reproducible validation, starting with mature PC DDR technologies.

This is an **engineering-first, correctness-oriented effort**, not a product launch.

---

## Why OMI Exists

Open CPUs, SoCs, and accelerators are now common.
System memory is not.

Despite being fundamental to all computation, modern DRAM modules remain opaque, proprietary, and difficult to study or reproduce outside closed industrial contexts.

OMI exists to close this gap by providing:

- an open, reference-quality memory design
- a transparent engineering methodology
- documentation that explains *why* decisions were made, not just *what* was built

---

## Project Status

OMI is active and progressing deliberately.

### Completed

- Project charter and governance model
- Engineering methodology (architecture → constraints → implementation → validation)
- Public documentation of design philosophy and process
- Validation and review framework
- Layout and SI/PI design guidelines
- Minimal reference design definition

### In Progress

- Finalizing v1 memory target (DDR3 vs DDR4)
- Defining initial validation and bring-up platforms
- Preparing minimal reference schematic artifacts

OMI prioritizes **structural correctness and reproducibility** over speed.

---

## How OMI Is Engineered

OMI follows a documentation-first, staged engineering methodology designed to preserve correctness, clarity, and reproducibility from architecture through implementation.

There are two complementary documents describing this approach:

- 📄 **[How OMI Is Engineered (Repository Document)](./docs/how_omi_is_engineered.md)**A living, in-repo document that explains the engineering philosophy, stages, and internal structure of OMI. This is the canonical reference for contributors.

This document explains:

- the staged engineering process
- architectural decisions and constraints
- validation philosophy
- what "success" means for OMI

New contributors are strongly encouraged to read it first.

---

## Project Charter

OMI operates under a published charter that defines its purpose, scope, governance, and non-negotiable principles.

📄 **[CHARTER.md](./CHARTER.md)**

The charter exists to protect:

- openness
- long-term maintainability
- technical integrity

---

## Contributing

Contributions are welcome, but **discipline matters**.

Before contributing, please read:

- 📄 **[CHARTER.md](./CHARTER.md)** — purpose, scope, governance
- 📄 **[CONTRIBUTING.md](./CONTRIBUTING.md)** — how to participate and what is expected

Good ways to engage:

- Review architecture or validation documents
- Ask critical questions in GitHub Discussions
- Open issues for concrete, actionable topics

OMI values **careful review and precise feedback** more than rapid iteration.

---

## What OMI Is (and Is Not)

### OMI is:

- An open, community-driven engineering initiative
- Focused on real, buildable memory designs
- Documentation-heavy and charter-first
- Incremental and scope-disciplined

### OMI is not:

- A commercial product
- A vendor-specific effort
- A marketing project
- A shortcut to production hardware
- An NDA-gated or closed initiative

---

## Background & Motivation

The original motivation for OMI is described here:

**Open Memory Is Not a Luxury — Introducing the Open Memory Initiative (OMI)**
https://medium.com/@mefe.sensoy/open-memory-is-not-a-luxury-introducing-the-open-memory-initiative-omi-77d189299f6d

This essay provides historical and ecosystem context.
The repository documents the engineering reality.

---

## Governance

Technical direction is guided by:

- transparency
- documentation quality
- reproducibility
- long-term sustainability

Decisions are expected to be explainable and reviewable.

---

## License

Licensing details will be finalized as technical artifacts mature.

Until then, all contributions must comply with the openness and redistribution principles defined in the project charter.

---

## Questions & Discussion

- **GitHub Issues** → concrete, actionable topics
- **GitHub Discussions** → open-ended or architectural conversations

Clear questions help build a clear project.

---

> OMI values careful, transparent engineering over speed.
> Correctness first. Reproducibility always.
