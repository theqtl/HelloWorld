# Block preparation (incoming)

Block synthesis is solvent-intensive and is a **supplier** operation, outside this facility's
solvent-free boundary. It is captured here as incoming-material specifications, because block
purity sets the purity floor the downstream train cannot beat.

## Achievable block purity

- **Measured, chromatography-free block purity is 89–96%** for 4–5 nucleotide modified blocks at
  145–258 g (e.g. a TTACC 5-mer at 93.6%, a UTTC 4-mer at 95.6%; <span class="prov-fact">fact</span>;
  [SRC-WO2020227618](../registers/sources.md)). The summary range often quoted, 90–95% full-length at
  62–76% yield and 0.3–3 kg/batch, is for the same Biogen programme
  ([SRC-ZHOU-2022](../registers/sources.md), abstract, corroborated by
  [SRC-NAR-2025](../registers/sources.md)). **Chemistry caveat:** these are MOE/DNA gapmer blocks
  carrying a 5'-DMTr group that is itself a purity handle a 5'-phosphate block does not have; a 6-mer
  2'-OMe PS oligomer measured only 81% ([SRC-KELLY-OPRD-2025](../registers/sources.md)), so 95%-class
  blocks are not assured in our 2'-OMe/2'-F/PS chemistry (Q-011).
- **"Assembled without chromatography" is chromatography-free *assembly*, not a chromatography-free
  *drug substance*.** The kilogram-scale paper's own abstract says purities suitable for clinical use
  are reached "after applying standard full-length product purification process", and describes
  eliminating that chromatography only as a demonstrated **potential**
  (<span class="prov-fact">fact</span>; [SRC-ZHOU-2022](../registers/sources.md)). Do not cite it for a
  chromatography-free product.
- **What one preparative chromatography step adds:** a crude block at 81–87% rises to 98–99% at 90–98%
  recovery after a single reversed-phase HPLC pass (<span class="prov-fact">fact</span>;
  [SRC-WO2020227618](../registers/sources.md)). That is the selectivity a filtration-only train forgoes
  (see the [filtration finding](../findings/filtration.md)).
- Full-length falls with length as \(y^n\) (`EQ-SPOS`): a short block carries far more full-length
  at the same coupling yield than a 21-mer does. This is why blocks help. A block route that omits
  capping, though, converts coupling failures into block-internal deletions rather than truncations —
  the harder class (risk R-018; [SRC-IQ-SUSTAIN-2021](../registers/sources.md)).

## Why single-nucleotide control belongs here

A single-nucleotide deletion is a much larger fractional difference on a short block (1 in ~7)
than on the full strand (1 in ~21), so anion-exchange or RP-HPLC resolves it at the block stage
(<span class="prov-fact">fact</span>, principle; [SRC-ATDBIO-PUR](../registers/sources.md);
RP-HPLC useful <40–50 nt, IEX/AX 5–100 nt). Doing this chromatography at the supplier keeps the
DS facility filtration-led. See the [filtration finding](../findings/filtration.md).

## Purity propagation

Isolated full-length purity is floored at \(\prod_i f_i\) (`EQ-PURITY`); block-internal n-1
propagates and cannot be removed downstream, while unreacted/partial products differ by a whole
block and are filterable. Empirically, ~5% of fragment-internal impurity is carried into the
ligated product (<span class="prov-fact">fact</span>; [SRC-NATCOMM-2024](../registers/sources.md)).

## 5'-phosphate

Installed chemically (in-line, ~quantitative, DMT-trackable) or enzymatically (T4 PNK). If done at
the supplier, blocks arrive phosphorylated; if enzymatic in-house, it adds an enzyme-removal burden.

## Specifications to place on incoming blocks (to be set)

Full-length %, single-impurity limit, n-1/n+1 limits, 5'-phosphorylation level, residual
protecting groups, and desulfurization (P=O) level. Numeric targets depend on the DS spec, which is
**not a fixed public number**: it is derived from the applicant's own toxicology batch capability and
tightens as batches accumulate (Q-033; [SRC-FDA-OXLUMO-CHEMR](../registers/sources.md),
[SRC-FDA-INCLISIRAN-CHEMR](../registers/sources.md)), so the block targets follow the demonstrated
capability rather than a threshold (Q-011). Approved-siRNA DS numeric limits are redacted in every
jurisdiction. The often-cited "≥80% full-length by LC with a 1% threshold" is an **FDA recommendation
for guide RNA in genome editing**, not an siRNA drug-substance specification, and must not be ported
as one (<span class="prov-fact">fact</span>, scope-limited; [SRC-FDA-CBER-2024](../registers/sources.md));
oligonucleotides are outside ICH Q3A/Q6A scope entirely ([SRC-ICH-Q3A-SCOPE](../registers/sources.md)).
