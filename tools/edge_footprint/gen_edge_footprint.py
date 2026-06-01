# SPDX-License-Identifier: Apache-2.0
#
# Copyright 2026 The Open Memory Initiative (OMI) contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
"""Generate the 288-pad DDR4 UDIMM card-edge KiCad 9 footprint from the keystone pinmap.

This is the OMI v1 *Phase 4* footprint generator. It reads the single source of truth

    design/connector/ddr4_udimm_288_pinmap.csv   (header: pin,symbol,omi_net,group,notes)

and emits, deterministically and with **standard library only**, one KiCad 9.0 footprint

    design/power/omi_v1_power/omi.pretty/DDR4_UDIMM_288_Edge.kicad_mod

whose 288 pads mirror the J1 symbol's 288 pins exactly:

  * pad number  <- CSV ``pin``    (1..288, so pad set == symbol pin set == CSV pin set)
  * pad face    <- pin <= 144 -> front (F.Cu/F.Mask), else back (B.Cu/B.Mask)
                   (matches the symbol's 1..144-left / 145..288-right grouping and the
                    JEDEC DDR4 DIMM front/back-halves convention)
  * edge fingers as ``connect rect`` pads (copper + mask, no paste), two rows at the
    NOMINAL DDR4 UDIMM contact pitch (0.85 mm).

MECHANICAL CAVEAT (mandatory, also carried in the footprint descr/tags): the pad<->pin
numbering is correct at nominal pitch and is kicad-cli-validated, but this is NOT a
JEDEC-mechanically-verified card-edge. Exact notch/key position, board outline (Edge.Cuts),
pad dimensions/gold-finger plating, and keepouts are layout/mechanical concerns behind the
WALL and are explicitly NOT claimed. The footprint models only the 288 numbered pads (no
Edge.Cuts outline, no notch), so it asserts nothing mechanical. It is NOT fabrication-ready.

Determinism: every uuid is uuid5(NS, key); no timestamps, no RNG -> byte-identical re-runs.
The symbol library (omi.kicad_sym) and its generator (tools/edge_symbol/) are NOT touched;
J1's footprint is assigned on the schematic instance, preserving "symbol == CSV exactly".
"""
from __future__ import annotations

import argparse
import csv
import sys
import uuid
from pathlib import Path

FP_NAME = "DDR4_UDIMM_288_Edge"
NS = uuid.uuid5(uuid.NAMESPACE_URL,
                "https://github.com/The-Open-Memory-Initiative-OMI/omi/edge_footprint")

# --- nominal geometry (NOT mechanically verified; see caveat) ---
PITCH = 0.85          # mm, nominal DDR4 UDIMM contact pitch
PAD_W = 0.55          # mm, nominal finger width
PAD_H = 2.35          # mm, nominal finger height (copper into board)
N_PER_SIDE = 144      # 144 front + 144 back = 288

DESCR = (
    "DDR4 UDIMM 288-pin card-edge, 0.85mm NOMINAL pitch, 144 front (F.Cu) + 144 back "
    "(B.Cu) fingers; pad number = JEDEC pin per ddr4_udimm_288_pinmap.csv. CAVEAT: the "
    "pad-to-pin numbering is correct and kicad-cli-validated, but this is NOT a "
    "JEDEC-mechanically-verified card-edge -- exact notch/key position, board outline, pad "
    "dimensions/plating and keepouts are layout/mechanical concerns (behind the WALL) and "
    "are NOT claimed. Models pads only (no Edge.Cuts, no notch). Not fabrication-ready."
)
TAGS = "ddr4 udimm 288 card-edge dimm omi nominal pad-complete"


def _u(key: str) -> str:
    return str(uuid.uuid5(NS, key))


def _num(v: float) -> str:
    s = f"{v:.6f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def read_pins(csv_path: Path):
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rows.append((int(row["pin"]), row["symbol"], row["omi_net"]))
    rows.sort(key=lambda r: r[0])
    return rows


def pad_x_layers(pin: int):
    span = (N_PER_SIDE - 1) * PITCH
    x0 = -span / 2.0
    if pin <= N_PER_SIDE:
        return x0 + (pin - 1) * PITCH, '"F.Cu" "F.Mask"'
    return x0 + (pin - N_PER_SIDE - 1) * PITCH, '"B.Cu" "B.Mask"'


