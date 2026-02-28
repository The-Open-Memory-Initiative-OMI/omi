# The Open Memory Initiative (OMI)

The **Open Memory Initiative (OMI)** is a community-driven engineering project focused on making system memory **understandable, reproducible, and buildable**.

OMI treats memory as a *first-class architectural system*, not a black box.
The project emphasizes **documentation-first design**, explicit constraints, and reproducible validation - starting with mature PC DDR technologies.

This is an **engineering-first, correctness-oriented effort**, not a product launch.

---

## New here?

📄 **[START_HERE.md](./START_HERE.md)** — Beginner-friendly onboarding guide with contribution tracks, starter tasks, and a full repository map.

---

## Why OMI Exists

Open CPUs, SoCs, and accelerators are now common. System memory is not.

Despite being fundamental to computation, modern DRAM modules remain opaque, proprietary, and difficult to study or reproduce outside closed industrial contexts.

OMI exists to close this gap by providing:

- An open, reference-quality memory design target
- A transparent engineering methodology
- Documentation that explains *why* decisions were made, not just *what* was built

---

## Project Status

OMI is active and progressing deliberately. The OMI v1 target is a **reviewable DDR4 UDIMM reference design**: 8 GB, single rank (1R), x8 DRAM devices, non-ECC (64-bit bus).

### Completed

- Project charter, governance model, and contribution workflow
- Staged engineering approach (architecture → blocks → schematic capture → validation)
- **Stage 5 — Architecture Decisions** — OMI v1 direction locked (DDR4 UDIMM baseline)
- **Stage 6 — Block Decomposition** — all core blocks documented and closure declared (power, CA/CLK, DQ/DQS, SPD, mechanical, validation plan)
- **Stage 7 — Schematic Capture — complete and frozen:**
  - 7.1 Power & PDN (frozen)
  - 7.2 Address/Command/Clock (frozen — simplified star representation; fly-by enforced at layout)
  - 7.3 Data (DQ/DQS) byte-lanes (frozen — per-DRAM net naming D0…D7)
  - 7.4 SPD & Configuration (frozen — host pull-ups; WP tied low)
  - 7.5 UDIMM Edge Pin Map (frozen — 288/288 pins mapped, no duplicates, no missing)
  - 7.6 Interface Summary (frozen)
  - 7.7 Stage 7 Closure (frozen — quality gates passed, handoff to Stage 8)

### In Progress

- **Stage 8 — Validation & Bring-Up Strategy**
  - Validation platform selection
  - Bring-up procedure definition
  - Success criteria and failure mode documentation
  - Review checklists and structured reporting templates

### Upcoming

- **Stage 9** — Minimal Reference Schematic (correctness-first, one rank, no optimizations)
- **Stage 10** — Layout & SI/PI Guidelines

OMI prioritizes **structural correctness and reproducibility** over speed.

---

## Repository Navigation

OMI is organized by engineering stages:

```
docs/05_architecture_decisions/   ← Stage 5: what we build and why
docs/06_block_decomposition/      ← Stage 6: power, CA/CLK, DQ/DQS, SPD, mechanical
docs/07_schematic_capture/        ← Stage 7: schematic-level intent (frozen)
docs/08_validation_and_review/    ← Stage 8: validation checklists and review
docs/v1/                          ← OMI v1 decision docs (form factor, capacity, etc.)
design/connector/                 ← 288-pin UDIMM edge connector CSV mapping
```

If you're new: start with the engineering method doc below, then skim Stage 5 decisions, then follow Stage 7 artifacts.

---

## How OMI Is Engineered

OMI follows a documentation-first, staged engineering methodology designed to preserve correctness, clarity, and reproducibility from architecture through implementation.

📄 **[How OMI Is Engineered](./docs/how_omi_is_engineered.md)** — the canonical reference for contributors. It explains the staged process, architectural constraints, validation philosophy, and what "success" means for OMI.

New contributors are strongly encouraged to read it first.

---

## Project Charter

OMI operates under a published charter that defines its purpose, scope, governance, and non-negotiable principles.

📄 **[CHARTER.md](./CHARTER.md)**

The charter protects openness, long-term maintainability, and technical integrity.

---

## Contributing

Contributions are welcome, but **discipline matters**.

Before contributing, please read:

- 📄 **[START_HERE.md](./START_HERE.md)** — onboarding, tracks, and starter tasks
- 📄 **[CHARTER.md](./CHARTER.md)** — purpose, scope, governance
- 📄 **[CONTRIBUTING.md](./CONTRIBUTING.md)** — how to participate and what is expected

Good ways to engage:

- Review Stage 5–7 documents and challenge assumptions
- Ask critical questions in GitHub Discussions
- Open issues for concrete, actionable topics (with clear acceptance criteria)
- Pick a contribution track (developer, reviewer, or tester) from [START_HERE.md](./START_HERE.md)

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

The original motivation for OMI is described in these essays:

- [Open Memory Is Not a Luxury — Introducing the Open Memory Initiative (OMI)](https://medium.com/@mefe.sensoy/open-memory-is-not-a-luxury-introducing-the-open-memory-initiative-omi-77d189299f6d)
- [The Open Memory Initiative (OMI): Toward an Open, Reproducible DDR Memory Module](https://www.linkedin.com/pulse/open-memory-initiative-omi-toward-reproducible-ddr-module-%C5%9Fensoy-8aqee/?trackingId=GKHgAhggTk2MHWIAghdTHw%3D%3D)

These provide historical and ecosystem context. The repository documents the engineering reality.

---

## Governance

Technical direction is guided by transparency, documentation quality, reproducibility, and long-term sustainability. Decisions are expected to be explainable and reviewable.

See [CHARTER.md](./CHARTER.md) for the full governance model.

---

## License

Licensing details will be finalized as technical artifacts mature.

Until then, all contributions must comply with the openness and redistribution principles defined in the project charter.

---

## Questions & Discussion

- **[GitHub Issues](https://github.com/The-Open-Memory-Initiative-OMI/omi/issues)** → concrete, actionable topics
- **[GitHub Discussions](https://github.com/The-Open-Memory-Initiative-OMI/omi/discussions)** → open-ended or architectural conversations

Clear questions help build a clear project.

---

> OMI values careful, transparent engineering over speed.
> Correctness first. Reproducibility always.
