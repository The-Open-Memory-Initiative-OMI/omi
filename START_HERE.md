<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Start Here

Welcome to the Open Memory Initiative.

OMI is building an **open, reference-quality DDR4 UDIMM**, and the **schematic stage is now complete** — a real 288-pin edge connector, ERC-clean (0 violations), with a generated netlist, BOM, and schematic PDF. The work spans architecture decisions, schematic capture, and a documented validation strategy. Everything is public, everything is documented, and every decision has a rationale you can read. (No board has been fabricated yet — layout, fabrication, and bench bring-up remain future work.)

This guide will help you understand the project, find your way around the repository, and start contributing.

---

## What OMI is building

OMI v1 targets a **DDR4 UDIMM** (desktop unbuffered DIMM):

- **8 GB total**, single rank (1R), x8 DRAM devices, non-ECC (64-bit bus)
- DDR4 UDIMM form factor (chosen for debuggability, platform access, and reproducibility)
- Host-supplied power rails (VDD, VDDQ, VPP) — no on-DIMM regulation
- SPD EEPROM for module identification

This is not a commercial product. It is a **reference-quality engineering artifact** designed to be understood, reviewed, and reproduced.

---

## How the project is structured

OMI follows a **staged engineering methodology**. Each stage builds on the previous one, and nothing moves forward until the current stage is documented and reviewable.

| Stage | Name | Status |
|:---:|:---|:---|
| 5 | Architecture Decisions | ✅ Locked |
| 6 | Block Decomposition | ✅ Core blocks documented |
| 7 | Schematic Capture | ✅ **Complete** — real 288-pin `J1`, ERC-clean (0), 18/18 footprinted, netlist/BOM/PDF in `exports/` |
| 8 | Validation & Review | ✅ Strategy documented; L0 + ERC satisfied — physical L1–L4 await a fabricated board |
| 9 | Minimal Reference Schematic | ⏳ Not started (beyond the wall) |
| 10 | Layout & SI/PI Guidelines | ⏳ Not started (beyond the wall) |

To understand the full engineering philosophy, read:

📄 **[How OMI Is Engineered](./docs/how_omi_is_engineered.md)** — the canonical reference for the staged process, design philosophy, and what "success" means for OMI.

---

## Repository map

```
omi/
├── CHARTER.md                          ← Purpose, scope, governance, principles
├── CONTRIBUTING.md                     ← How to participate and what is expected
├── START_HERE.md                       ← You are here
│
├── design/
│   ├── power/omi_v1_power/             ← KiCad schematic — the ACTUAL capture
│   │                                      (J1 edge, DRAM, SPD, ZQ) + omi.kicad_sym + footprint
│   └── connector/
│       └── ddr4_udimm_288_pinmap.csv   ← 288-pin UDIMM edge connector mapping
│
├── exports/                            ← Generated netlist, BOM, schematic PDF,
│                                          erc.json (0 violations), MANIFEST.txt
│
├── docs/
│   ├── how_omi_is_engineered.md        ← Engineering methodology (read this first)
│   │
│   ├── 05_power_delivery_and_pdn/      ← Power delivery & PDN assumptions
│   ├── 06_signal_topology_and_routing/ ← Signal topology: CA/CLK, DQ/DQS, routing philosophy
│   │
│   ├── 07_schematic_capture/           ← Stage 7: schematic-level intent & design rationale
│   │   ├── stage-7-1-power-final.md
│   │   ├── stage-7-2-ca-clk-final.md
│   │   ├── stage-7-3-dq-dqs-final.md
│   │   ├── stage-7-4-spd-final.md
│   │   ├── stage-7-5-edge-pinmap-final.md
│   │   ├── stage-7-6-interface-summary.md
│   │   └── stage-7-7-stage-7-closure.md
│   │
│   ├── 08_validation_and_review/       ← Stage 8: validation framework & checklists
│   ├── implementations/                ← Phase-by-phase record of the completed schematic
│   └── v1/                             ← OMI v1 decision docs (form factor, capacity, etc.)
│
└── validation/
    ├── evidence/                       ← L0 artifact-integrity (real) + L1 framework dry-run (not measurements)
    └── runs/                           ← Bench run logs (empty until a board is fabricated)
```

---

## Recommended reading order

If you're new, follow this path:

1. **[How OMI Is Engineered](./docs/how_omi_is_engineered.md)** — understand the methodology and philosophy
2. **[CHARTER.md](./CHARTER.md)** — understand the project's scope, principles, and governance
3. **[Power delivery & PDN](./docs/05_power_delivery_and_pdn/)** — rails, sourcing, and PDN assumptions
4. **[Signal topology & routing](./docs/06_signal_topology_and_routing/)** — CA/CLK, DQ/DQS, and routing philosophy
5. **[Stage 7 schematics](./docs/07_schematic_capture/)** — schematic-level design rationale; the completed KiCad design itself lives in [`design/power/omi_v1_power/`](./design/power/omi_v1_power/), with generated outputs in [`exports/`](./exports/)

