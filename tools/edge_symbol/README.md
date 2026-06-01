# `gen_edge_symbol.py` — 288-pin DDR4 UDIMM edge-connector generator

`gen_edge_symbol.py` turns the keystone pinmap into the KiCad artifacts for the UDIMM
edge connector. It is **standard-library-only Python 3** (no pip dependencies) and is
fully deterministic: the same CSV always produces byte-identical output.

## What it reads

```
design/connector/ddr4_udimm_288_pinmap.csv     # header: pin,symbol,omi_net,group,notes
```

This CSV is the **single source of truth** and is never modified by the generator.

## What it writes

| Output | Path (default) | Notes |
| --- | --- | --- |
| Symbol library | `design/power/omi_v1_power/omi.kicad_sym` | one symbol, `DDR4_UDIMM_288_Edge`, 288 pins |
| Populated edge sheet | `design/power/omi_v1_power/udimm-edge-interface.kicad_sch` | one `J1` instance + `global_label` per non-NC pin |

The library is registered in `design/power/omi_v1_power/sym-lib-table` under the nickname
`omi`, so the symbol's `lib_id` is `omi:DDR4_UDIMM_288_Edge`.

## CSV → symbol mapping

* **pin number** ← CSV `pin`
* **pin name** ← CSV `symbol` (the JEDEC / functional name shown on the body)
* **electrical type**:
  * `no_connect` when `omi_net == "NC"` (ECC/CB lanes, 2nd-rank, reserved — kept out of the
    ERC "unconnected" tally by design);
  * `passive` otherwise — **including power/ground by default**. Power pins can be promoted to
    `power_in` with `--power-type power_in`, but that requires PWR_FLAGs to satisfy ERC and is a
    Phase-5 decision, so `passive` is the default to keep this additive phase ERC-neutral.

Net labels use **`global_label`**, the dominant label type in this design, so the `omi_net`
names merge across sheets automatically. NC pins are left unconnected (their `no_connect`
type makes that ERC-clean); they are never labelled with a signal net.

## Regenerate

```powershell
python tools\edge_symbol\gen_edge_symbol.py
```

Useful flags:

| Flag | Effect |
| --- | --- |
| `--no-sheet` | emit only the symbol library (defer placement) |
| `--power-type power_in` | type POWER-group pins `power_in` instead of `passive` (needs PWR_FLAGs; Phase 5) |
| `--verify` | re-parse `omi.kicad_sym` and assert 288 pins whose number+name+type match the CSV exactly |
| `--csv / --out-sym / --out-sheet` | override input/output paths |

## Validate (KiCad 9.0 `kicad-cli`)

```powershell
$bin = "$env:LOCALAPPDATA\Programs\KiCad\9.0\bin\kicad-cli.exe"
& $bin sym upgrade -o build\p2\omi_upgraded.kicad_sym design\power\omi_v1_power\omi.kicad_sym
& $bin sym export svg -o build\p2 design\power\omi_v1_power\omi.kicad_sym
python tools\edge_symbol\gen_edge_symbol.py --verify
& $bin sch erc --severity-all --format json -o build\p2\erc_after.json design\power\omi_v1_power\omi_v1_power.kicad_sch
& $bin sch export netlist --format kicadxml -o build\p2\netlist_after.xml design\power\omi_v1_power\omi_v1_power.kicad_sch
```

Use the **KiCad 9.0** `kicad-cli` (schematic format `20250114`), not 10.x.
