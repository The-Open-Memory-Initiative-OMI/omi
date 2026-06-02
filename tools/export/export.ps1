# SPDX-License-Identifier: Apache-2.0
#
# Copyright 2026 The Open Memory Initiative (OMI) contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

<#
.SYNOPSIS
  OMI v1 - Phase 6 schematic-side export pipeline (Windows PowerShell / powershell.exe).

.DESCRIPTION
  Produces the repeatable, in-repo export set from the ERC-clean schematic:

      1. ERC GATE   - runs ERC first; ABORTS (non-zero exit) if ANY violation exists.
                      Exports are only ever produced from a verified-clean design.
      2. Netlist    - KiCad XML (.netlist.xml) + KiCad S-expression (.net).
      3. BOM        - CSV, grouped by Value+Footprint. J1 (the 288-position card edge)
                      is annotated as a board copper feature, NOT a purchased part.
      4. PDF        - combined schematic PDF, all sheets.
      5. MANIFEST   - HONEST export-provenance record: UTC timestamp, git HEAD,
                      kicad-cli version, "ERC: 0 violations (clean)", and a SHA-256
                      for every emitted artifact.

  This is an EXPORT PROVENANCE pipeline. The manifest records how the artifacts were
  produced and that ERC was clean at export time. It is NOT a validation / verification
  / bench / hardware-test record - this project is a schematic-stage reference-design
  study and no hardware was built or tested.

  The design is read-only: this script reads the schematic and writes only into the
  output directory. It modifies no *.kicad_sch, no symbol/footprint library, and no PCB.

  Idempotent: safe to re-run. Previous artifacts in the output directory are removed and
  regenerated. Exits 0 only on a fully clean run; non-zero on the ERC gate or any failure.

.PARAMETER KicadBin
  Full path to kicad-cli.exe (KiCad 9.0). If omitted, the script auto-detects a 9.0
  install under %LOCALAPPDATA%\Programs\KiCad\9.0\bin, Program Files, or PATH.
  KiCad 10.x is rejected (this project targets the 9.0 toolchain / file format 20250114).

.PARAMETER OutDir
  Output directory for the export set. Default: "exports" (repo-relative).

.PARAMETER Schematic
  Root schematic. Default: design\power\omi_v1_power\omi_v1_power.kicad_sch (repo-relative).

.EXAMPLE
  powershell.exe -ExecutionPolicy Bypass -File tools\export\export.ps1

