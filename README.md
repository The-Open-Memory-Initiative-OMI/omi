<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# The Open Memory Initiative (OMI)

The **Open Memory Initiative (OMI)** is A place to take memory hardware apart and rebuild it in the open - the kind of end-to-end reference work usually locked behind paywalled JEDEC raw cards and vendor NDAs. Every design decision is documented, every artifact is reproducible, and claims match reality: work is described at exactly the stage it has reached (schematic, validated, …), never more.

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

OMI v1 is a **reviewable DDR4 UDIMM reference design**: 8 GB, single rank (1R), x8 DRAM devices, non-ECC (64-bit bus). **The schematic stage is complete.**

### ✅ Schematic capture — complete, ERC-clean, and netlisted

The OMI v1 schematic is captured in KiCad and **passes Electrical Rule Check with 0 violations — no exclusions, no waivers**:

- A real **288-pin DDR4 UDIMM card-edge connector (`J1`)**, pin-mapped from the JEDEC keystone pin map. The placeholder host connectors used during early capture have been **removed** — `J1` is the genuine module edge.
- **18 / 18 real components footprinted**: `J1` (288-pad card edge), 8× DDR4 SDRAM (FBGA-78), one SPD EEPROM (UDFN-8), and 8× ZQ calibration resistors (R1–R8, 240 Ω).
- ERC reaches 0 through **real connections** — datasheet-genuine no-connect flags on truly-NC balls, VSS ties on `TEN`/`PAR`, the eight mandatory ZQ resistors, and `PWR_FLAG`s on host-supplied rails — **not** through exclusions or waivers.
- A **generated netlist** (KiCad XML + s-expression), **BOM** (CSV), and **5-page schematic PDF** are checked in under [`exports/`](./exports/), produced by an export step **gated on the clean ERC**.

**Evidence (reproducible):** [`exports/`](./exports/) holds the netlist, BOM, PDF, and `erc.json` (0 violations); [`exports/MANIFEST.txt`](./exports/MANIFEST.txt) records the source commit, `kicad-cli` version, and a SHA-256 for every artifact. The KiCad source is at [`design/power/omi_v1_power/`](./design/power/omi_v1_power/). The step-by-step engineering record is in [`docs/implementations/`](./docs/implementations/).

### What "validated" means here — and what it does not

OMI v1 is a **schematic-stage** study. At this stage, "validation" means three real, reproducible things:

- **L0 — artifact integrity:** the 288/288 edge pin map and net naming pass automated checks ([`validation/evidence/l0_summary.md`](./validation/evidence/l0_summary.md)).
- **ERC-clean:** the electrical rule check passes with 0 violations ([`exports/erc.json`](./exports/erc.json)).
- **Export provenance:** every exported artifact is hashed and traceable to a commit ([`exports/MANIFEST.txt`](./exports/MANIFEST.txt)).

**No hardware has been built, populated, or measured.** The physical bench-validation levels (**L1–L4**) are **defined as procedures but not executed** — there is no board, and there are no measurements. Any "PASS" in the bench-validation *framework* is a tooling/procedure dry-run over a blank template, **not** a hardware result (see [`validation/evidence/l1_summary.md`](./validation/evidence/l1_summary.md)).

### Scope boundary — what is *not* here (the wall)

OMI v1 stops at a complete, ERC-clean schematic. The following are **out of scope and do not exist** in this repository:

- **PCB layout, Gerbers, and stack-up** — none produced.
- **Signal-integrity / power-integrity (SI/PI) simulation** — none performed.
- **A fabricated or bench-tested board** — none built; no measurements taken.

Two caveats **scope** (they do not negate) the completed schematic:

- **`J1` models the 288 numbered pads only.** Exact JEDEC notch position, card-edge outline, and pad-mechanical geometry are a layout/mechanical concern and are **unproven** here.
- **Label-on-pin connectivity.** Global net labels are anchored directly on `J1` pins. This is ERC-clean and correct, but it is a known KiCad structural quirk (it prevented directional pin retyping) and is flagged for future cleanup.

### How the schematic was reached — documentation stages

The completed schematic above was produced through OMI's staged, documentation-first method:

