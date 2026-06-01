# Phase 4 — Footprint assignment

**Date:** 2026-06-01
**Branch:** `phase4-footprints` (based on `phase3-integration`, the P3-bearing base)
**Status:** complete — J1 footprint generated + assigned; all real components footprinted; ERC unchanged at 85; PR open (not merged).
**Tooling:** `kicad-cli` 9.0.8 (KiCad 9.0, format `20250114`); `powershell.exe`.

---

## 1. Problem / Motivation

Phase 3 left the schematic logically complete: J1 (the 288-pin edge connector) is integrated,
the placeholder connectors are gone, ERC is a justified 85. But the **netlist/BOM are not yet
complete** — a component needs a *footprint* to appear in a board netlist with a land pattern.
The 8 DRAM and the SPD already carry footprints; **J1 has none**. Phase 4 is the **last
pre-layout step on the schematic side of the WALL**: it *assigns* footprints so the netlist is
complete. It places **nothing** on a board, does **not** touch the `.kicad_pcb`, and makes
**no** claim of mechanical / fabrication readiness.

## 2. Measured state going in (audited)

- 15 components: `J1` (`omi:DDR4_UDIMM_288_Edge`), `U_DRAM0–7` (`Memory_RAM:H5AN8G8NAFR-UHC`),
  `U_SPD0` (`Memory_EEPROM:AT24CS01-MAHM`), and `#PWR*` power symbols (no footprint — correct).
- **DRAM footprint — CONFIRMED correct, no change:** `Package_BGA:FBGA-78_7.5x11mm_Layout2x3x13_P0.8mm`
  — resolves; 78 pads, ball designators A1…N9; **clean 1:1** with the symbol's 78 ball-designator
  pins (verified against footprint, symbol, and netlist); correct JEDEC DDR4-×8 78-ball FBGA.
- **SPD footprint — CONFIRMED correct, no change:** `Package_DFN_QFN:DFN-8-1EP_3x2mm_P0.5mm_EP1.3x1.5mm`
  — resolves; 9 pads (1–8 + EP pad "9"); symbol pin 9 = EP tied to GND; `AT24CS01-MAHM` decodes
  to UDFN-8 2×3mm (Microchip code 8MA2) → this DFN-8 land pattern is correct.
- **J1 footprint — MISSING; no stock library footprint fits.** The closest stock part,
  `Connector_PCBEdge:SODIMM-260_DDR4_..._Socket`, is a 260-pin SODIMM *socket* — wrong pin count
  and wrong type. So J1's footprint is **generated** (below).
