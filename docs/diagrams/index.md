# Diagrams

## Block flow diagram (BFD)

Vector flowsheet. Stream numbers (S01…S12) tie to the [stream register](../registers/streams.md)
and the [mass balance](../balance/results.md). Product path in teal, buffer/utility in purple
(dashed), waste in red (dashed).

<div markdown="0">
--8<-- "diagrams/bfd.svg"
</div>

*Teal = product path · purple dashed = buffer/utility · red dashed = waste. The diagram above is
included from `bfd.svg`, the same file linked below, so the rendered and downloadable versions
cannot diverge.*

[Download the SVG](bfd.svg)

## Reading the flowsheet

- **U00 Buffer prep** feeds the ligation buffer (S03) and the diafiltration/final-matrix buffer
  (S06). The final diafiltration must exchange into a spray-dry-compatible matrix (risk R-005).
- **U01 Ligation** receives blocks (S01/S02) and produces the reaction mass (S04): full-length
  strand plus impurities.
- **U02 Clarify / enzyme separation** removes particulates and, with an immobilised ligase, the
  enzyme (see [filtration finding](../findings/filtration.md) §4).
- **U03 UF/DF** desalts, exchanges buffer, and concentrates (S08); permeate S07 is the largest
  aqueous waste.
- **U04 Evaporation** concentrates further (condensate S09); duty depends on how far UF got.
- **U05 Spray dry** produces the DS powder (S12); exhaust S11 carries humid gas and fines.

## Process flow diagrams

Each block above is drawn again, one unit operation at a time, with the instruments the register
carries for it: **[process flow diagrams](pfd.md)**. The bubbles distinguish a closed control loop
from a reading that exists only because a sample was withdrawn, and that distinction is computed
from the register rather than asserted.

!!! note "What the PFDs still do not carry"
    **Equipment layout and a plot plan** are not drawn — those are a facility exercise and a
    function of annual demand (Q-002). Neither is a **stream table** on the drawing itself: the
    quantities are computed and already published scenario by scenario in the
    [mass & energy balance](../balance/results.md), so duplicating them onto an SVG would create a
    second copy to drift. And none of this is a **P&ID** — no piping, no valve specification, no
    line numbering. The symbol set is this project's own, because no standard it has read pins one
    down (Q-054).
