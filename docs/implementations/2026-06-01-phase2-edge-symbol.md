# Phase 2 — 288-pin DDR4 UDIMM edge-connector symbol (generated from CSV)

**Date:** 2026-06-01
**Branch:** `phase2-edge-symbol`
**Status:** complete; placement validated end-to-end with `kicad-cli` 9.0.8.

---

## 1. Problem / Motivation

The OMI v1 schematic carries an empty 168-byte skeleton sheet,
`design/power/omi_v1_power/udimm-edge-interface.kicad_sch`, where the physical 288-pin DDR4
UDIMM edge connector belongs. Until that connector exists, the host-side interface is
described only by placeholder connectors and floating `global_label`s, so the design cannot
be called complete. Hand-drawing a 288-pin part is an error farm; the keystone pinmap CSV
already encodes the JEDEC pin→net mapping authoritatively. Phase 2 turns that CSV into a
**generated, validated** KiCad symbol and places one instance on the edge sheet so the
`omi_net` names line up with the rest of the design.

This is an **additive** phase. It deliberately does **not** fix ERC, remove placeholders,
reconcile net-name mismatches, or add root sheet-pins — those are Phases 3/5.

## 2. What Changed

| File | Change | Description |
| --- | --- | --- |
| `tools/edge_symbol/gen_edge_symbol.py` | **added** | Stdlib-only generator: CSV → `omi.kicad_sym` + populated edge sheet; `--verify` re-parses and diffs against the CSV. |
| `tools/edge_symbol/README.md` | **added** | How to regenerate and validate. |
| `design/power/omi_v1_power/omi.kicad_sym` | **added** | Generated symbol library; one symbol `DDR4_UDIMM_288_Edge`, 288 pins. |
| `design/power/omi_v1_power/sym-lib-table` | **added** | Project symbol-lib table registering the library under nickname `omi`. |
| `design/power/omi_v1_power/udimm-edge-interface.kicad_sch` | **modified** | The single permitted edit: filled the empty sheet with one `J1` instance + 252 `global_label`s. |
| `build/p2/erc_after.json`, `build/p2/netlist_after.xml` | **added** | Measured post-placement evidence. |

No other existing file was touched: the four other sheets, the CSV, the `.kicad_pcb`, the
validation scripts, and the evidence tree are all unchanged.

## 3. Implementation Approach

**Inspection first (read-only fan-out).** Four parallel agents established: the CSV schema
(`pin,symbol,omi_net,group,notes`, 288 unique rows, NC predicate `omi_net == "NC"`); the
dominant label type (`global_label`, 452 vs 18 local, 0 hierarchical); a free connector ref
(`J1`); and the KiCad 9 `.kicad_sym` s-expression shape (confirmed from the installed stock
`Connector_Generic.kicad_sym`). The hierarchy facts (project `omi_v1_power`, root UUID, edge
sheet-node UUID) were read directly from the root sheet.

**Generation.** The generator reads the CSV (the single source of truth), validates it
(288 contiguous unique pins, no empty fields), and emits:

* a symbol library whose one symbol lays the 288 pins in two 144-pin columns on a 2.54 mm
  (100 mil) pitch — pins 1–144 exit left, 145–288 exit right;
* a populated edge sheet that embeds the symbol, places one `J1` instance, and drops a
  `global_label` (carrying the `omi_net`) exactly on every non-NC pin's connection point.

**Electrical typing.** `no_connect` when `omi_net == "NC"`; `passive` otherwise (power/ground
included — see Design Decisions). Histogram: **36 `no_connect`, 252 `passive`**.

**Determinism.** Every UUID is `uuid.uuid5(fixed_namespace, name)`; there are no timestamps
or RNG, so regeneration is byte-identical (verified by diff).

## 4. Mathematical / Geometric Details

Connectivity here is pure coordinate geometry, so it is worth stating precisely.

**Pin connection point.** In a KiCad symbol a pin `(at x y a)` has its *electrical
connection point* at exactly `(x, y)` in symbol-local coordinates, regardless of the stem
angle `a` (the stem is drawn from there toward the body over `length`). Verified against the
stock `Conn_01x01`: `(pin … (at -5.08 0 0) (length 3.81))` with a body rectangle whose left
edge is at `x = -1.27`, i.e. the stem runs `-5.08 → -1.27` and the connection point is the
left tip `(-5.08, 0)`.

**Symbol-local → sheet transform.** For a symbol placed at origin `(Ox, Oy)` with angle 0 and
no mirror, KiCad maps a local point `(lx, ly)` to the sheet as

```
sheet_x = Ox + lx
sheet_y = Oy − ly        (Y is flipped: symbol Y is up, sheet Y is down)
```

