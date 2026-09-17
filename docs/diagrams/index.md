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

!!! note "Not yet drawn"
    A stream-numbered process flow diagram (PFD) with instrument tags and equipment layout is
    Tier-2/Tier-3. This BFD is the hand-off skeleton.
