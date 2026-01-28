
# The Open Memory Initiative (OMI)

The **Open Memory Initiative (OMI)** is a community-driven engineering project focused on making system memory **understandable, reproducible, and buildable**.

OMI treats memory as a *first-class architectural system*, not a black box.
The project emphasizes **documentation-first design**, explicit constraints, and reproducible validation—starting with mature PC DDR technologies.

This is an **engineering-first, correctness-oriented effort**, not a product launch.

---

## Why OMI Exists

Open CPUs, SoCs, and accelerators are now common.
System memory is not.

Despite being fundamental to computation, modern DRAM modules remain opaque, proprietary, and difficult to study or reproduce outside closed industrial contexts.

OMI exists to close this gap by providing:

- an open, reference-quality memory design target
- a transparent engineering methodology
- documentation that explains *why* decisions were made, not just *what* was built

---

## Project Status

OMI is active and progressing deliberately. Current work is focused on shipping a **reviewable DDR4 UDIMM reference schematic set** (starting from power → CA/CLK → DQ/DQS) and then moving into SPD + bring-up strategy.

### Completed

- Project charter and governance model
- Contribution workflow and participation baseline
- Staged engineering approach (architecture → blocks → schematic capture → validation)
- **Stage 5 (Architecture Decisions) — locked OMI v1 direction** (DDR4 UDIMM baseline)
- **Stage 6 (Block Decomposition) — core technical blocks documented** (power, CA/CLK, SPD/config, etc.)
- **Stage 7 schematic capture progress**
  - **7.1 Power & PDN — completed and frozen**
  - **7.2 Address/Command/Clock — completed and frozen (schematic uses simplified star representation; routing topology deferred to layout constraints)**
  - **7.3 Data (DQ/DQS) byte-lanes — completed and frozen with per-DRAM net naming (D0…D7) to prevent accidental shorts**

### In Progress

- **Stage 7.4 — SPD & Configuration schematic**
- **Stage 6 remaining blocks and closure**
  - mechanical/connector interface doc refinements
  - validation & bring-up strategy doc completion
  - block interface summary + closure pass
- **Validation platform definition + bring-up plan**
- Converting placeholders into **pin-accurate UDIMM connector mapping** as documentation and review maturity increases

OMI prioritizes **structural correctness and reproducibility** over speed.

---

## Repository Navigation

OMI is organized by engineering stages:

- `docs/05_architecture_decisions/` — Stage 5 decisions (what we build and why)
- `docs/06_block_decomposition/` — Stage 6 blocks (power, CA/CLK, SPD, mechanical, validation plan)
- `docs/07_schematic_capture/` — Stage 7 schematic capture (power, CA/CLK, DQ/DQS, SPD next)

If you're new: start with the engineering method doc below, then skim Stage 5 decisions, then follow Stage 7 artifacts.

---

## How OMI Is Engineered

OMI follows a documentation-first, staged engineering methodology designed to preserve correctness, clarity, and reproducibility from architecture through implementation.

- 📄 **[How OMI Is Engineered (Repository Document)](./docs/how_omi_is_engineered.md)** — A living, in-repo document that explains the engineering philosophy, stages, and internal structure of OMI. This is the canonical reference for contributors.

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

- Review Stage 5–7 documents and challenge assumptions
- Ask critical questions in GitHub Discussions
- Open issues for concrete, actionable topics (with clear acceptance criteria)

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

**The Open Memory Initiative (OMI): Toward an Open, Reproducible DDR Memory Module**
https://www.linkedin.com/pulse/open-memory-initiative-omi-toward-reproducible-ddr-module-%C5%9Fensoy-8aqee/?trackingId=GKHgAhggTk2MHWIAghdTHw%3D%3D

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
