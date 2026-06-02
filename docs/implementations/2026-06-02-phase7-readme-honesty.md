# Phase 7 — Honest README & claims (the closer)

**Date:** 2026-06-02
**Branch:** `phase7-readme-honesty` (based on `phase6-exports`, the finished-state base; the P4→P5→P6 stack is not yet merged into `main`).
**Status:** complete — README + public-facing docs made accurate; the legacy "L1 Bench PASS" honestly corrected; PR open (not merged).
**Ethos:** **documentation only.** The engineering and its evidence are complete and frozen. P7 edits prose; it changes no schematic, symbol, footprint, export, or script.

---

## 1. Problem / Motivation

This project began because an audit found the repo **overclaimed** — most damningly an "L1 Bench
Electrical — **PASS**" that was actually produced by running the L1 tooling over a **blank
measurement template**, with no board and no measurements.

By Phase 7 the framing had **inverted**. Phases 1–6 made the schematic genuinely **complete**: a
real 288-pin edge connector `J1`, placeholder host connectors removed, **ERC = 0 with no
exclusions**, **18/18 components footprinted**, and a generated netlist + BOM + schematic PDF under
`exports/`. So the README now faced *two* equal failure modes:

- **Overclaiming** (the original sin) — implying fabricated/validated/bench-tested hardware, or a
  bench PASS that never happened.
- **Underclaiming** — burying six phases of real, finished work under apologetic hedging.

P7's job is the honesty balance: **claim the earned completion confidently, correct the genuinely
false legacy claims, state the WALL plainly, and carry the build's caveats.** The README is also the
public face of this work (CV / website), so "accurate, neither inflated nor apologetic" is the bar.

## 2. What changed

| File | Change |
|---|---|
| `README.md` | **Project Status** rewritten to claim the earned completion (Stage 7 schematic complete: real 288-pin `J1`, placeholders removed, ERC-0 no exclusions, 18/18 footprinted, netlist+BOM+PDF) with evidence pointers; new **"What 'validated' means here"** (L0 + ERC + export provenance real; physical L1–L4 not executed) and **"Scope boundary (the wall)"** subsections (no layout/Gerbers/SI-PI/fab; J1 pads-only caveat; label-on-pin note); **Repository Navigation** fixed (dead `docs/05`/`docs/06` paths → real dirs; `design/power/omi_v1_power/` + `exports/` added); **Publications** "Verifiable Hardware" line scoped to "a complete *schematic*". P0's Licensing + governance sections left intact. |
| `validation/evidence/l1_summary.md` | **The key legacy fix.** Retitled "FRAMEWORK DRY-RUN (NOT a bench measurement)"; prominent honesty banner; "Status: PASS" → "Framework status"; measurements row marked **BLANK TEMPLATE**; check table reframed as tooling-ran-OK (not measurements); `continuity_report.json` annotated as a template-structure check; pointer to `exports/erc.json` for genuine electrical evidence. Recorded evidence-file hashes left unchanged (all still valid). |
| `validation/evidence/l1_summary.json` | Added a top-level `_HONESTY_NOTE` disclaiming the dry-run; existing machine fields (incl. `overall_status`) left intact. |
| `START_HERE.md` | Intro + stage table updated to the earned completion; broken `docs/05`/`docs/06` links fixed; repo map corrected (real KiCad source + `exports/` added); "validation" wording scoped. |
| `CHARTER.md` | Bounded dated status note at **§8.1** (Minimum Viable Success): schematic milestone reached; physical-manufacture / bench / measured-results criteria **remain future**. No principle (§4/§6) altered. |
| `docs/implementations/2026-06-02-phase7-readme-honesty.md` | **New.** This document. |

**Unmodified (verified by `git status`):** every `*.kicad_sch`, `omi.kicad_sym`, the generators
under `tools/**`, the `.kicad_pcb`, `design/connector/ddr4_udimm_288_pinmap.csv`, **everything in
`exports/`**, the genuine **L0 evidence** (`l0_summary.*`, `pinmap_report.json`,
`naming_report.json`, `lane_matrix.csv`), `continuity_report.json`, and the validation **scripts**.
The tracked diff is exactly six files: five prose files + this doc.

## 3. The claim → correction list (the heart of P7)