def _prop(name: str, value: str, at: str, layer: str, size: str, hide: bool, key: str):
    out = [f'\t(property "{name}" "{value}"', f"\t\t(at {at})"]
    if hide:
        out.append("\t\t(unlocked yes)")
    out.append(f'\t\t(layer "{layer}")')
    if hide:
        out.append("\t\t(hide yes)")
    out += [f'\t\t(uuid "{_u(key)}")',
            "\t\t(effects", "\t\t\t(font", f"\t\t\t\t(size {size})",
            "\t\t\t\t(thickness 0.15)", "\t\t\t)", "\t\t)", "\t)"]
    return out


def build(rows) -> str:
    L = [
        f'(footprint "{FP_NAME}"',
        "\t(version 20241229)",
        '\t(generator "gen_edge_footprint")',
        '\t(generator_version "9.0")',
        '\t(layer "F.Cu")',
        f'\t(descr "{DESCR}")',
        f'\t(tags "{TAGS}")',
    ]
    L += _prop("Reference", "REF**", "0 -3 0", "F.SilkS", "1 1", False, "prop.ref")
    L += _prop("Value", FP_NAME, "0 3 0", "F.Fab", "1 1", False, "prop.value")
    L += _prop("Datasheet", "", "0 0 0", "F.Fab", "1.27 1.27", True, "prop.datasheet")
    L += _prop("Description", DESCR, "0 0 0", "F.Fab", "1.27 1.27", True, "prop.description")
    L.append("\t(attr exclude_from_pos_files exclude_from_bom allow_soldermask_bridges)")
    L += ['\t(fp_text user "${REFERENCE}"', "\t\t(at 0 0 0)", '\t\t(layer "F.Fab")',
          f'\t\t(uuid "{_u("text.ref")}")',
          "\t\t(effects", "\t\t\t(font", "\t\t\t\t(size 1 1)", "\t\t\t\t(thickness 0.15)",
          "\t\t\t)", "\t\t)", "\t)"]
    for pin, _sym, _net in rows:
        x, layers = pad_x_layers(pin)
        L += [f'\t(pad "{pin}" connect rect',
              f"\t\t(at {_num(x)} 0)",
              f"\t\t(size {_num(PAD_W)} {_num(PAD_H)})",
              f"\t\t(layers {layers})",
              f'\t\t(uuid "{_u("pad." + str(pin))}")',
              "\t)"]
    L.append(")")
    return "\n".join(L) + "\n"


def verify(mod_path: Path, rows) -> int:
    """Re-parse the generated .kicad_mod; assert 288 pads numbered exactly 1..288 == CSV pins."""
    import re
    text = mod_path.read_text(encoding="utf-8")
    pad_nums = [int(m) for m in re.findall(r'\(pad "(\d+)"', text)]
    csv_pins = sorted(r[0] for r in rows)
    problems = []
    if len(pad_nums) != 288:
        problems.append(f"pad count {len(pad_nums)} != 288")
    if sorted(pad_nums) != csv_pins:
        problems.append("pad number set != CSV pin set")
    if len(set(pad_nums)) != len(pad_nums):
        problems.append("duplicate pad numbers")
    f_cu = text.count('(layers "F.Cu" "F.Mask")')
    b_cu = text.count('(layers "B.Cu" "B.Mask")')
    if (f_cu, b_cu) != (144, 144):
        problems.append(f"face split {f_cu}/{b_cu} != 144/144")
    if problems:
        print("VERIFY FAIL: " + "; ".join(problems))
        return 1
    print(f"VERIFY OK: 288 pads, numbers 1..288 == CSV pins, faces 144 F.Cu / 144 B.Cu")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the DDR4 UDIMM 288 card-edge footprint.")
    ap.add_argument("--csv", default="design/connector/ddr4_udimm_288_pinmap.csv")
    ap.add_argument("--out", default="design/power/omi_v1_power/omi.pretty/DDR4_UDIMM_288_Edge.kicad_mod")
    ap.add_argument("--verify", action="store_true", help="re-check the emitted footprint vs CSV")
    args = ap.parse_args(argv)

    rows = read_pins(Path(args.csv))
    if len(rows) != 288:
        print(f"ERROR: expected 288 CSV rows, got {len(rows)}", file=sys.stderr)
        return 2
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(rows), encoding="utf-8", newline="\n")
    print(f"wrote {out} ({len(rows)} pads)")
    if args.verify:
        return verify(out, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
