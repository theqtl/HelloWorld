"""Generate the block-flow diagram docs/diagrams/bfd.svg from data/streams.csv.

The flowsheet is DERIVED from the stream edge list (data/streams.csv) and the equipment
register (data/equipment.csv), so it cannot silently drift from the data - the defect that
lost the product-outlet arrow in Tier 1.

Layout is deterministic. Process units are ranked by longest path along the PRODUCT streams,
which fixes the x column of the product spine. Every OTHER node touched by a stream then
inherits a column from its ranked neighbours, so a utility or cleaning stream can be added to
the data without the generator failing. Rows are assigned by role: the product spine in the
middle, buffer/utility feeds in a top bus, auxiliary units (anything connected but off the
product path, e.g. a CIP skid) in a lower row, and streams to the WASTE sink as bottom stubs.

The same data always renders byte-identical SVG, which a test enforces against the committed
file. `render()` returns the SVG string; gen/build.py writes it. Do not hand-edit bfd.svg -
edit data/streams.csv (and data/equipment.csv) and run `python -m gen.build`.
"""
from .dataio import load_rows

SENTINELS = {"SUPPLY", "WASTE", "DS-STORE"}

# Layout geometry. Integer coordinates keep the rendered output byte-stable.
MARGIN_X = 20
PITCH = 165
BOX_W, BOX_H = 120, 60
Y_MAIN = 180            # top of the process-row boxes
CY = Y_MAIN + BOX_H // 2
Y_BUF, BUF_H, BUF_W = 30, 46, 140
Y_AUX = 330             # auxiliary row: connected units off the product path
BUS_Y = 150             # horizontal bus that buffer feeds run along
WASTE_Y = 300           # where waste stubs end
VIEW_W, VIEW_H = 1160, 460

# Short display labels; fall back to the equipment name / id for anything unmapped.
UNIT_LABELS = {
    "SUPPLY": "Blocks",
    "U00-BUF": "Buffer prep",
    "U01-LIG": "Ligation",
    "U02-CF": "Clarify / sep",
    "U03-UFDF": "UF / DF",
    "U04-EVAP": "Evaporation",
    "U05-SD": "Spray dry",
    "DS-STORE": "DS powder",
}
UNIT_SUBLABELS = {
    "SUPPLY": "received, 5'-P",
    "DS-STORE": "product",
}


def _rank_product_nodes(streams):
    """Longest-path rank of each node along PRODUCT streams -> its x column index.

    Raises on a cycle rather than returning garbage ranks: the layout needs a DAG, and a
    recycle stream (R-013 requires evaporator recirculation) is a foreseeable data change.
    """
    edges = [(r["from_unit"], r["to_unit"]) for r in streams
             if r["stream_class"] == "product"]
    nodes = {n for e in edges for n in e}
    rank = {n: 0 for n in nodes}
    for _ in range(len(nodes) + 1):      # a DAG settles in <= |nodes| passes
        changed = False
        for f, t in edges:
            if rank[t] < rank[f] + 1:
                rank[t] = rank[f] + 1
                changed = True
        if not changed:
            return rank
    raise ValueError(
        "product streams contain a cycle, so the flowsheet has no longest-path layout; "
        "model a recycle as a separate stream class or split the unit"
    )


def _columns(streams, rank):
    """A column index for EVERY node touched by a stream, not just the product-ranked ones.

    Product ranks are authoritative; anything else (a buffer skid, a CIP system, a utility
    sink) inherits a column from its nearest ranked neighbour. Without this an added
    utility stream raised KeyError and took down the whole build.
    """
    col = dict(rank)
    touched = {r[k] for r in streams for k in ("from_unit", "to_unit")}
    for _ in range(len(touched) + 1):
        changed = False
        for r in streams:
            f, t = r["from_unit"], r["to_unit"]
            if f in col and t not in col:
                col[t] = col[f] + 1
                changed = True
            elif t in col and f not in col:
                col[f] = max(col[t] - 1, 0)
                changed = True
        if not changed:
            break
    unplaced = sorted(touched - set(col))
    if unplaced:
        raise ValueError(
            "stream endpoint(s) with no path to the product spine, so no column can be "
            f"derived: {unplaced}; connect them or give them a product stream"
        )
    return col