| # | Where | Was (inaccurate) | Now (accurate) |
|---|---|---|---|
| 1 | README Status / Stage 7 | **Underclaimed** — Stage 7 framed as intent docs ("simplified star"), no mention of the real ERC-clean/footprinted/netlisted KiCad capture | Earned completion claimed: real 288-pin `J1`, placeholders removed, **ERC-0 (no exclusions)**, **18/18 footprinted**, netlist+BOM+PDF; evidence → `exports/`, `MANIFEST.txt`, `docs/implementations/` |
| 2 | README "validation" | No honest scoping of the word | Validation = **L0 artifact-integrity + ERC-clean + export provenance** (all real); physical **L1–L4 not executed** (no board, no measurements) |
| 3 | README scope | No explicit WALL | WALL stated: no PCB layout, Gerbers, SI/PI, or fabricated/bench board. **J1 = 288 numbered pads only** (JEDEC notch/outline/pad geometry unproven); **label-on-pin** structural note carried |
| 4 | README + START_HERE nav | `docs/05_architecture_decisions/`, `docs/06_block_decomposition/` — **do not exist** | Real `docs/05_power_delivery_and_pdn/`, `docs/06_signal_topology_and_routing/`; **added** `design/power/omi_v1_power/` (real KiCad source) and `exports/` |
| 5 | README Publications | "Turning a DDR4 UDIMM Schematic into **Verifiable Hardware**" | Scope note: the repo contains a complete **schematic** today — not fabricated/verified hardware; that remains future work |
| 6 | `validation/evidence/l1_summary.{md,json}` | **"L1 Bench Electrical — PASS"** over a blank template — read as bench validation | Relabeled a **framework/procedure dry-run**: no board built/probed, no measurements; `continuity_report.json` flagged as template-structure; pointer to `exports/erc.json` (real ERC 0) |
| 7 | START_HERE / CHARTER | "building toward fabricated hardware" framing unscoped; fabricated-hardware success implied as the measure | Schematic milestone reached; **fabricated-hardware success remains future/aspirational** (CHARTER §8.1) — consistent with the README |

## 4. Implementation approach

Read-only inventory first (the table above), then edits in three logical commits — **README**, then
the **L1 relabel**, then the **START_HERE / CHARTER** consistency pass — followed by this doc.

The **L1 relabel** is deliberately surgical. Two artifacts were edited (`l1_summary.md`, the
human-facing headline the audit flagged, and `l1_summary.json`, the machine summary). `l1_summary.md`
gets a top-of-file ⚠️ honesty banner and a retitle so a casual reader cannot mistake it for a bench
result; the `continuity_report.json` "PASS" lines are explicitly re-explained as *template-structure*
checks (the report itself is **not** edited — see §5/§6). The genuine **L0 evidence** and the
**scripts** are untouched: P7 corrects only the misleading *framing*, never the data or the tooling.

## 5. Design decisions