This was **verified against existing wiring** on the power sheet, not assumed: the placed
`Conn_01x05` at `(176.53, 100.33)` angle 0 has pin 5 at local `(-5.08, -5.08)`, which maps to
`(176.53 − 5.08, 100.33 − (−5.08)) = (171.45, 105.41)` — exactly the coordinate of the `GND`
power symbol it connects to. Pins 1–4 likewise land on their wires/labels.

**Placement.** `J1` is placed at `(Ox, Oy) = (152.4, 190.5)` (both multiples of 2.54). Pin
*i* in the left column sits at local `(−25.4, 180.34 − (i−1)·2.54)`; the right column mirrors
in `x` to `+25.4`. Applying the transform, every connection point lands on the 2.54 mm grid
with `sheet_y ∈ [10.16, 373.38]` (all positive, fits A2). A `global_label` is anchored on
each non-NC connection point, so the label attaches to the pin with no wire stub required —
confirmed by the netlist (below).

## 5. Design Decisions

* **`global_label`, not local/hierarchical.** It is the design's dominant label type (452
  occurrences) and merges nets across sheets by name, which is the whole point of exposing the
  connector's nets. 125 of the connector's nets duly merge with existing nodes.
* **Power pins `passive` by default.** Typing them `power_in` would make ERC demand a PWR_FLAG
  on every rail, injecting noise into an additive phase. `passive` keeps the connector
  ERC-neutral; `--power-type power_in` is offered for Phase 5, not baked in.
* **NC pins typed `no_connect` and left unlabelled.** This keeps all 36 ECC/CB/2nd-rank/reserved
  pins out of the ERC "unconnected" tally — they add **zero** violations, so the real connector
  is cleaner than the placeholder it will replace.
* **Library upgraded to a *copy* for validation.** `kicad-cli sym upgrade` writes to
  `build/p2/`, leaving the committed `omi.kicad_sym` byte-identical to generator output, so the
  "regenerate reproduces it" guarantee holds.
* **Bug found and fixed during validation.** The first sheet emission omitted the closing `)`
  of the `J1` `(symbol …)` node; KiCad silently dropped the malformed instance (0 J1 nodes in
  the netlist, 129 dangling labels). Adding the paren fixed it — a good argument for gating on
  the netlist, not just on "the file parses."

## 6. Verification

All gates run with KiCad 9.0.8 `kicad-cli` (format `20250114`).

* **Symbol:** `sym upgrade` clean (no changes needed); `sym export svg` renders; `--verify`
  reports **288/288 pins match the CSV exactly** (number + name + type); histogram
  `{no_connect: 36, passive: 252}`.
* **Sheet:** `sch erc` and `sch export netlist` both run; `sch export svg` renders the page.
* **Netlist connectivity:** `J1` present with all 288 pins; sampled pins land on the exact
  expected nets (79→A0, 2→GND, 59→VDD, 3→D0_DQ4, 142→VPP, 146→VREF, 141→SPD_SCL, 74→CK_t);
  125 nets merge `J1` with other components; the 36 NC pins sit on auto `unconnected-(J1-…)`
  nets (no error).
* **Reproducibility:** regenerating to a temp path and diffing yields byte-identical files.

**ERC delta: 131 → 135 (+4), fully attributable to the placement:**

| Type | Baseline | After | Δ |
| --- | --- | --- | --- |
| pin_not_connected | 108 | 108 | 0 |
| pin_not_driven | 16 | 16 | 0 |
| power_pin_not_driven | 5 | 5 | 0 |
| label_dangling | 2 | 2 | 0 |
| **global_label_dangling** | 0 | **3** | **+3** |
| **same_local_global_label** | 0 | **1** | **+1** |
| **Total** | **131** | **135** | **+4** |

The 3 new dangling globals are `ALERT_n`, `PARITY`, `VTT` — connector-side nets the CSV marks
as host-supplied / not-enabled-in-v1, with no counterpart elsewhere yet. The 1
same-local/global is `VREF` (root uses a *local* `VREF` label, the edge a *global* one). Both
are cross-sheet reconciliation items owned by **Phase 3**; per scope they are reported, not
fixed.

## 7. Related Docs

* `PHASE2_EDGE_SYMBOL_BRIEF.md` (working brief; intentionally untracked).
* `baseline/phase1/PHASE1_BASELINE.md` — the 131-violation baseline this delta is measured against.
* `tools/edge_symbol/README.md` — regeneration and validation commands.

### Handoff to Phase 3
* Replace the placeholder host connectors with wiring to `J1`.
* Reconcile the connector-only nets (`ALERT_n`, `PARITY`, `VTT`) and the `VREF` local/global
  clash (the ~4% name mismatches).
* Add root hierarchy / sheet-pins if cross-sheet structure is formalised.
* Resolve the pre-existing "schematic has annotation errors" warning.
* ERC clean-up to zero/justified is Phase 5.
