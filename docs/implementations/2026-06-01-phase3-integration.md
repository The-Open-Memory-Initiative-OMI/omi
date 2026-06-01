# Phase 3 — Cross-sheet integration (the surgery phase)

**Date:** 2026-06-01
**Branch:** `phase3-integration` (based on `phase2-edge-symbol`, which carries `J1`)
**Status:** in progress — plan documented before edits per the documentation-first rule.
**Tooling:** `kicad-cli` 9.0.8 (KiCad 9.0, format `20250114`); `powershell.exe`.

---

## 1. Problem / Motivation

Phase 2 added the real 288-pin host edge connector `J1` (`omi:DDR4_UDIMM_288_Edge`) on
`udimm-edge-interface.kicad_sch` and wired it to the design via `global_label`s. It was
deliberately **additive**: it left in place the 6 pre-existing **placeholder host
connectors** (`J_PWR`, `J_HOST`, `J_HOST_DQ_A/B/C`, `J_HOST_SPD`) that `J1` now supersedes,
and it left ~5 connector-side nets unaligned with the rest of the design. Going in, ERC =
**135** and `kicad-cli sch export netlist` still prints *"schematic has annotation errors."*

Phase 3 is the first phase that edits **multiple existing sheets** and **removes
components**. Its job is to *integrate* `J1`: reconcile the unaligned nets, remove the now-
redundant placeholders once `J1` verifiably carries their nets, and clear the annotation
warning — validating after every change and committing incrementally so any regression is
revertible. It does **not** drive ERC to zero; the DRAM-pin-level and power-flag ERC is
explicitly handed to Phase 5, and footprints to Phase 4.

## 2. Measured state going in (baseline, ERC = 135)

