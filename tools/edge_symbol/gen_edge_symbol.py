# SPDX-License-Identifier: Apache-2.0
#
# Copyright 2026 The Open Memory Initiative (OMI) contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
"""Generate a 288-pin DDR4 UDIMM edge-connector KiCad 9 symbol from the keystone pinmap.

This is the OMI v1 *Phase 2* generator. It reads the single source of truth

    design/connector/ddr4_udimm_288_pinmap.csv   (header: pin,symbol,omi_net,group,notes)

and emits, deterministically and with **standard library only**:

  1. a KiCad 9.0 symbol library (``omi.kicad_sym``) holding one symbol,
     ``DDR4_UDIMM_288_Edge``, with all 288 pins; and
  2. (optionally) a populated copy of the edge sheet ``udimm-edge-interface.kicad_sch``
     placing one instance of that symbol (ref ``J1``) and attaching a ``global_label``
     (the dominant label type in this design) carrying the CSV ``omi_net`` to every
     non-NC pin, so the names merge across sheets.

CSV -> symbol pin mapping (CSV is authoritative):
  * pin number   <- CSV ``pin``
  * pin name     <- CSV ``symbol``   (the functional / JEDEC name shown on the body)
  * electrical type:
        - ``no_connect``  when ``omi_net == "NC"``  (ECC / CB / 2nd-rank / reserved pins)
        - otherwise ``passive``     (signals AND power/ground by default)

  Power pins default to ``passive`` on purpose: typing them ``power_in`` would require
  PWR_FLAGs to keep ERC quiet, which is a Phase-5 decision. Pass ``--power-type power_in``
  to opt into the stricter typing; the default keeps this additive phase ERC-neutral.

Geometry (all millimetres, 100-mil / 2.54 mm pitch):
  Two columns of 144 pins. Pins 1..144 exit left, 145..288 exit right. A pin's ``(at x y)``
  IS its electrical connection point; with the symbol placed at angle 0 (no mirror) the
  sheet coordinate of a pin is ``(Ox + x, Oy - y)`` (KiCad's symbol->sheet Y flip, verified
  against the existing Conn_01x05/GND wiring on the power sheet). Each non-NC pin therefore
  gets a global_label anchored exactly on that point -- no wires required.

Determinism: every UUID is derived with ``uuid.uuid5`` from a fixed namespace, so running
the generator twice on the same CSV produces byte-identical output (no timestamps, no RNG).

Validation is layered: this script self-checks the in-memory model, the caller round-trips
``omi.kicad_sym`` through ``kicad-cli sym upgrade`` + ``sym export svg``, and the ``verify``
sub-command re-parses the emitted symbol and diffs every pin number+name against the CSV.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import uuid
from pathlib import Path

# --------------------------------------------------------------------------------------
# Fixed identifiers from the existing design (read-only facts, captured during inspection)
# --------------------------------------------------------------------------------------
PROJECT_NAME = "omi_v1_power"
ROOT_SHEET_UUID = "464309c0-e3ad-4428-a43f-e1cf3b7a7d42"          # root .kicad_sch uuid
EDGE_SHEET_NODE_UUID = "9986c6c0-2ac4-474e-a00a-d8203c8bf46f"     # (sheet ...) node in root
EDGE_SHEET_FILE_UUID = "210817e1-752b-42f4-8fed-a870dd9e41c3"     # edge sheet's own uuid
# Hierarchical instance path for a symbol living on the edge sub-sheet:
EDGE_INSTANCE_PATH = f"/{ROOT_SHEET_UUID}/{EDGE_SHEET_NODE_UUID}"

# Deterministic-UUID namespace (arbitrary fixed constant -> reproducible output).
NS_UUID = uuid.UUID("b6e4f4a0-0c2e-5a7d-9f31-0a2b3c4d5e6f")

# Symbol / library naming
LIB_NICKNAME = "omi"
SYMBOL_NAME = "DDR4_UDIMM_288_Edge"
LIB_ID = f"{LIB_NICKNAME}:{SYMBOL_NAME}"
REFERENCE_PREFIX = "J"
PLACED_REFERENCE = "J1"

# KiCad format tokens (captured from the stock 9.0 Connector library / project sheets)
SYM_LIB_VERSION = 20241209
SCH_VERSION = 20250114

# Geometry
PITCH = 2.54
PIN_LENGTH = 5.08
X_OUT = 25.4                 # |x| of a pin's connection point in symbol-local coords
BODY_X = X_OUT - PIN_LENGTH  # 20.32 -> body rectangle half-width (pin meets body edge)
COL_SIZE = 144
TOP_Y = 71 * PITCH           # 180.34 -> y of the top pin (grid-aligned)
PLACE_OX = 60 * PITCH        # 152.4  -> sheet placement origin X (grid-aligned)
PLACE_OY = 75 * PITCH        # 190.5  -> sheet placement origin Y (keeps all y > 0)

NC_TOKEN = "NC"              # a row is No-Connect iff omi_net == "NC"

EXPECTED_PIN_COUNT = 288


# --------------------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------------------
class Pin:
    """One physical edge-finger: number, displayed name, net, and derived electrical type."""

    __slots__ = ("number", "name", "net", "group", "notes", "etype", "is_nc")

    def __init__(self, number: int, name: str, net: str, group: str, notes: str,
                 power_type: str):
        self.number = number
        self.name = name
        self.net = net
        self.group = group
        self.notes = notes
        self.is_nc = (net == NC_TOKEN)
        if self.is_nc:
            self.etype = "no_connect"
        elif group == "POWER":
            self.etype = power_type        # "passive" (default) or "power_in"
        else:
            self.etype = "passive"


def det_uuid(*parts: str) -> str:
    """Stable UUID from a fixed namespace and a dotted name -> reproducible files."""
    return str(uuid.uuid5(NS_UUID, ".".join(parts)))


def esc(s: str) -> str:
    r"""Escape a string for a KiCad s-expression double-quoted token (\\ and \")."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def read_pinmap(csv_path: Path, power_type: str) -> list[Pin]:
    """Parse and validate the pinmap CSV; return 288 Pins ordered by ascending pin number.

    Raises ValueError on any schema violation so a bad CSV can never yield a bad symbol.
    """
    with csv_path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        expected_header = ["pin", "symbol", "omi_net", "group", "notes"]
        if reader.fieldnames != expected_header:
            raise ValueError(
                f"unexpected CSV header {reader.fieldnames!r}; expected {expected_header!r}")
        pins: list[Pin] = []
        seen: set[int] = set()
        for lineno, row in enumerate(reader, start=2):
            raw_pin = (row["pin"] or "").strip()
            if raw_pin == "":
                raise ValueError(f"line {lineno}: empty pin number")
            number = int(raw_pin)
            if number in seen:
                raise ValueError(f"line {lineno}: duplicate pin number {number}")
            seen.add(number)
            name = (row["symbol"] or "").strip()
            net = (row["omi_net"] or "").strip()
            group = (row["group"] or "").strip()
            notes = (row["notes"] or "").strip()
            if name == "":
                raise ValueError(f"line {lineno}: empty symbol/name for pin {number}")
            if net == "":
                raise ValueError(f"line {lineno}: empty omi_net for pin {number}")
            pins.append(Pin(number, name, net, group, notes, power_type))

    if len(pins) != EXPECTED_PIN_COUNT:
        raise ValueError(f"expected {EXPECTED_PIN_COUNT} data rows, found {len(pins)}")
    pins.sort(key=lambda p: p.number)
    if [p.number for p in pins] != list(range(1, EXPECTED_PIN_COUNT + 1)):
        raise ValueError("pin numbers are not the contiguous range 1..288")
    return pins


# --------------------------------------------------------------------------------------
# Geometry helpers
# --------------------------------------------------------------------------------------
def fmt(n: float) -> str:
    """Format a millimetre coordinate the way KiCad does (trim trailing zeros)."""
    s = f"{n:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def local_pin_geometry(pin_number: int):
    """Return (local_x, local_y, pin_angle, column) for a pin in the symbol's own frame."""
    if pin_number <= COL_SIZE:                      # left column, exits left, body to right
        row = pin_number - 1
        return (-X_OUT, TOP_Y - row * PITCH, 0, "L")
    row = pin_number - COL_SIZE - 1                  # right column, exits right, body to left
    return (X_OUT, TOP_Y - row * PITCH, 180, "R")


def sheet_point(local_x: float, local_y: float):
    """Symbol-local -> edge-sheet coordinate for the J1 placement (angle 0, no mirror)."""
    return (PLACE_OX + local_x, PLACE_OY - local_y)


# --------------------------------------------------------------------------------------
# Emitters
# --------------------------------------------------------------------------------------
def _effects(*extra: str, hide: bool = False) -> list[str]:
    lines = ["(effects", "\t(font", "\t\t(size 1.27 1.27)", "\t)"]
    for e in extra:
        lines.append(f"\t{e}")
    if hide:
        lines.append("\t(hide yes)")
    lines.append(")")
    return lines


def _indent(block: list[str], tabs: int) -> list[str]:
    pad = "\t" * tabs
    return [pad + ln for ln in block]


def emit_symbol_body(pins: list[Pin]) -> list[str]:
    """The inner ``(symbol "..._1_1" ...)`` graphic unit: body rectangle + 288 pins."""
    out: list[str] = []
    out.append(f'(symbol "{SYMBOL_NAME}_1_1"')
    top = TOP_Y + PITCH
    bot = TOP_Y - (COL_SIZE - 1) * PITCH - PITCH
    out.append("\t(rectangle")
    out.append(f"\t\t(start {fmt(-BODY_X)} {fmt(top)})")
    out.append(f"\t\t(end {fmt(BODY_X)} {fmt(bot)})")
    out.append("\t\t(stroke")
    out.append("\t\t\t(width 0.254)")
    out.append("\t\t\t(type default)")
    out.append("\t\t)")
    out.append("\t\t(fill")
    out.append("\t\t\t(type background)")
    out.append("\t\t)")
    out.append("\t)")
    for p in pins:
        lx, ly, ang, _col = local_pin_geometry(p.number)
        out.append(f"\t(pin {p.etype} line")
        out.append(f"\t\t(at {fmt(lx)} {fmt(ly)} {ang})")
        out.append(f"\t\t(length {fmt(PIN_LENGTH)})")
        out.append(f'\t\t(name "{esc(p.name)}"')
        out.extend(_indent(_effects(), 3))
        out.append("\t\t)")
        out.append(f'\t\t(number "{p.number}"')
        out.extend(_indent(_effects(), 3))
        out.append("\t\t)")
        out.append("\t)")
    out.append(")")
    return out


def emit_symbol_definition() -> list[str]:
    """The library ``(symbol "DDR4_UDIMM_288_Edge" ...)`` header (properties + pin_names)."""
    out: list[str] = []
    out.append(f'(symbol "{SYMBOL_NAME}"')
    out.append("\t(pin_names")
    out.append("\t\t(offset 1.016)")
    out.append("\t)")
    out.append("\t(exclude_from_sim no)")
    out.append("\t(in_bom yes)")
    out.append("\t(on_board yes)")
    props = [
        ("Reference", REFERENCE_PREFIX, f"0 {fmt(TOP_Y + 3 * PITCH)} 0", False),
        ("Value", SYMBOL_NAME, f"0 {fmt(TOP_Y - (COL_SIZE - 1) * PITCH - 3 * PITCH)} 0", False),
        ("Footprint", "", "0 0 0", True),
        ("Datasheet", "~", "0 0 0", True),
        ("Description",
         "DDR4 UDIMM 288-pin edge connector; generated from ddr4_udimm_288_pinmap.csv",
         "0 0 0", True),
        ("ki_keywords", "DDR4 UDIMM 288 edge connector DIMM", "0 0 0", True),
    ]
    for name, value, at, hide in props:
        out.append(f'\t(property "{name}" "{esc(value)}"')
        out.append(f"\t\t(at {at})")
        out.extend(_indent(_effects(hide=hide), 2))
        out.append("\t)")
    return out


def emit_library(pins: list[Pin]) -> str:
    out: list[str] = []
    out.append("(kicad_symbol_lib")
    out.append(f"\t(version {SYM_LIB_VERSION})")
    out.append('\t(generator "kicad_symbol_editor")')
    out.append('\t(generator_version "9.0")')
    for ln in emit_symbol_definition():
        out.append("\t" + ln)
    for ln in emit_symbol_body(pins):
        out.append("\t\t" + ln)
    out.append("\t\t(embedded_fonts no)")
    out.append("\t)")
    out.append(")")
    return "\n".join(out) + "\n"


def emit_global_label(net: str, x: float, y: float, column: str, uid: str) -> list[str]:
    """One global_label anchored on a pin's connection point (matches the BA0 convention)."""
    if column == "L":           # pin exits left -> label reads leftwards
        angle, justify, ir_x = 180, "right", x - 2.54
    else:                       # pin exits right -> label reads rightwards
        angle, justify, ir_x = 0, "left", x + 2.54
    out = [
        f'(global_label "{esc(net)}"',
        "\t(shape input)",
        f"\t(at {fmt(x)} {fmt(y)} {angle})",
        "\t(fields_autoplaced yes)",
        "\t(effects",
        "\t\t(font",
        "\t\t\t(size 1.27 1.27)",
        "\t\t)",
        f"\t\t(justify {justify})",
        "\t)",
        f'\t(uuid "{uid}")',
        '\t(property "Intersheetrefs" "${INTERSHEET_REFS}"',
        f"\t\t(at {fmt(ir_x)} {fmt(y)} 0)",
        "\t\t(effects",
        "\t\t\t(font",
        "\t\t\t\t(size 1.27 1.27)",
        "\t\t\t)",
        f"\t\t\t(justify {justify})",
        "\t\t\t(hide yes)",
        "\t\t)",
        "\t)",
        ")",
    ]
    return out


def emit_placed_symbol(pins: list[Pin]) -> list[str]:
    """The ``(symbol (lib_id omi:...) ...)`` instance for J1 on the edge sheet."""
    out: list[str] = []
    out.append("(symbol")
    out.append(f'\t(lib_id "{LIB_ID}")')
    out.append(f"\t(at {fmt(PLACE_OX)} {fmt(PLACE_OY)} 0)")
    out.append("\t(unit 1)")
    out.append("\t(exclude_from_sim no)")
    out.append("\t(in_bom yes)")
    out.append("\t(on_board yes)")
    out.append("\t(dnp no)")
    out.append(f'\t(uuid "{det_uuid("placed", "j1")}")')
    ref_at = f"{fmt(PLACE_OX - BODY_X)} {fmt(PLACE_OY - TOP_Y - 3 * PITCH)} 0"
    val_at = f"{fmt(PLACE_OX - BODY_X)} {fmt(PLACE_OY - (TOP_Y - (COL_SIZE - 1) * PITCH) + 3 * PITCH)} 0"
    placed_props = [
        ("Reference", PLACED_REFERENCE, ref_at, False),
        ("Value", SYMBOL_NAME, val_at, False),
        ("Footprint", "", f"{fmt(PLACE_OX)} {fmt(PLACE_OY)} 0", True),
        ("Datasheet", "~", f"{fmt(PLACE_OX)} {fmt(PLACE_OY)} 0", True),
    ]
    for name, value, at, hide in placed_props:
        out.append(f'\t(property "{name}" "{esc(value)}"')
        out.append(f"\t\t(at {at})")
        out.extend(_indent(_effects(hide=hide), 2))
        out.append("\t)")
    for p in pins:
        out.append(f'\t(pin "{p.number}"')
        out.append(f'\t\t(uuid "{det_uuid("placed", "j1", "pin", str(p.number))}")')
        out.append("\t)")
    out.append("\t(instances")
    out.append(f'\t\t(project "{PROJECT_NAME}"')
    out.append(f'\t\t\t(path "{EDGE_INSTANCE_PATH}"')
    out.append(f'\t\t\t\t(reference "{PLACED_REFERENCE}")')
    out.append("\t\t\t\t(unit 1)")
    out.append("\t\t\t)")
    out.append("\t\t)")
    out.append("\t)")
    out.append(")")                 # close the (symbol ...) instance node
    return out


def emit_sheet(pins: list[Pin]) -> str:
    """The fully-populated ``udimm-edge-interface.kicad_sch`` (header + lib_symbols + content)."""
    out: list[str] = []
    out.append("(kicad_sch")
    out.append(f"\t(version {SCH_VERSION})")
    out.append('\t(generator "eeschema")')
    out.append('\t(generator_version "9.0")')
    out.append(f'\t(uuid "{EDGE_SHEET_FILE_UUID}")')
    out.append('\t(paper "A2")')

    # Embedded library symbol: same body, but the wrapper is named with the lib_id.
    out.append("\t(lib_symbols")
    out.append(f'\t\t(symbol "{LIB_ID}"')
    for ln in emit_symbol_definition()[1:]:          # drop the '(symbol "NAME"' opener
        out.append("\t\t\t" + ln)
    for ln in emit_symbol_body(pins):
        out.append("\t\t\t\t" + ln)
    out.append("\t\t\t\t(embedded_fonts no)")
    out.append("\t\t)")
    out.append("\t)")

    # Global labels for every non-NC pin, anchored exactly on the pin connection point.
    for p in pins:
        if p.is_nc:
            continue
        lx, ly, _ang, col = local_pin_geometry(p.number)
        sx, sy = sheet_point(lx, ly)
        uid = det_uuid("label", str(p.number))
        for ln in emit_global_label(p.net, sx, sy, col, uid):
            out.append("\t" + ln)

    # The J1 instance.
    for ln in emit_placed_symbol(pins):
        out.append("\t" + ln)

    out.append("\t(embedded_fonts no)")
    out.append(")")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------------------
# Verify: re-parse an emitted .kicad_sym and diff against the CSV
# --------------------------------------------------------------------------------------
def _tokenize(text: str):
    return re.findall(r'"(?:[^"\\]|\\.)*"|\(|\)|[^\s()]+', text)


def _parse(tokens):
    """Recursive-descent s-expression -> nested lists; strings keep a leading '"' marker."""
    it = iter(tokens)

    def build():
        node = []
        for tok in it:
            if tok == "(":
                node.append(build())
            elif tok == ")":
                return node
            else:
                node.append(tok)
        return node

    for tok in it:
        if tok == "(":
            return build()
    return []


def _unq(tok: str) -> str:
    if tok.startswith('"') and tok.endswith('"'):
        return tok[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return tok


def _walk_pins(node, found):
    if not isinstance(node, list) or not node:
        return
    if node[0] == "pin" and len(node) >= 3 and isinstance(node[1], str):
        etype = node[1]
        name = number = None
        for child in node:
            if isinstance(child, list) and child:
                if child[0] == "name":
                    name = _unq(child[1])
                elif child[0] == "number":
                    number = _unq(child[1])
        if name is not None and number is not None:
            found.append((number, name, etype))
    for child in node:
        if isinstance(child, list):
            _walk_pins(child, found)


def verify(sym_path: Path, csv_path: Path, power_type: str) -> int:
    """Assert the emitted symbol has 288 pins exactly matching the CSV (number+name+type)."""
    pins = read_pinmap(csv_path, power_type=power_type)
    expected_by_number = {str(p.number): p for p in pins}
    text = sym_path.read_text(encoding="utf-8")
    root = _parse(_tokenize(text))
    found: list[tuple[str, str, str]] = []
    _walk_pins(root, found)

    errors: list[str] = []
    if len(found) != EXPECTED_PIN_COUNT:
        errors.append(f"pin count is {len(found)}, expected {EXPECTED_PIN_COUNT}")

    seen_numbers = set()
    for number, name, etype in found:
        seen_numbers.add(number)
        exp = expected_by_number.get(number)
        if exp is None:
            errors.append(f"pin {number}: not in CSV")
            continue
        if name != exp.name:
            errors.append(f"pin {number}: name {name!r} != CSV {exp.name!r}")
        if etype != exp.etype:
            errors.append(f"pin {number}: type {etype!r} != expected {exp.etype!r}")
    missing = set(expected_by_number) - seen_numbers
    for number in sorted(missing, key=int):
        errors.append(f"pin {number}: missing from symbol")

    hist: dict[str, int] = {}
    for _n, _nm, etype in found:
        hist[etype] = hist.get(etype, 0) + 1

    if errors:
        print("VERIFY: FAIL")
        for e in errors[:50]:
            print("  - " + e)
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more")
        return 1
    print("VERIFY: PASS")
    print(f"  pins matched exactly against CSV: {len(found)}/{EXPECTED_PIN_COUNT}")
    print(f"  electrical-type histogram: {dict(sorted(hist.items()))}")
    return 0


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------
def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main(argv: list[str]) -> int:
    root = repo_root()
    default_csv = root / "design" / "connector" / "ddr4_udimm_288_pinmap.csv"
    proj_dir = root / "design" / "power" / "omi_v1_power"
    default_sym = proj_dir / "omi.kicad_sym"
    default_sheet = proj_dir / "udimm-edge-interface.kicad_sch"

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", type=Path, default=default_csv)
    ap.add_argument("--out-sym", type=Path, default=default_sym)
    ap.add_argument("--out-sheet", type=Path, default=default_sheet)
    ap.add_argument("--power-type", choices=["passive", "power_in"], default="passive",
                    help="electrical type for POWER-group pins (default: passive; "
                         "power_in is the stricter Phase-5 option and needs PWR_FLAGs)")
    ap.add_argument("--no-sheet", action="store_true",
                    help="emit only the symbol library (defer placement)")
    ap.add_argument("--verify", action="store_true",
                    help="instead of generating, re-parse --out-sym and diff against the CSV")
    args = ap.parse_args(argv)

    if args.verify:
        return verify(args.out_sym, args.csv)

    pins = read_pinmap(args.csv, args.power_type)

    nc = sum(1 for p in pins if p.is_nc)
    power = sum(1 for p in pins if (not p.is_nc) and p.group == "POWER")
    signal = len(pins) - nc - power
    hist: dict[str, int] = {}
    for p in pins:
        hist[p.etype] = hist.get(p.etype, 0) + 1

    args.out_sym.parent.mkdir(parents=True, exist_ok=True)
    args.out_sym.write_text(emit_library(pins), encoding="utf-8")
    print(f"wrote symbol library: {args.out_sym}")
    print(f"  pins={len(pins)}  NC={nc}  power={power}  signal={signal}")
    print(f"  electrical-type histogram: {dict(sorted(hist.items()))}")

    if not args.no_sheet:
        args.out_sheet.write_text(emit_sheet(pins), encoding="utf-8")
        labelled = sum(1 for p in pins if not p.is_nc)
        print(f"wrote populated edge sheet: {args.out_sheet}")
        print(f"  J1 placed; {labelled} global_labels; {nc} NC pins left unconnected")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