- **Stage 5 — Architecture Decisions** — OMI v1 direction locked (DDR4 UDIMM baseline).
- **Stage 6 — Block Decomposition** — power, CA/CLK, DQ/DQS, SPD, and mechanical blocks documented.
- **Stage 7 — Schematic Capture — complete** — design intent (7.1 power/PDN, 7.2 CA/CLK, 7.3 DQ/DQS byte-lanes, 7.4 SPD, 7.5 288/288 edge pin map, 7.6 interface summary, 7.7 closure) **realized** as the ERC-clean, footprint-complete, netlisted KiCad design described above.
- **Stage 8 — Validation & Bring-Up Strategy — documentation complete** — the L0–L4 ladder, platform strategy, bring-up procedure, test-point/DFT plan, failure-mode catalog, and review checklists are written. **L0 and ERC are satisfied today; physical L1–L4 execution awaits a fabricated board.**

### Beyond the wall — not started

- **Stage 9 — Minimal Reference Schematic refinements** (e.g. SPD hex image / EEPROM content) and **Stage 10 — Layout & SI/PI Guidelines** (PCB layout, impedance, stack-up, signal/power integrity). These are the stages that stand between this schematic and verifiable hardware, and they are **not started**.

OMI prioritizes **structural correctness and reproducibility** over speed.

---

## Repository Navigation

OMI is organized by engineering stages:

```
design/power/omi_v1_power/            ← KiCad schematic — the actual capture (J1 edge, DRAM, SPD, ZQ),
                                          omi.kicad_sym library, and the J1 card-edge footprint
exports/                              ← Generated netlist, BOM, schematic PDF, erc.json (0 violations), MANIFEST.txt
docs/05_power_delivery_and_pdn/       ← Power delivery & PDN assumptions
docs/06_signal_topology_and_routing/  ← Signal topology: CA/CLK, DQ/DQS, routing philosophy
docs/07_schematic_capture/            ← Stage 7: schematic-level intent and design rationale
docs/08_validation_and_review/        ← Stage 8: validation framework, procedures, checklists
docs/implementations/                 ← Phase-by-phase record of how the schematic was completed
docs/v1/                              ← OMI v1 decision docs (form factor, capacity, etc.)
design/connector/                     ← 288-pin UDIMM edge connector CSV pin map
validation/evidence/                  ← L0 artifact-integrity evidence (real) + L1 framework dry-run (not measurements)
validation/runs/                      ← Bench run logs (empty until a board is fabricated)
```

If you're new: start with the engineering method doc below, then skim the Stage 5–6 design docs, then read the completed schematic and its evidence in [`exports/`](./exports/).

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
- 📄 **[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)** — the conduct expected of everyone who participates

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

## Licensing

This project uses a multi-license approach to properly cover all content types.
Each license maps to a specific part of the repository:

| Content type | Applies to | License | File |
|---|---|---|---|
| Hardware design | `design/**` — schematics, PCB layouts, connector data, design artifacts | CERN Open Hardware Licence v2 — Strongly Reciprocal (CERN-OHL-S-2.0) | [`LICENSE`](LICENSE) |
| Documentation | `docs/**` and the root prose docs — charter, scope, methodology, learning materials | Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) | [`LICENSE-docs`](LICENSE-docs) |
| Software / code | `docs/08_validation_and_review/scripts/**` — validation scripts, test tooling, automation | Apache License 2.0 | [`LICENSE-software`](LICENSE-software) |

All contributions must comply with these licenses and with the openness and
redistribution principles defined in [CHARTER.md](CHARTER.md).

## Publications

- [OMI Enters Stage 8: Turning a DDR4 UDIMM Schematic into Verifiable Hardware](https://medium.com/@mefe.sensoy/omi-enters-stage-8-turning-a-ddr4-udimm-schematic-into-verifiable-hardware-c6d252b0e1d3)

  *Scope note:* this essay frames the project's **direction**. What this repository contains **today** is a complete, ERC-clean DDR4 UDIMM **schematic** with a generated netlist, BOM, and PDF — **not** fabricated or bench-verified hardware. Turning the schematic into *verifiable hardware* (layout, fabrication, bring-up) remains future work, beyond the current scope (see **Project Status → Scope boundary**, above).

---

## Questions & Discussion

- **[GitHub Issues](https://github.com/The-Open-Memory-Initiative-OMI/omi/issues)** → concrete, actionable topics
- **[GitHub Discussions](https://github.com/The-Open-Memory-Initiative-OMI/omi/discussions)** → open-ended or architectural conversations

Clear questions help build a clear project.

---

> OMI values careful, transparent engineering over speed.
> Correctness first. Reproducibility always.