| Sheet | Count | Breakdown |
| --- | --- | --- |
| `/` (root) | 6 | 3 `global_label_dangling` (VREF, ALERT_n, PARITY) · 2 `label_dangling` (VREF, VDDQ stubs on `J_PWR`) · 1 `power_pin_not_driven` (#PWR06 GND) |
| `/address-command-clock/` | 94 | 75 `pin_not_connected` · 16 `pin_not_driven` · 3 `power_pin_not_driven` |
| `/data-byte-lanes-dqs/` | 32 | 32 `pin_not_connected` |
| `/spd-and-configuration/` | 2 | 1 `pin_not_connected` · 1 `power_pin_not_driven` |
| `/udimm-edge-interface/` | 1 | 1 `same_local_global_label` (VREF) |

Pre-existing baseline reconciles exactly: 108 `pin_not_connected` + 16 `pin_not_driven` +
5 `power_pin_not_driven` + 2 `label_dangling` = 131, plus Phase 2's **+4** = 135.

**Correction to the brief's measured state (verified against the ERC JSON):** the three
`global_label_dangling` items are **VREF, ALERT_n, PARITY** — *not* VTT. `VTT` is a valid
**2-node net** (`J1` pins 77 + 221 tied via two matching global labels), so it carries **no
ERC violation** and needs no action. The P3-owned **+4** are therefore: VREF-dangling,
VREF-same-local-global, ALERT_n-dangling, PARITY-dangling.

## 3. Diagnosis (read-only fan-out + netlist/ERC ground truth)

- **Net gap (5 unaligned):** 129 distinct `omi_net` names; 125 merge `J1` with the design.
  The unaligned: **VREF** (fragmented 3 ways — root `J_PWR` local, edge `J1` global, 8 DRAM
  VREFCA locals), **ALERT_n** / **PARITY** (J1-only dangling globals; CSV marks
  host-supplied / not-enabled-in-v1; DRAM `~{ALERT}`/`PAR` pins are left NC per CSV),
  **VTT** (J1-only but a valid 2-node net → no violation), and **VDDQ** (the "5th": a root
  `J_PWR` local stub `/VDDQ` that never merges with the DRAM VDDQ rail; `J1` has no VDDQ edge
  pin, correctly).
- **Placeholders — all 6 verified safe to remove** (netlist node check): every *connected*
  pin's net contains `J1` **and** the relevant DRAM/SPD device, so no removal isolates `J1`
  from a DRAM. `J_HOST` pin 29 `A17` = `{8 DRAMs}` only (J1 omits A17, correct per CSV "A17
  NC for 8Gb"); it stays inter-connected after removal. `J_PWR` `/VDDQ`+`/VREF` are dead
  stubs (zero other nodes). No placeholder is a jumper.
- **Annotation warning root cause:** the 6 placeholders carry references with **no numeric
  suffix** (`J_PWR`, `J_HOST`, …). KiCad requires `prefix+integer`; the project sets
  `unannotated = error`, so netlist export warns. **Removing all 6 placeholders clears the
  warning** — §8 and §9 share one root cause. (`J1`, `U_DRAM0–7`, `U_SPD0`, `#PWR*` are all
  properly annotated.)
- **Hierarchy:** all 4 children are properly instantiated as sheet boxes with valid
  `sheet_instances` + per-symbol instance paths; connectivity rides on `global_label`s by
  design. Adding sheet-pins would be **cosmetic** → §10 skipped (documented, not done).

## 4. Plan (each step validated with the ERC+netlist pair, one commit each)

1. **ALERT_n → no-connect** (edge): delete the dangling `global_label "ALERT_n"` at its J1
   pin endpoint (177.8, 170.18) and place a `(no_connect)` there. Clears 1 dangling.
2. **PARITY → no-connect** (edge): same at (177.8, 205.74). Clears 1 dangling.
3. **J_HOST_SPD removal** (spd): symbol + its 7 pin global-labels (x=73.66) + 7 wires; keep
   `U_SPD0` and its labels. Clears the 1 spd `pin_not_connected`; proves the removal pattern.
4. **J_HOST_DQ_A removal** (data, x-column 30.48): symbol + 33 labels + 33 wires.
5. **J_HOST_DQ_B removal** (data, x-column 96.52): symbol + 33 labels + 33 wires.
6. **J_HOST_DQ_C removal** (data, x-column 161.29): symbol + 22 labels + 22 wires (sheet now
   holds only its descriptive `text` note). Removes all 32 data `pin_not_connected`.
7. **J_HOST removal** (acc): symbol + 29 labels (y=24.13) + 29 wires; keeps the 8 DRAMs.
   Removes 11 `pin_not_connected` (its NC pins 30–40); `A17` stays an 8-DRAM net.
8. **VREF merge** (acc): convert the 8 DRAM `label "VREF"` → `global_label "VREF"` (same
   anchor) so DRAM VREFCA merges with `J1` global VREF. Clears VREF `global_label_dangling`.
9. **J_PWR removal** (root): symbol + the 2 dead stub labels (VREF, VDDQ) + their 2 wires;
   keep `#PWR04/05/06`. Clears 2 `label_dangling` + `same_local_global` (last local VREF
   gone) + the annotation warning (last non-numeric ref gone). VDDQ "5th net": the dangling
   root stub disappears; the DRAM VDDQ rail is left for P5.

**VTT:** no action (already a clean 2-node net consistent with CSV "not enabled in v1").
**Hierarchy:** skipped (connectivity already correct via global labels).

## 5. Net-reconciliation rationale (why VREF is handled on the DRAM side)

The brief's literal instruction was "convert the *root* local VREF to global." Investigation
showed the root local VREF **is** `J_PWR` pin-4's label, and `J_PWR` is a placeholder being
removed. Converting it to global and then removing `J_PWR` would re-strand VREF. The
electrically-correct, intent-honoring fix is to promote the **8 DRAM VREFCA** local labels
(the real consumers) to global so VREF spans `J1` pin 146 → all 8 DRAM VREFCA inputs; the
root local VREF then disappears with `J_PWR`, clearing `same_local_global`. This is net
reconciliation (P3), not DRAM-pin ERC (P5).

ALERT_n / PARITY are marked intentionally unconnected with a **sheet-level `no_connect`
flag** (never a symbol retype — the "symbol == CSV exactly" invariant holds), per the CSV's
"host-supplied / not-enabled-in-v1" note.

## 6. What Changed

| File | Change | Description |
| --- | --- | --- |
| `design/power/omi_v1_power/udimm-edge-interface.kicad_sch` | modified | ALERT_n, PARITY global labels → `no_connect` flags. |
| `design/power/omi_v1_power/spd-and-configuration.kicad_sch` | modified | Removed `J_HOST_SPD` + its labels/wires. |
| `design/power/omi_v1_power/data-byte-lanes-dqs.kicad_sch` | modified | Removed `J_HOST_DQ_A/B/C` + their labels/wires. |
| `design/power/omi_v1_power/address-command-clock.kicad_sch` | modified | Removed `J_HOST`; converted 8 DRAM VREF labels local→global. |
| `design/power/omi_v1_power/omi_v1_power.kicad_sch` | modified | Removed `J_PWR` + its 2 dead stub labels/wires. |
| `build/p3/erc_*.json`, `build/p3/netlist_final.xml` | added | Per-step ERC + final netlist evidence. |

Untouched: the P2 symbol (`omi.kicad_sym`) and generator (`tools/edge_symbol/**`), the CSV,
`validation/**` scripts/evidence, and the `.kicad_pcb`.

## 7. Verification

_(Filled in during execution — per-step ERC deltas, final count, connectivity sanity.)_

## 8. Remaining (handoff)

- **Phase 4:** assign `J1`'s footprint; confirm DRAM/SPD footprints.
- **Phase 5:** the DRAM-pin-level `pin_not_connected` / `pin_not_driven` and the power-flag
  (`power_pin_not_driven`) decision — i.e. the residual ERC after P3. Not driven to zero here.

## 9. Related Docs

- `PHASE3_INTEGRATION_BRIEF.md` (authoritative spec, untracked working doc).
- `docs/implementations/2026-06-01-phase2-edge-symbol.md` (the J1 symbol + placement).
