# Phase 6 — Export pipeline (netlist + BOM + schematic PDF, ERC-gated)

**Date:** 2026-06-02
**Branch:** `phase6-exports` (based on `phase5-erc`, the P5-bearing base; PR #32 not yet merged)
**Status:** complete — repeatable `powershell.exe` pipeline added; canonical export set committed; ERC-0 gate enforced; PR open (not merged).
**Tooling:** `kicad-cli` 9.0.8; Windows `powershell.exe`. Ethos: **additive only — the design is read-only.**

---

## 1. Problem / Motivation

After P5 the schematic is electrically coherent (**genuine ERC = 0**, 18 footprinted components).
What was missing was a *repeatable, honest* way to turn that design into the schematic-side
deliverables a reviewer or CV viewer can read without opening KiCad — the netlist, BOM, and
schematic PDF — plus a provenance record proving *which commit* they came from and that ERC was
clean when they were produced.

The risk this phase addresses is twofold: (a) **stale/ad-hoc exports** that drift from the real
design, and (b) the repo's known sensitivity — **overclaiming**. An export set with no provenance,
or a manifest that reads like a "validation/bench" report, would repeat the very mistake the audit
flagged. P6's deliverable is therefore a *gated, self-documenting* pipeline, not just files.

## 2. What changed

| File | Change |
|---|---|
| `tools/export/export.ps1` | **New.** The pipeline: ERC gate → netlist (xml + s-expr) → BOM (CSV) → schematic PDF → provenance manifest. Apache-2.0 header; auto-detects KiCad 9.0; idempotent; exits non-zero on the gate or any failure. |
| `tools/export/README.md` | **New.** Usage note: outputs, the ERC-0 gate behavior, the 9.0 requirement, how to run. (Usage only — no project-status/claims framing; that is P7.) |
| `exports/erc.json` | **New (generated).** ERC report — the gate's evidence (0 violations across all 5 sheets). |
| `exports/omi_v1.netlist.xml` | **New (generated).** Netlist, KiCad XML. |
| `exports/omi_v1.net` | **New (generated).** Netlist, KiCad S-expression. |
| `exports/omi_v1.bom.csv` | **New (generated).** Grouped BOM, with a `Procurement_Note` column annotating J1. |
| `exports/omi_v1.schematic.pdf` | **New (generated).** Combined schematic PDF, 5 pages (root + 4 sheets). |
| `exports/MANIFEST.txt` | **New (generated).** Export-provenance manifest (see §4). |
| `docs/implementations/2026-06-02-phase6-exports.md` | **New.** This document. |

**Unmodified (verified):** every `*.kicad_sch`, `omi.kicad_sym`, `tools/edge_symbol/**`,
`tools/edge_footprint/**`, the `.kicad_pcb`, `design/connector/ddr4_udimm_288_pinmap.csv`, and
`validation/**`. `git diff` against the design tree is empty before and after running the pipeline.

## 3. Implementation approach

`export.ps1` runs, in order, against the root schematic
`design/power/omi_v1_power/omi_v1_power.kicad_sch`:

1. **Resolve the toolchain.** Auto-detect `kicad-cli.exe` under `%LOCALAPPDATA%\Programs\KiCad\9.0\bin`,
   `Program Files\KiCad\9.0\bin`, or `PATH` (or take `-KicadBin`). The version string is checked to
   start with `9.` — **10.x is rejected**, because this project targets the 9.0 file format
   (`20250114`).
2. **ERC GATE (mandatory).** `kicad-cli sch erc --severity-all --exit-code-violations --format json`.
   The JSON is parsed and violations are summed across all sheets; if that count is `> 0` **or**
   kicad-cli's exit code is non-zero, the script aborts (`exit 1`) **before any export is written**.
   Exports are only ever produced from a verified-clean design.
3. **Netlist** in both formats: `--format kicadxml` → `omi_v1.netlist.xml`; `--format kicadsexpr` →
   `omi_v1.net`.
4. **BOM** (`sch export bom`), grouped by `Value,Footprint`, fields
   `Reference,Value,Footprint,Qty,DNP,Manufacturer,MPN`. The CSV is then post-processed (read-only
   to the design) to append a `Procurement_Note` column — see §5 for the J1-honesty rationale.
5. **Schematic PDF** (`sch export pdf`) — all sheets, one combined 5-page PDF.
6. **Provenance manifest** — `MANIFEST.txt` (see §4).

The script sets `$ErrorActionPreference = "Stop"`, checks `$LASTEXITCODE` after each native call,
and asserts each artifact exists before proceeding. It is **idempotent**: at start it removes any
prior artifacts in the output directory, so a re-run is clean and a *failed* run never leaves a
stale manifest that claims success. The hand-written usage doc lives in `tools/export/`, not
`exports/`, so the output directory holds only generated files and can be cleaned safely.

## 4. Provenance manifest — contents & honest labeling

`MANIFEST.txt` records **export provenance**, explicitly *not* validation. It opens with a scope
disclaimer ("NOT a validation, verification, bench, or hardware-test record … no hardware was
built, populated, or tested") and then records:

- **UTC timestamp** of generation;
- **`git rev-parse HEAD`** and branch — the exact design commit the artifacts came from;
- **`kicad-cli` version** (9.0.8);
- **ERC result**: `0 violations (clean) — gate passed`;
- **SHA-256** of every emitted artifact;
- a **component inventory** (18 components) that flags `J1` as a board feature, not a part.

This wording is deliberate: the manifest is an integrity/traceability artifact, and the repo's
history makes "validation"-flavored language a hazard.

## 5. Design decisions

- **ERC gate first, not last.** Running ERC *before* the exports (and aborting on any violation) is
  the integrity feature: it makes "these exports came from a clean design" a *guarantee of the
  pipeline*, not a claim in prose. Alternative (export, then ERC as a report) was rejected — it
  would allow exports from an unclean design.
- **J1 BOM honesty via a generated column, not a design edit.** The honest options were (a) set
  *Exclude-from-BOM* on the J1 symbol, or (b) annotate the output. Option (a) edits
  `*.kicad_sch` — forbidden in P6 (the design is read-only) and would also *hide* J1 entirely,
  making the BOM less complete. We chose (b): keep J1 visible (the netlist/BOM stay complete) but
  add a `Procurement_Note` marking it *"PCB card edge (board copper feature) — NOT a purchased
  part; exclude from procurement."* The DRAM, SPD, and 8× 240 Ω ZQ resistors are left unannotated —
  they are real, purchasable lines.
- **Both netlist formats.** `kicadxml` is the tool-friendly interchange format; `kicadsexpr` is the
  native KiCad netlist. Emitting both costs nothing and serves both downstream tools and KiCad
  users.
- **Optional generator `--verify` deliberately omitted.** The brief offered re-running the
  symbol/footprint generators' `--verify` to re-assert the 288-pin keystone invariants. The
  footprint generator's `--verify` *regenerates* the `.kicad_mod` into the design tree before
  checking (deterministic, but a write into read-only territory). To honor the additive-only rail
  and avoid OneDrive write churn, it was left out. The **ERC-0 gate is the mandatory integrity
  check**; the keystone invariants remain covered by the generators' own `--verify` when run
  intentionally (P2/P4).
- **PowerShell, off-PATH safe.** This machine has only `powershell.exe` and a per-user KiCad install
  (`%LOCALAPPDATA%\Programs\KiCad\9.0\bin`), so detection probes that path first.

## 6. Mathematical / numeric details

Two numeric pieces, both audit-relevant:

- **ERC violation count.** The gate's decision value is
  `N = Σ_sheets (length of that sheet's "violations" array)` from the ERC JSON. The pipeline
  proceeds **iff** `N = 0` *and* kicad-cli's exit code is 0 (belt-and-suspenders: the parsed count
  and the tool's own `--exit-code-violations` signal must agree). Measured: `N = 0` across all 5
  sheets.
- **SHA-256 digests.** Each artifact's fingerprint is its SHA-256 hash — a 256-bit (64 hex-char)
  one-way digest where any single-byte change yields an essentially unrelated value (collision
  probability negligible at ~2⁻¹²⁸ for accidental change). The manifest lists these so a reviewer
  can recompute `Get-FileHash -Algorithm SHA256 <file>` and confirm the committed artifact is the
  one the manifest describes. The manifest cannot hash itself (a file cannot contain its own
  digest), so it hashes the five artifacts and omits itself — standard practice.

## 7. Verification

Concrete, runnable steps (all read-only except the pipeline, which writes only `exports/`):

1. **Run the pipeline:**
   ```powershell
   powershell.exe -ExecutionPolicy Bypass -File tools\export\export.ps1
   echo "exit=$LASTEXITCODE"   # expect 0
   ```
   Expect: `ERC: 0 violations (clean) - gate passed`, then 5 artifacts + `MANIFEST.txt`.
2. **Confirm the ERC gate logic** would abort on a dirty design *by reasoning, not by breaking the
   design*: the ERC call is step 1, its result is summed and checked, and a non-zero count calls
   `Fail` (`exit 1`) before any `export` command runs. (Independently, P5's ledger shows the gate at
   the boundary: 85→0.)
3. **BOM honesty:** `Get-Content exports\omi_v1.bom.csv` — the `J1` row carries the
   `Procurement_Note`; the DRAM/SPD/ZQ rows do not.
4. **PDF page count = 5** (root + 4 sheets): count `/Type /Page` objects in the PDF.
5. **Manifest integrity:** recompute each SHA-256 and confirm it appears in `MANIFEST.txt`:
   ```powershell
   foreach ($f in 'erc.json','omi_v1.netlist.xml','omi_v1.net','omi_v1.bom.csv','omi_v1.schematic.pdf') {
     $h = (Get-FileHash -Algorithm SHA256 "exports\$f").Hash.ToLower()
     "$f -> $(Select-String -Path exports\MANIFEST.txt -Pattern $h -Quiet)"   # expect True for all
   }
   ```
6. **Design untouched:** `git diff --stat` is empty for the design tree before and after the run.
7. **Repeatable (not bit-reproducible):** re-run step 1; it exits 0 again. The netlist and ERC
   reports embed a wall-clock export `<date>`, so those bytes — and thus their manifest hashes —
   change every run; the *file set*, the ERC-0 result, and the (timestamp-free) BOM contents are
   unchanged. The manifest always stays internally consistent with the run that produced it.

All seven were executed during implementation and passed.

## 8. Related docs

- `PHASE6_EXPORTS_BRIEF.md` — the authoritative P6 spec (untracked working doc).
- `docs/implementations/2026-06-01-phase5-erc.md` — P5, which produced the ERC-0 design these
  exports come from.
- `docs/implementations/2026-06-01-phase4-footprints.md` — footprints (the BOM's `Footprint` column).
- `tools/export/README.md` — pipeline usage.

## 9. Handoff to P7 (README / claims)

P7 should point the project README at these **real** exports (`exports/`), and frame the project
honestly: **ERC-0 via real electrical connections** (not exclusions), the **J1 mechanical caveat**
(288-position card edge = board copper, not a purchased connector; mechanical/SI unproven), the
**label-on-pin structural note** (J1 kept frozen in P5 because directional retyping broke
label-on-pin connectivity), and the overall scope — **a schematic-stage reference-design study, not
validated hardware.** The manifest's disclaimer wording is a usable template for that framing.