You do not need to read everything before contributing. But you should understand the stage your work touches.

---

## Pick a track

OMI has three contribution tracks. You can contribute meaningfully regardless of your background.

### ⚡ Track 1 — Developers (tooling + automation + docs)

You can contribute without touching hardware.

**What you'll do:**
- Build linters and checkers (naming rules, consistency checks, schema validation)
- Improve documentation pipelines (doc generation, CI, templates)
- Create traceability helpers that connect specs → schematics → validation

**Good fit if you like:** Python, CI/CD, GitHub Actions, docs engineering, automation.

**Starter tasks:**
- Validate that all Stage 7 docs reference the correct artifact filenames
- Build a script that checks the pin map CSV for duplicates or missing entries
- Add a CI check that all markdown files have a `## Status` field

---

### 🔍 Track 2 — Reviewers (correctness + clarity + scope enforcement)

You help keep OMI coherent.

**What you'll do:**
- Review docs and specs for internal consistency and missing assumptions
- Check that decisions are justified and properly scoped
- Turn observations into structured review notes and actionable issues

**Good fit if you like:** systems thinking, correctness, design review, documentation quality.

**Starter tasks:**
- Read a Stage 6 block doc and check whether all stated assumptions are also reflected in Stage 7
- Review the Stage 7 closure doc and verify the artifact index is complete and links resolve
- Identify any decision that lacks an explicit rationale and open an issue

---

### 🧪 Track 3 — Testers (validation evidence + reproducible reports)

You turn designs into reality checks.

**What you'll do:**
- Run validation steps on real desktop platforms
- Submit structured test reports (platform details, procedure, results, failures)
- Help build the validation matrix (what works where, and why)

**Good fit if you like:** hardware bring-up, debugging, measurement discipline, reporting.

**Starter tasks:**
- Document your available test platform (CPU, chipset, motherboard, BIOS version)
- Review the Stage 8 validation checklists and flag any unclear or untestable items
- Propose a bring-up procedure for verifying SPD detection on a commodity desktop

---

## How to contribute

All contributions go through pull requests or issues.

### For documentation, tooling, or design changes:

1. Fork the repository
2. Create a branch for your work
3. Make your changes with clear, descriptive commits
4. Open a pull request against `main`
5. Describe what you changed and why
6. Reference any related issues

### For review findings or validation reports:

Open an **Issue** using the appropriate template, including:
- What you reviewed or tested
- What you found (with specifics)
- What you recommend

Full details are in **[CONTRIBUTING.md](./CONTRIBUTING.md)**.

---

## Task labels

When browsing issues, look for these labels:

| Label | Meaning |
|:---|:---|
| `good-first-issue` | Easy entry point — good for first-time contributors |
| `review-needed` | Needs a reviewer to check correctness, clarity, or completeness |
| `test-needed` | Needs validation on real hardware or structured test evidence |
| `docs` | Documentation improvement or addition |
| `tooling` | CI, automation, scripts, or infrastructure work |

---

## What OMI expects from contributors

OMI is not a fast-moving project. It is a careful one.

- **Document your assumptions.** If something is uncertain, say so explicitly.
- **Reproducibility is required**, not optional. If someone else can't follow your work, it isn't done.
- **No NDA-protected or proprietary material.** If it can't be shared publicly, it doesn't belong here.
- **Review is part of the process.** Feedback is technical, not personal. Expect it and welcome it.
- **Scope discipline matters.** OMI v1 is a DDR4 UDIMM. Proposals outside that scope are deferred, not dismissed.

---

## Key links

| Resource | Description |
|:---|:---|
| [CHARTER.md](./CHARTER.md) | Purpose, scope, governance, and principles |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Contribution workflow and expectations |
| [How OMI Is Engineered](./docs/how_omi_is_engineered.md) | Engineering methodology and stage definitions |
| [GitHub Discussions](https://github.com/The-Open-Memory-Initiative-OMI/omi/discussions) | Open-ended questions, proposals, and design RFCs |
| [GitHub Issues](https://github.com/The-Open-Memory-Initiative-OMI/omi/issues) | Concrete, actionable tasks and findings |

---

## Not sure where to start?

Open a Discussion titled:

**"I want to contribute — help me pick a starter task"**

Include:
- Your background and skills
- How much time you can commit
- Whether you have access to a desktop DDR4 platform for testing

Someone will help you find the right entry point.

---

> OMI values careful, transparent engineering over speed.
> Correctness first. Reproducibility always.
>
> If that aligns with how you work, welcome aboard.

