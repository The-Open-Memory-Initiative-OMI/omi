<!-- SPDX-License-Identifier: Apache-2.0 -->
# `tools/export` — OMI v1 schematic-side export pipeline

`export.ps1` regenerates the in-repo export set (`exports/`) from the schematic, **gated on a
clean ERC**. It is a Windows PowerShell (`powershell.exe`) script. This is a *usage* note; for the
design rationale see `docs/implementations/2026-06-02-phase6-exports.md`.

## What it produces

Into `exports/` (repo-relative by default):

| File | What it is |
|---|---|
| `erc.json` | ERC report (the gate's evidence; 0 violations) |
| `omi_v1.netlist.xml` | Netlist, KiCad XML format |
| `omi_v1.net` | Netlist, KiCad S-expression format |
| `omi_v1.bom.csv` | BOM (grouped by Value+Footprint), with a `Procurement_Note` column |
| `omi_v1.schematic.pdf` | Combined schematic PDF, all sheets |
| `MANIFEST.txt` | Export-provenance manifest: UTC time, git HEAD, kicad-cli version, ERC-clean confirmation, SHA-256 of every artifact above |

## The ERC-0 gate

ERC runs **first**. If the schematic has **any** ERC violation, the script prints an error and
**exits non-zero without producing any export** — exports only ever come from a verified-clean
design. A fully clean run exits `0`.

## Requirements

- **KiCad 9.0** `kicad-cli` (file format `20250114`) — **not** 10.x, which the script rejects.
  Auto-detected under `%LOCALAPPDATA%\Programs\KiCad\9.0\bin`, `Program Files\KiCad\9.0\bin`, or
  `PATH`; otherwise pass `-KicadBin`.
- `git` on `PATH` (for the manifest's HEAD; the script still runs without it, recording the HEAD
  as unavailable).

## Run

```powershell
# from the repo root
powershell.exe -ExecutionPolicy Bypass -File tools\export\export.ps1

# explicit kicad-cli path / custom output dir
powershell.exe -ExecutionPolicy Bypass -File tools\export\export.ps1 `
  -KicadBin "C:\Users\me\AppData\Local\Programs\KiCad\9.0\bin\kicad-cli.exe" `
  -OutDir exports
```

The script is **idempotent**: each run clears and regenerates the artifacts (the manifest's UTC
timestamp and hashes change accordingly).

## Scope note

The manifest is an **export-provenance** record (how/when/from-what-commit the files were
generated, and that ERC was clean) — **not** a validation, verification, bench, or hardware-test
record. OMI v1 is a schematic-stage reference-design study; PCB layout, Gerbers, and SI/PI remain
out of scope. In the BOM, **`J1` is the PCB card edge** (board copper fingers), annotated as *not a
purchased part*; the DRAM, SPD, and ZQ resistors are real, purchasable lines.