.EXAMPLE
  powershell.exe -ExecutionPolicy Bypass -File tools\export\export.ps1 `
    -KicadBin "C:\Users\me\AppData\Local\Programs\KiCad\9.0\bin\kicad-cli.exe"
#>

[CmdletBinding()]
param(
    [string]$KicadBin = "",
    [string]$OutDir = "exports",
    [string]$Schematic = "design\power\omi_v1_power\omi_v1_power.kicad_sch"
)

$ErrorActionPreference = "Stop"

function Fail([string]$msg) {
    Write-Host ""
    Write-Host "ERROR: $msg" -ForegroundColor Red
    exit 1
}

function Write-Utf8NoBom([string]$path, [string]$text) {
    # Write UTF-8 WITHOUT a byte-order mark (clean CSV/text for downstream parsers).
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($path, $text, $enc)
}

# --- Resolve repo root (this script lives in <root>\tools\export) -----------------
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

# --- Resolve kicad-cli (KiCad 9.0; off-PATH safe; reject 10.x) ---------------------
function Resolve-KicadCli([string]$override) {
    $candidates = New-Object System.Collections.Generic.List[string]
    if ($override) { $candidates.Add($override) }
    if ($env:LOCALAPPDATA) { $candidates.Add((Join-Path $env:LOCALAPPDATA "Programs\KiCad\9.0\bin\kicad-cli.exe")) }
    if ($env:ProgramFiles) { $candidates.Add((Join-Path $env:ProgramFiles "KiCad\9.0\bin\kicad-cli.exe")) }
    if (${env:ProgramFiles(x86)}) { $candidates.Add((Join-Path ${env:ProgramFiles(x86)} "KiCad\9.0\bin\kicad-cli.exe")) }
    $onPath = Get-Command kicad-cli -ErrorAction SilentlyContinue
    if ($onPath) { $candidates.Add($onPath.Source) }
    foreach ($c in $candidates) {
        if ($c -and (Test-Path $c)) { return (Resolve-Path $c).Path }
    }
    return $null
}

$bin = Resolve-KicadCli $KicadBin
if (-not $bin) {
    Fail "kicad-cli.exe (KiCad 9.0) not found. Install KiCad 9.0 or pass -KicadBin <path to kicad-cli.exe>."
}

$ver = ""
try { $ver = (& $bin version 2>$null | Select-Object -First 1) } catch {}
$ver = "$ver".Trim()
if ($ver -notmatch '^9\.') {
    Fail "kicad-cli reports version '$ver'. This pipeline requires KiCad 9.0.x (file format 20250114), not 10.x. Pass -KicadBin to a 9.0 install."
}

# --- Resolve and validate paths ----------------------------------------------------
$sch = Join-Path $repoRoot $Schematic
if (-not (Test-Path $sch)) { Fail "Root schematic not found: $sch" }

$out = Join-Path $repoRoot $OutDir
New-Item -ItemType Directory -Force -Path $out | Out-Null

$ercJson  = Join-Path $out "erc.json"
$netXml   = Join-Path $out "omi_v1.netlist.xml"
$netSexpr = Join-Path $out "omi_v1.net"
$bomCsv   = Join-Path $out "omi_v1.bom.csv"
$pdf      = Join-Path $out "omi_v1.schematic.pdf"
$manifest = Join-Path $out "MANIFEST.txt"

# Idempotency: clear previously generated artifacts so a re-run is clean and a failed
# run never leaves a stale manifest that claims success.
foreach ($f in @($ercJson, $netXml, $netSexpr, $bomCsv, $pdf, $manifest)) {
    if (Test-Path $f) { Remove-Item $f -Force }
}

Write-Host ""
Write-Host "OMI v1 - export pipeline" -ForegroundColor Cyan
Write-Host "  kicad-cli : $bin (v$ver)"
Write-Host "  schematic : $sch"
Write-Host "  output    : $out"
Write-Host ""

# --- [1/5] ERC GATE (mandatory) ----------------------------------------------------
Write-Host "[1/5] ERC gate ..."
& $bin sch erc --severity-all --exit-code-violations --format json -o $ercJson $sch | Out-Null
$ercExit = $LASTEXITCODE
if (-not (Test-Path $ercJson)) { Fail "ERC produced no report ($ercJson)." }

$erc = Get-Content $ercJson -Raw | ConvertFrom-Json
$violCount = 0
if ($erc.sheets) {
    foreach ($sheet in $erc.sheets) { $violCount += @($sheet.violations).Count }
}
if ($violCount -gt 0 -or $ercExit -ne 0) {
    Fail "ERC GATE FAILED: $violCount violation(s) (kicad-cli exit $ercExit). Exports NOT produced. Resolve ERC to 0 first; see $ercJson."
}
Write-Host "      ERC: 0 violations (clean) - gate passed." -ForegroundColor Green

# --- [2/5] Netlist (kicadxml + kicadsexpr) -----------------------------------------
Write-Host "[2/5] Netlist (kicadxml + kicadsexpr) ..."
& $bin sch export netlist --format kicadxml -o $netXml $sch | Out-Null
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $netXml)) { Fail "netlist (kicadxml) export failed." }
& $bin sch export netlist --format kicadsexpr -o $netSexpr $sch | Out-Null
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $netSexpr)) { Fail "netlist (kicadsexpr) export failed." }

# --- [3/5] BOM (CSV, grouped) ------------------------------------------------------
Write-Host "[3/5] BOM (CSV) ..."
$bomFields = 'Reference,Value,Footprint,${QUANTITY},${DNP},Manufacturer,MPN'
$bomLabels = 'Reference,Value,Footprint,Qty,DNP,Manufacturer,MPN'
& $bin sch export bom --fields $bomFields --labels $bomLabels --group-by 'Value,Footprint' -o $bomCsv $sch | Out-Null
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $bomCsv)) { Fail "BOM export failed." }

# BOM honesty: J1 is the PCB card edge (board copper fingers), not a buyable connector.
# The design is read-only, so we annotate the GENERATED CSV (not the schematic): add a
# Procurement_Note column flagging J1 as a board feature. DRAM / SPD / ZQ resistors are
# real, purchasable BOM lines and are left unannotated.
$j1Note = "PCB card edge (board copper feature) - NOT a purchased part; exclude from procurement"
$rows = Import-Csv $bomCsv
$annotated = $rows | Select-Object Reference, Value, Footprint, Qty, DNP, Manufacturer, MPN, `
    @{ N = 'Procurement_Note'; E = { if ($_.Reference -match '^J') { $j1Note } else { '' } } }
