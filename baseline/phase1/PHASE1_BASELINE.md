# OMI v1 — Phase 1 Baseline (kicad-cli measurement snapshot)

**Branch:** `phase1-kicad-cli-baseline` · **Date:** 2026-06-01 · **Type:** read-only measurement.
**Nothing in the design was modified.** This is a point-in-time "before" snapshot of the *unmodified*
schematic — ERC, netlist, BOM, and a phase-tagged gap list. No ERC error was fixed, no symbol built,
no footprint assigned, no connector replaced, no PCB command run.

All raw artifacts live beside this file in `baseline/phase1/`:
`erc_report.json`, `erc_report.txt`, `netlist.kicadxml.xml`, `netlist.net`, `bom.csv`,
`_console_log.txt`.

---

## 1. Environment

| Item | Value |
|---|---|
| kicad-cli used | **9.0.8** (release build, 2026-03-15; x64, Windows 11 build 26200) |
| Other KiCad present (unused) | 10.0.1 — *not* used; 9.0 chosen to match the schematic's generator |
| Root schematic | `design/power/omi_v1_power/omi_v1_power.kicad_sch` (confirmed root via the same-named `.kicad_pro`) |
| Sub-sheets (traversed) | `address-command-clock`, `data-byte-lanes-dqs`, `spd-and-configuration`, `udimm-edge-interface` |
| Schematic format version | `(version 20250114)`, `(generator "eeschema")`, `(generator_version "9.0")` — **uniform across all 5 sheets** |
| Symbol libraries referenced | `Connector_Generic`, `Memory_RAM`, `Memory_EEPROM` — **all standard KiCad libs** |
| Project library tables | none — no `sym-lib-table` / `fp-lib-table` in the project; global KiCad libs only |
| Missing-library warnings | **none** — all symbols resolved |
| Other CLI warning | `schematic has annotation errors` (emitted on netlist/BOM export — see §5 finding) |

**Command log** (run from repo root, KiCad 9.0.8, `$sch` = root schematic above):

```powershell
kicad-cli sch erc --severity-all --format json   -o baseline\phase1\erc_report.json $sch
kicad-cli sch erc --severity-all --format report -o baseline\phase1\erc_report.txt  $sch
kicad-cli sch export netlist --format kicadxml   -o baseline\phase1\netlist.kicadxml.xml $sch
kicad-cli sch export netlist --format kicadsexpr -o baseline\phase1\netlist.net          $sch
kicad-cli sch export bom                         -o baseline\phase1\bom.csv              $sch
```

ERC exit code was 0 here (no `--exit-code-violations` passed); the 131 violations were still written —
exit code is not a pass/fail signal for this baseline.

---

## 2. ERC summary — 131 violations

Source: `erc_report.json` (`sch erc --severity-all`).

**By type:**

| Violation type | Count |
|---|---|
| `pin_not_connected` | 108 |
| `pin_not_driven` | 16 |
| `power_pin_not_driven` | 5 |
| `label_dangling` | 2 |
| **Total** | **131** |

**By sheet:**

| Sheet | Violations |
|---|---|
| `/address-command-clock/` | 94 |
| `/data-byte-lanes-dqs/` | 32 |
| `/spd-and-configuration/` | 2 |
| `/` (root power) | 3 |
| `/udimm-edge-interface/` | 0 |
| **Total** | **131** |

**Structural reading:** 95% of violations are *unconnected* or *not-driven* pins (124/131) —
`pin_not_connected` alone is 108 (82%) — concentrated where the design meets the (not-yet-real) host
interface: DRAM control/data pins and the placeholder host connectors. 5 `power_pin_not_driven`
(e.g. `U_DRAM* VDDQ`, isolated `#PWR` symbols) and 2 dangling labels on the root sheet (`VDDQ`,
`VREF`). All 131 are reported at error-severity; deciding which are true errors vs.
acceptable-by-design warnings is **P5** work, not a Phase-1 judgement.

---

## 3. Netlist / BOM summary

Source: `netlist.kicadxml.xml` (structural ground truth) + `bom.csv`.

| Metric | Value |
|---|---|
| Components | **15** |
| Nets | **238** |
| Footprints assigned | **9 of 15** (all 8 DRAM + the SPD EEPROM) |
| Footprints missing | **6 of 15** — exactly the placeholder host connectors |
| DRAM instances | **8** — `U_DRAM0…U_DRAM7` |
| Duplicate references | none (15 unique instance refs) |

**Component inventory:**

| Ref(s) | Qty | Value / MPN | Footprint | Sheet |
|---|---|---|---|---|
| `U_DRAM0…7` | 8 | H5AN8G8NAFR-UHC (SK Hynix DDR4 8 Gb ×8) | `Package_BGA:FBGA-78_7.5x11mm_Layout2x3x13_P0.8mm` | address-command-clock |
| `U_SPD0` | 1 | DDR4_SPD_EEPROM (AT24CS01-class I²C) | assigned | spd-and-configuration |
| `J_PWR` | 1 | `UDIMM_HOST_POWER` *(placeholder)* | — | (power / root) |
| `J_HOST` | 1 | `HOST_CA_CLK` *(placeholder)* | — | address-command-clock |
| `J_HOST_DQ_A/B/C` | 3 | `HOST_DQ_DQS` *(placeholder)* | — | data-byte-lanes-dqs |
| `J_HOST_SPD` | 1 | `HOST_SMBUS_SPD` *(placeholder)* | — | spd-and-configuration |

