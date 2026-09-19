# Filtration & UF/DF

Purification is filtration-led. This page holds the clearance matrix and the UF/DF design basis;
the [filtration finding](../findings/filtration.md) holds the argument for whether the train closes.

## Clearance matrix

What each mode can and cannot clear, with the quantitative basis. Modes: **UF/DF** (tight
ultrafiltration + diafiltration), **NF** (nanofiltration, conventionally rated in the few-hundred to
~1000 Da range; [SRC-MWCO-REVIEW-2024](../registers/sources.md)), **Q/S** (charged membrane
adsorber), **0.2 µm / depth**. Sizes below are from `P-MW-STRAND`, `P-DMW-N1` and `P-MW-DUPLEX`.

| Impurity | UF/DF | NF | Q/S adsorber | 0.2 µm / depth |
|---|---|---|---|---|
| Block-internal n-1 (`P-DMW-N1`, ~330 Da, ~5%) | No — MW ratio ~1.05, far below the ~5× floor (`EQ-UFRULE`) | No (both retained) | No (~5% charge diff) | No |
| Unreacted blocks / partials (whole block) | Partial; very short → yes | Short blocks/mononucleotides → yes | Marginal | No |
| Ligase protein (tens kDa) | No in solution; **immobilise** → yes | No | Unreliable (polyanion competes) | Only if precipitated |
| Splint oligo (same chemistry) | No | No | No | No |
| Adenylylated dead-end (donor + ~329 Da; R-010) | No | No | No | No |
| ATP / AMP / PPi / monovalent salts (<1 kDa) | **Yes** (diafiltration) | Yes | n/a | No |
| Divalent cations (Mg²⁺ / Ca²⁺) | **Not reliably** — bind the polyanion, may not pass (R-014) | Partial | n/a | No |
| Endotoxin (LPS ~10³ kDa micelles) | Co-retained (counter-productive) | No | Yes in protein feeds; unproven for oligo | No |
| Aggregates / particulates / bioburden | Retained with product | No | No | **Yes** |

Source basis: [SRC-ZYDNEY-2024](../registers/sources.md), [SRC-GRONKE-2023](../registers/sources.md),
[SRC-PMC12226154](../registers/sources.md), [SRC-PMC7415879](../registers/sources.md). Most flux
data is protein/pDNA/mRNA surrogate — see evidence-quality note below. A polyanion will not diafilter
out cationic impurities including the ligation buffer's magnesium
(<span class="prov-fact">fact</span>, single-strand antisense;
[SRC-GRONKE-2023](../registers/sources.md), R-014).

## UF/DF design basis

- **Membrane cut-off** for a ~7 kDa strand / ~14–17 kDa duplex: the cut-off sits **well below** the
  product mass. An oligonucleotide should be at least **twice** the membrane cut-off for robust
  retention (<span class="prov-fact">fact</span>; [SRC-GRONKE-2023](../registers/sources.md)), the
  vendor rule is a cut-off **3–6× lower** than the molecule
  (<span class="prov-fact">fact</span>; [SRC-SCHWARTZ-BPI-2003](../registers/sources.md),
  [SRC-PALL-TFF](../registers/sources.md)), and the only siRNA optimisation study ran at **10 kDa**
  (<span class="prov-fact">fact</span>; [SRC-ZYDNEY-2025](../registers/sources.md)). A previously
  asserted **"30 kDa upper limit" is struck** — it is unsupported and points the wrong way; the
  Zydney siRNA study's own cut-off enumeration is still unreachable, so Q-035 stays open on that point.
  The duplex molecular weight is 17.15 kDa by SEC-MALS (<span class="prov-fact">fact</span>;
  [SRC-ZYDNEY-2024](../registers/sources.md)); 1–3 kDa for a single strand is our
  <span class="prov-inference">inference</span>.
- **Concentration:** surface-modified negatively charged membranes raised the maximum achievable
  siRNA concentration **from 52 to >180 mg/mL** (<span class="prov-fact">fact</span>;
  [SRC-ZYDNEY-2024](../registers/sources.md)), and **~193 g/L** in the ligand-density follow-up on a
  10 kDa membrane (<span class="prov-fact">fact</span>, bench; [SRC-ZYDNEY-2025](../registers/sources.md)).
  A single-strand antisense oligo reached 200 mg/mL at ≥95% yield and <15 cP on a 3 kDa membrane
  (<span class="prov-fact">fact</span>, single-strand antisense;
  [SRC-GRONKE-2023](../registers/sources.md)), so for our duplex **viscosity is unlikely to be the
  binding constraint** (<span class="prov-inference">inference</span>); oligo UF/DF routinely reaches 40–100 mg/mL
  (<span class="prov-fact">fact</span>; [SRC-PMC7415879](../registers/sources.md)). Whether osmotic
  pressure or fouling sets our ceiling is open (Q-041). The high-concentration patent claims a final
  composition "greater than about 150 mg/mL", with embodiments described up to 250–400 mg/mL — an
  open-ended lower bound, not a closed band (<span class="prov-fact">fact</span>;
  [SRC-WO2023164631](../registers/sources.md)).
- **Diafiltration:** `EQ-DIAF`; 7 diavolumes → 99.9% small-solute clearance at σ≈1. Sets the
  dominant clean-water and aqueous-waste volumes (`P-DF-DIAVOL`, Q-020).
- **Flux / sizing:** `EQ-FLUX`; area \(A = V_\text{perm}/(J_\text{avg}t)\). The flux figures
  available are protein (25–60 LMH) and plasmid DNA (10–30 LMH) surrogates from a secondary source
  whose provenance is weak ([SRC-BPT-TFF](../registers/sources.md)); they are not messenger-RNA or
  oligonucleotide figures. Oligo-specific flux, and any RNA recovery figure, are a **gap** (Q-036).
- **Scale-up invariants:** constant flux, wall shear, loading (L/m²), diavolumes, TMP.
- **Yield is an equation, not a "<10%" rule** (`EQ-UFYIELD`). Membrane-passage loss is exponential in
  retention and in \((\ln \mathrm{VCF} + N)\) — a tenfold swing (9.5% at R=0.99, 1.0% at R=0.999) from
  one membrane choice (<span class="prov-fact">fact</span>; [SRC-MILLIPORE-TFF](../registers/sources.md)).
  The **dominant** loss at small batch is unrecoverable **hold-up** in tubing and filters: 30–40% of a
  nucleic acid can be left behind (<span class="prov-fact">fact</span>, mRNA;
  [SRC-NOURAFKAN-2024](../registers/sources.md)), a term the old flat yield lacked. Account for
  retentate, filtrate **and** hold-up as a mass balance, not yield alone (Q-036, R-011).

## Final matrix (hard constraint)

The final diafiltration must exchange into a **spray-dry-compatible matrix** (excipient + minimal
or volatile salts). Otherwise evaporation concentrates Tris/Mg/NaCl into the powder (risk R-005).
See [buffers](../registers/buffers.md) `BUF-FINAL`.

!!! warning "Evidence quality"
    The only oligo-specific UF source is abstract-only; separation-limit conclusions (n-1, splint,
    ligase) rest on established membrane first principles plus the ≥5× MW-ratio rule. Endotoxin
    adsorber data is protein-feed only and the top experimental gap (R-007). And note the honest
    external check on the whole premise: both named commercial ligation routes still end in **HPLC
    purification of the siRNA itself** — filtration replaces *fragment* chromatography, not
    final-product chromatography ([SRC-HONGENE-BROCHURE-2025](../registers/sources.md); see the
    [filtration finding](../findings/filtration.md) §7).