- ERC = 85 (footprints do not affect ERC — that residual is P5's). No project `fp-lib-table` yet.

## 3. Plan

1. **DRAM + SPD:** confirm only (audit above shows both resolve, correct package, pad↔pin clean).
   No edits.
2. **Generate J1's footprint** (stdlib-only Python, Apache-2.0 SPDX header, CSV as the single
   source of truth) → `design/power/omi_v1_power/omi.pretty/DDR4_UDIMM_288_Edge.kicad_mod`:
   - **288 pads, pad number ← CSV `pin`** (so pad set = {1..288} = the J1 symbol's pin set).
   - Edge-finger pads (`connect rect`, copper + mask, no paste), two rows at the **nominal**
     DDR4 UDIMM pitch (0.85 mm): pins **1–144 → front (F.Cu/F.Mask)**, **145–288 → back
     (B.Cu/B.Mask)** — mirroring the symbol's 1–144-left / 145–288-right grouping and the JEDEC
     DDR4 DIMM front/back-halves convention. Deterministic pad uuids (`uuid5`).
   - `attr exclude_from_pos_files exclude_from_bom allow_soldermask_bridges` (a board edge, not a
     placed/BOM part). Reference `REF**`, Value `DDR4_UDIMM_288_Edge` (matches the symbol value).
3. **Register a project `fp-lib-table`** (nickname `omi` → `${KIPRJMOD}/omi.pretty`), mirroring
   the P2 `sym-lib-table`.
4. **Assign** the footprint on the **J1 schematic instance** (Footprint property on the edge
   sheet) = `omi:DDR4_UDIMM_288_Edge`. The symbol library `omi.kicad_sym` and the symbol
   generator stay **byte-frozen** (the "symbol == CSV exactly" invariant is preserved).
5. **Validate:** `fp upgrade` clean + `fp export svg` renders; assert the `.kicad_mod` has
   exactly 288 pads numbered {1..288}; netlist shows footprints for all real components; ERC
   **unchanged at 85**; J1 still 288 pins.

## 4. Mechanical caveat (MANDATORY — carried in the footprint, here, and flagged for P7)

The generated card-edge footprint has **correct pad↔pin numbering at nominal pitch and is
kicad-cli-validated**, but it is **NOT a JEDEC-mechanically-verified card-edge.** Exact notch /
key position, board outline (`Edge.Cuts`), pad dimensions / gold-finger plating, and keepouts are
**layout / mechanical concerns behind the WALL** and are **explicitly not claimed**. The
footprint deliberately models **only the 288 numbered pads** (no `Edge.Cuts` outline, no notch) so
it makes no unverified mechanical assertion. It is **not** a fabrication-ready footprint. This
caveat is duplicated in the footprint's `descr`/`tags` so it travels inside KiCad.

## 5. What Changed

| File | Change | Description |
| --- | --- | --- |
| `tools/edge_footprint/gen_edge_footprint.py` | added | Stdlib-only generator: CSV → `omi.pretty/DDR4_UDIMM_288_Edge.kicad_mod`; `--verify` re-checks 288 pads ↔ CSV pins. |
| `design/power/omi_v1_power/omi.pretty/DDR4_UDIMM_288_Edge.kicad_mod` | added | Generated 288-pad card-edge footprint (nominal geometry; mechanical caveat in `descr`). |
| `design/power/omi_v1_power/fp-lib-table` | added | Project footprint-lib table registering nickname `omi` → `omi.pretty`. |
| `design/power/omi_v1_power/udimm-edge-interface.kicad_sch` | modified | The single schematic edit: set J1's Footprint property to `omi:DDR4_UDIMM_288_Edge`. |
| `build/p4/*` | added | kicad-cli evidence (SVG render, netlist, ERC, pad-match report). |

Untouched: `omi.kicad_sym` + `tools/edge_symbol/**` (frozen), the CSV, `validation/**`, the
`.kicad_pcb`, the DRAM/SPD footprints, and ERC.

## 6. Verification

**DRAM + SPD (confirm-only, no change):**
- U_DRAM0–7 = `Package_BGA:FBGA-78_7.5x11mm_Layout2x3x13_P0.8mm` — resolves; 78 ball-designator
  pads = 78 symbol pins (clean 1:1, verified against footprint + symbol + netlist); correct
  JEDEC DDR4-×8 78-ball FBGA.
- U_SPD0 = `Package_DFN_QFN:DFN-8-1EP_3x2mm_P0.5mm_EP1.3x1.5mm` — resolves; pads 1–8 + EP "9";
  symbol pin 9 = EP→GND; `-MAHM` = UDFN-8 2×3mm (8MA2) → correct land pattern.

**J1 (generated):**
- `gen_edge_footprint.py --verify` → **288 pads, numbers 1..288 == CSV pins, 144 F.Cu / 144 B.Cu.**
- `kicad-cli fp upgrade` → exit 0, *"library was not updated"* (output already canonical KiCad-9).
- `kicad-cli fp export svg` → exit 0, rendered `DDR4_UDIMM_288_Edge.svg` (104 KB).
- `fp-lib-table` registers nickname `omi` → `${KIPRJMOD}/omi.pretty`.
- J1 instance Footprint property set to `omi:DDR4_UDIMM_288_Edge` (1-line edit on the edge sheet;
  `omi.kicad_sym` + `tools/edge_symbol/**` untouched).

**Whole-design (kicad-cli on the root):**
- Netlist footprint coverage: **10/10 real components** carry a resolvable footprint (J1,
  U_DRAM0–7, U_SPD0); power symbols are not in the component list (carry none — correct).
- **J1 pad↔pin:** footprint pads {1..288} == symbol pins {1..288} (sets exactly equal).
- **ERC = 85, unchanged** (footprints don't affect ERC; the residual is P5's).
- Symbol invariant intact: J1 still 288 pins; `omi.kicad_sym` byte-unchanged.

## 7. Remaining (handoff)

- **P5:** the residual **85** ERC — 64 `pin_not_connected` + 16 `pin_not_driven` (DRAM I/O) + 5
  `power_pin_not_driven` (power-flag decision). Footprints do not change it.
- **P7:** carry the J1 mechanical caveat into the README/claims (do not overstate the footprint
  as fabrication-ready).

## 8. Related Docs

- `PHASE4_FOOTPRINTS_BRIEF.md` (authoritative spec, untracked working doc).
- `docs/implementations/2026-06-01-phase3-integration.md` (J1 integration).
- `docs/implementations/2026-06-01-phase2-edge-symbol.md` (the J1 symbol; the generator pattern this footprint generator mirrors).