8 × 8 Gb = 64 Gb = **8 GB**, x8 devices on a 64-bit bus = **1Rx8**. The capacity/organisation matches
the stated v1 target. **The "9 DRAM" anomaly is not reproduced** — see §5.

---

## 4. Pinmap vs. netlist cross-check

Source: `omi_net` column of `design/connector/ddr4_udimm_288_pinmap.csv` vs. net names in
`netlist.kicadxml.xml`.

| Metric | Value |
|---|---|
| Pinmap rows / unique `omi_net` names | 288 / **130** |
| Netlist nets | 238 |
| Intended `omi_net` names **present verbatim** in the netlist | **125 / 130 (96.2%)** |
| Intended names absent | **5** — `ALERT_n`, `PARITY`, `NC`, `VREF`, `VTT` |

**Interpretation (important — corrects an over-optimistic first read):** the high match is a
**naming-discipline** result, **not** a completeness result. The intended edge net *names*
(`D0_DQ0…`, `A0…A16`, `BA*`, `BG*`, `CK_t/c`, `SPD_*`, …) already exist as **labels** on the DRAM /
data / CA-CLK sheets — but they terminate at **placeholder host connectors**, not a real 288-pin UDIMM
edge symbol (which does not exist yet; see §5). Net *names* aligning with the pinmap ≠ a built edge
interface; the 131 ERC unconnected/undriven pins and the empty edge sheet show the interface is
**unbuilt**. Binding these names to the 288 physical edge pins is **P2/P3**. The 5 absent names are the
no-connect pseudo-net (`NC`), two rails not yet instantiated (`VREF`, `VTT`), and two controls
(`ALERT_n`; `PARITY` is disabled by design in v1).

---

## 5. Gap list (each finding confirmed from the artifacts, tagged to its owning phase)

| # | Finding (measured, not assumed) | Evidence (file : metric) | Owning phase |
|---|---|---|---|
| 1 | **Placeholder host connectors** stand in for a real 288-pin edge | netlist: `J_PWR/J_HOST/J_HOST_DQ_A·B·C/J_HOST_SPD`, values `…(placeholder)`, generic `Conn_01x*` symbols | P2 / P3 |
| 2 | **`udimm-edge-interface.kicad_sch` is an empty skeleton** — no edge symbol | file = 168 B, only header + empty `(lib_symbols)`; 0 components, 0 ERC, 0 nets contributed | P2 |
| 3 | **No real 288-pin edge connector** binding `omi_net` names to physical pins | pinmap 288 pins vs. netlist: names exist as labels, no edge component instance | P2 / P3 |
| 4 | **DRAM count = 8 (not 9)** — audit's "9" **not reproduced** | 8× `lib_id "Memory_RAM:H5AN8G8NAFR-UHC"` placements + refs `U_DRAM0…7`; netlist = 8; **0** `?`-unannotated, 0 instance dups | P3 *(anomaly resolved to 8)* |
| 5 | **All 8 DRAM sit on the address-command-clock sheet**, not the data sheet | netlist `<sheetpath>` = `/address-command-clock/` for every `U_DRAM*` | P3 *(note / possible reorg)* |
| 6 | **`schematic has annotation errors`** warning on netlist/BOM export | `_console_log.txt`; **not** a `?`-ref (0 across all sheets) and **not** an instance-ref duplicate (15 unique) — subtler (power-symbol / cross-sheet) trigger | P3 / P5 *(investigate; did not block export)* |
| 7 | **Footprints: 6 of 15 unassigned** — and they are exactly the placeholder connectors | netlist footprint field: 9/15 populated (8 DRAM `FBGA-78` + SPD) | P4 *(smaller than expected — DRAM/SPD already footprinted)* |
| 8 | **131 ERC violations** (108 not-connected, 16 not-driven, 5 power-not-driven, 2 dangling) | `erc_report.json` tally | P5 |
| 9 | **5 intended `omi_net` names absent** (`ALERT_n`, `PARITY`, `NC`, `VREF`, `VTT`) | pinmap vs. netlist (125/130 present) | P3 *(NC pseudo-net + PARITY by design; VREF/VTT = reference/termination rails)* |
| 10 | **No missing symbol/footprint libraries; no project lib tables** | netlist `libsource` = standard libs only; no `sym-/fp-lib-table` | — *(clean; no action)* |

**Headline corrections to the prior audit's assumptions** (the value of measuring):
- The **9-DRAM anomaly is refuted** at both the netlist and schematic-source level — there are exactly **8**.
- **Footprints are mostly assigned** (9/15), not ~0 — only the placeholder connectors lack them.
- The schematic's **net naming is ~96% aligned** with the intended edge pinmap already (125/130); the
  real gap is the **missing physical 288-pin edge connector**, not the net names.

---

## 6. Note

This document is a **measurement snapshot** of the schematic exactly as it stands on `main` at the time
of capture. Nothing was modified, fixed, built, or assigned. Building the edge symbol (P2), replacing
connectors / wiring the edge / resolving the DRAM-sheet placement (P3), assigning footprints (P4), and
driving ERC down (P5) are later phases, each with its own brief.