$csvText = ($annotated | ConvertTo-Csv -NoTypeInformation) -join "`r`n"
Write-Utf8NoBom $bomCsv ($csvText + "`r`n")

# --- [4/5] Schematic PDF (all sheets) ----------------------------------------------
Write-Host "[4/5] Schematic PDF (all sheets) ..."
& $bin sch export pdf -o $pdf $sch | Out-Null
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $pdf)) { Fail "schematic PDF export failed." }

# --- [5/5] Provenance manifest (HONEST: provenance, not validation) ----------------
Write-Host "[5/5] Provenance manifest ..."

$utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-dd HH:mm:ss 'UTC'")

$gitHead = ""
$gitBranch = ""
try { $gitHead = (& git -C $repoRoot rev-parse HEAD 2>$null) } catch {}
try { $gitBranch = (& git -C $repoRoot rev-parse --abbrev-ref HEAD 2>$null) } catch {}
if (-not $gitHead) { $gitHead = "(unavailable - not a git working tree)" }
if (-not $gitBranch) { $gitBranch = "(unavailable)" }
$gitHead = "$gitHead".Trim()
$gitBranch = "$gitBranch".Trim()

$schRel = $Schematic -replace '\\', '/'

# SHA-256 every emitted artifact (the manifest cannot hash itself).
$artifacts = @($ercJson, $netXml, $netSexpr, $bomCsv, $pdf)
$hashLines = foreach ($a in $artifacts) {
    $h = (Get-FileHash -Algorithm SHA256 -Path $a).Hash.ToLower()
    $name = Split-Path $a -Leaf
    "  {0}  {1}" -f $h, $name
}

$lines = @()
$lines += "OMI v1 - Export Provenance Manifest"
$lines += "==================================="
$lines += ""
$lines += "This file records the PROVENANCE of the schematic-side export artifacts in this"
$lines += "directory: when they were generated, from which commit, with which tool, and that"
$lines += "the schematic passed Electrical Rule Check (ERC) cleanly at export time."
$lines += ""
$lines += "It is NOT a validation, verification, bench, or hardware-test record. OMI v1 is a"
$lines += "schematic-stage reference-design study; no hardware was built, populated, or tested."
$lines += "PCB layout, Gerbers, and signal/power integrity remain out of scope."
$lines += ""
$lines += "Generated (UTC) : $utc"
$lines += "Git HEAD        : $gitHead"
$lines += "Git branch      : $gitBranch"
$lines += "Source schematic: $schRel"
$lines += "kicad-cli       : $ver"
$lines += "ERC result      : 0 violations (clean) - gate passed, exports produced."
$lines += ""
$lines += "Artifacts (SHA-256):"
$lines += $hashLines
$lines += ""
$lines += "Component inventory (18 placed components, all footprinted):"
$lines += "  J1          x1   DDR4_UDIMM_288_Edge    288-position card edge - BOARD FEATURE, not a purchased part"
$lines += "  R1-R8       x8   240 ohm, 0402          ZQ calibration resistors (to VSS)"
$lines += "  U_DRAM0-7   x8   FBGA-78                DDR4 SDRAM (8Gb, 1Rx8)"
$lines += "  U_SPD0      x1   UDFN-8                 SPD EEPROM"
$lines += ""
$lines += "Regenerate with: powershell.exe -ExecutionPolicy Bypass -File tools\export\export.ps1"
$lines += ""

Write-Utf8NoBom $manifest (($lines -join "`r`n"))

# --- Done --------------------------------------------------------------------------
Write-Host ""
Write-Host "Export complete - ERC clean, 5 artifacts + manifest written to:" -ForegroundColor Green
Write-Host "  $out"
Get-ChildItem $out | Sort-Object Name | Format-Table Name, Length -AutoSize | Out-String | Write-Host
exit 0