def _x(col):
    return MARGIN_X + col * PITCH


def _label(unit, equip):
    main = UNIT_LABELS.get(unit)
    if main is None:
        main = (equip.get(unit, {}).get("name") or unit)[:16]
    if unit in UNIT_SUBLABELS:
        sub = UNIT_SUBLABELS[unit]
    elif unit in equip:
        sub = unit.split("-")[0]
    else:
        sub = ""
    return main, sub


def _box(out, unit, x, y, w, h, equip, util=False):
    cx = x + w // 2
    main, sub = _label(unit, equip)
    cls = "util" if util else "box"
    dy1, dy2 = (20, 36) if util else (27, 43)
    out.append(f'  <rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>')
    out.append(f'  <text class="lbl" x="{cx}" y="{y + dy1}" text-anchor="middle">{main}</text>')
    if sub:
        out.append(f'  <text class="sub" x="{cx}" y="{y + dy2}" text-anchor="middle">{sub}</text>')


def render():
    streams = load_rows("streams")
    equip = {r["equip_id"]: r for r in load_rows("equipment")}
    rank = _rank_product_nodes(streams)
    col = _columns(streams, rank)

    # Buffer/utility node: equipment whose every outgoing stream is a buffer.
    out_classes = {}
    for r in streams:
        out_classes.setdefault(r["from_unit"], set()).add(r["stream_class"])
    buffer_nodes = sorted(
        n for n, cls in out_classes.items() if n in equip and cls == {"buffer"}
    )
    buf_col = {}
    for b in buffer_nodes:
        targets = [col.get(r["to_unit"], 0) for r in streams if r["from_unit"] == b]
        buf_col[b] = min(targets) if targets else 0

    # Auxiliary nodes: connected, but off the product path and not a buffer feed. WASTE is a
    # sink drawn as stubs, never as a box.
    touched = {r[k] for r in streams for k in ("from_unit", "to_unit")}
    aux_nodes = sorted(touched - set(rank) - set(buffer_nodes) - {"WASTE"})

    # Row (box top y) and width per drawn node, so edge routing is role-agnostic.
    geom = {}
    for n in rank:
        geom[n] = (_x(col[n]), Y_MAIN, BOX_W, BOX_H)
    for b in buffer_nodes:
        bx = _x(buf_col[b]) + BOX_W // 2 - BUF_W // 2
        geom[b] = (bx, Y_BUF, BUF_W, BUF_H)
    for a in aux_nodes:
        geom[a] = (_x(col[a]), Y_AUX, BOX_W, BOX_H)

    out = []
    out.append('<!-- GENERATED by gen/flowsheet.py from data/streams.csv - do not edit '
               'by hand. Edit data/streams.csv and run python -m gen.build. -->')
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VIEW_W} {VIEW_H}" '
               'class="bfd-svg" role="img" '
               'aria-label="Block flow diagram of the siRNA drug-substance process">')
    out.append('  <style>')
    out.append('    .box { fill: none; stroke: #00897b; stroke-width: 2; rx: 6; }')
    out.append('    .util { fill: none; stroke: #8e24aa; stroke-width: 2; stroke-dasharray: 4 3; }')
    out.append('    .lbl { fill: currentColor; font: 600 13px sans-serif; }')
    out.append('    .sub { fill: currentColor; font: 400 10px sans-serif; opacity: 0.8; }')
    out.append('    .sid { fill: #00695c; font: 700 10px sans-serif; }')
    out.append('    .wid { fill: #c62828; font: 700 10px sans-serif; }')
    out.append('    .flow { stroke: currentColor; stroke-width: 1.8; marker-end: url(#arrow); fill: none; }')
    out.append('    .wflow { stroke: #c62828; stroke-width: 1.4; marker-end: url(#warr); fill: none; }')
    out.append('    .uflow { stroke: #8e24aa; stroke-width: 1.4; stroke-dasharray: 4 3; marker-end: url(#uarr); fill: none; }')
    out.append('  </style>')
    out.append('  <defs>')
    out.append('    <marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="currentColor"/></marker>')
    out.append('    <marker id="warr" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#c62828"/></marker>')
    out.append('    <marker id="uarr" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#8e24aa"/></marker>')
    out.append('  </defs>')

    # Process-row boxes (product-ranked nodes), left to right.
    for n in sorted(rank, key=lambda n: (rank[n], n)):
        x, y, w, h = geom[n]
        _box(out, n, x, y, w, h, equip)

    # Buffer/utility boxes (top row).
    for b in buffer_nodes:
        x, y, w, h = geom[b]
        _box(out, b, x, y, w, h, equip, util=True)

    # Auxiliary boxes (lower row): connected units off the product path.
    for a in aux_nodes:
        x, y, w, h = geom[a]
        _box(out, a, x, y, w, h, equip, util=True)

    # Edges, grouped by (from, to) so parallel streams share one arrow (e.g. S01/S02).
    order, grouped = [], {}
    for r in streams:
        k = (r["from_unit"], r["to_unit"])
        if k not in grouped:
            grouped[k] = []
            order.append(k)
        grouped[k].append(r)

    for (f, t) in order:
        rows = grouped[(f, t)]
        sid = "/".join(r["stream_id"] for r in rows)
        cls = rows[0]["stream_class"]
        if t == "WASTE":
            fx, fy, fw, fh = geom[f]
            scx = fx + fw // 2
            name = rows[0]["name"].replace("(waste)", "").strip()
            tag = name.split()[-1] if name.split() else ""
            out.append(f'  <path class="wflow" d="M{scx},{fy + fh} V{WASTE_Y}"/>')
            out.append(f'  <text class="wid" x="{scx + 6}" y="{(fy + fh + WASTE_Y) // 2}">{sid} {tag}</text>')
        elif cls == "buffer":
            bcx = _x(buf_col.get(f, 0)) + BOX_W // 2
            tcx = _x(col.get(t, 0)) + BOX_W // 2
            out.append(f'  <path class="uflow" d="M{bcx},{Y_BUF + BUF_H} V{BUS_Y} H{tcx} V{Y_MAIN}"/>')
            if tcx == bcx:
                out.append(f'  <text class="sid" x="{bcx + 6}" y="{(Y_BUF + BUF_H + BUS_Y) // 2}">{sid}</text>')
            else:
                out.append(f'  <text class="sid" x="{(bcx + tcx) // 2}" y="{BUS_Y - 4}">{sid}</text>')
        else:
            fx, fy, fw, fh = geom[f]
            tx, ty, tw, th = geom[t]
            if fy == ty:
                # same row: straight horizontal connector between the two boxes
                ax, bx = fx + fw, tx
                out.append(f'  <path class="flow" d="M{ax},{fy + fh // 2} L{bx},{ty + th // 2}"/>')
                out.append(f'  <text class="sid" x="{ax + 6}" y="{fy + fh // 2 - 7}">{sid}</text>')
            else:
                # different rows: drop out of the source, run across, then into the target
                scx, tcx = fx + fw // 2, tx + tw // 2
                sy = fy + fh if ty > fy else fy
                mid = (sy + (ty if ty > fy else ty + th)) // 2
                out.append(f'  <path class="flow" d="M{scx},{sy} V{mid} H{tcx} V{ty if ty > fy else ty + th}"/>')
                out.append(f'  <text class="sid" x="{(scx + tcx) // 2}" y="{mid - 4}">{sid}</text>')

    out.append(f'  <text class="sub" x="{MARGIN_X}" y="450">Teal = product path '
               '&#183; purple dashed = buffer/utility &#183; red dashed = waste. '
               'Stream IDs tie to the stream register and the mass balance.</text>')
    out.append('</svg>')
    return "\n".join(out) + "\n"
