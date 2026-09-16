# Block preparation (incoming)

Block synthesis is solvent-intensive and is a **supplier** operation, outside this facility's
solvent-free boundary. It is captured here as incoming-material specifications, because block
purity sets the purity floor the downstream train cannot beat.

## Achievable block purity

- Modified gapmer fragments: **90–95% full-length, 62–76% yield, at 0.3–3 kg/batch**; blocks
  assembled to 18- and 34-mers with an impurity profile similar to standard synthesis, without
  chromatography on the assembled product (<span class="prov-fact">fact</span>;
  [SRC-ZHOU-2022](../registers/sources.md)).
- Full-length falls with length as \(y^n\) (`EQ-SPOS`): a short block carries far more full-length
  at the same coupling yield than a 21-mer does. This is why blocks help.

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
protecting groups, and desulfurization (P=O) level. Numeric targets depend on the DS spec (Q-033)
and are a gap (Q-011). Approved-siRNA DS numeric limits are redacted; public guidance is ≥80% by
LC with a 1% single-impurity characterisation threshold.