- **Branch base = `phase6-exports`, not `main`.** The pre-flight gate requires the finished design
  (ERC 0, 18 footprinted, `exports/` present) to be **on the base**. `main` does **not** yet contain
  P4/P5/P6 (they are a stacked, unmerged set: PR #31→#32→#33). The only base where the finished state
  actually lives is `phase6-exports`, so P7 stacks on it — consistent with how P6 stacked on P5.
  Landing the whole stack into `main` in order remains the user's final step; P7 does not merge.
- **L1: relabel, don't delete or fabricate.** The honest fix is to *reframe* the misleading summary,
  not to delete the L1 artifacts (they are a legitimate *framework* dry-run) nor to alter the scripts
  or the genuine L0 evidence. The "PASS" values are left visible but unambiguously re-scoped as
  "the tooling ran over a blank template," with a pointer to the real ERC evidence.
- **`continuity_report.json` left byte-for-byte unchanged.** It is the faithful output of
  `validate_continuity_log.py`, and — crucially — its SHA-256 is *recorded in the L0/L1 manifests*.
  Editing it would (a) misrepresent what the script produced and (b) break a hash that the genuine L0
  evidence references. Instead it is neutralized **in prose** from `l1_summary.md`, which indexes it.
- **`validation/evidence/README.md` reverted after an initial edit.** An early draft added an L1
  clarification there — but that file's SHA-256 is recorded (`c454f21…`) inside the **genuine L0
  manifest** (`l0_summary.md`) as well as the L1 summary. Editing it would have invalidated a hash in
  evidence I am forbidden to alter, so the edit was reverted (file restored to `c454f21…`). The L1
  honesty fix is fully carried by `l1_summary.{md,json}`, which **nothing** hash-references.
- **CHARTER edit kept minimal.** The charter is an aspirational founding document and is honest in
  its forward-looking tense; it does not *claim* hardware exists. So P7 adds only a bounded, dated
  **status note** at §8.1 (schematic reached; fabrication/bench remain future) and changes no
  principle — honoring §12.5 ("changes must preserve Sections 4 and 6").
- **Stage 9 reclassified from "In Progress" to "not started."** There is no evidence of Stage 9
  (reference-schematic refinement / SPD hex) or Stage 10 (layout) work; the real progress is the
  *completed schematic* (Stage 7). Calling Stage 9 "in progress" would itself be a mild overclaim, so
  it is now listed beyond the WALL.

## 6. Integrity note — the evidence hash chain

The `validation/evidence/` directory is self-describing: `l0_summary.{md,json}` and
`l1_summary.{md,json}` each list the **SHA-256** of the other evidence files (pin-map/naming reports,
`lane_matrix.csv`, `continuity_report.json`, `probe_*`, and the directory's `README.md`). A SHA-256
is a 256-bit one-way digest: any single-byte change to a referenced file makes the recorded hash no
longer match, which a reviewer can detect with `Get-FileHash -Algorithm SHA256`.

Two consequences governed the L1 fix:
1. **`l1_summary.md` and `l1_summary.json` are safe to edit** — no file records *their* hashes, so
   reframing them invalidates nothing. (They list *other* files' hashes; since those files are
   untouched, every listed hash stays valid.)
2. **Any hash-referenced file is off-limits** — `continuity_report.json` and the evidence-dir
   `README.md` are both referenced by the genuine L0 manifest, so neither was changed. This is why
   the L1 correction lives entirely in the two summary files.

## 7. Verification

1. **Scope (prose-only):** `git status --porcelain --untracked-files=no` lists exactly
   `CHARTER.md`, `README.md`, `START_HERE.md`, `validation/evidence/l1_summary.md`,
   `validation/evidence/l1_summary.json` (+ this doc once added). No `*.kicad_sch`, `omi.kicad_sym`,
   `exports/**`, script, CSV, `.kicad_pcb`, or genuine L0 evidence appears.
2. **Hash chain intact:** `(Get-FileHash validation\evidence\README.md -Algorithm SHA256).Hash`
   equals `c454f21…` (the value recorded in `l0_summary.md`/`l1_summary.md`). `l1_summary.json`
   parses as valid JSON (`Get-Content -Raw … | ConvertFrom-Json`).
3. **No broken nav:** the strings `05_architecture_decisions` and `06_block_decomposition` no longer
   appear in `README.md` or `START_HERE.md`; every path referenced (`design/power/omi_v1_power/`,
   `exports/`, `docs/05_power_delivery_and_pdn/`, `docs/06_signal_topology_and_routing/`,
   `docs/implementations/`, `validation/evidence/l0_summary.md`) resolves to a real file/dir.
4. **Facts match evidence:** the README's component figures (18 total; `J1` ×1, `R1–R8` ×8 @240 Ω,
   `U_DRAM0–7` ×8 FBGA-78, `U_SPD0` ×1 UDFN-8) match `exports/MANIFEST.txt`; "ERC 0 violations / no
   exclusions" matches `exports/erc.json` (empty `violations` on all 5 sheets).
5. **L1 unmistakable:** `validation/evidence/l1_summary.md` opens with the ⚠️ honesty banner and the
   title says "NOT a bench measurement"; no remaining unscoped "PASS" reads as hardware.
6. **No contradiction:** README, START_HERE, and CHARTER agree — schematic complete; hardware future.

Steps 1–6 were executed during implementation and an independent multi-lens review confirmed no
over- or under-claim and no broken link remained.

## 8. Related docs

- `PHASE7_README_HONESTY_BRIEF.md` — the authoritative P7 spec (untracked working doc).
- `docs/implementations/2026-06-02-phase6-exports.md` — P6 exports (the evidence the README points at)
  and its §9 handoff, which scoped this phase.
- `docs/implementations/2026-06-01-phase5-erc.md` — P5, the genuine ERC-0 and the frozen-J1 /
  label-on-pin finding the WALL note carries.
- `exports/MANIFEST.txt` — the provenance/scope wording reused as the README's scope template.
