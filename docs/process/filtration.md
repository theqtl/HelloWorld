# Filtration & UF/DF

Purification is filtration-led. This page holds the clearance matrix and the UF/DF design basis;
the [filtration finding](../findings/filtration.md) holds the argument for whether the train closes.

## Clearance matrix

What each mode can and cannot clear, with the quantitative basis. Modes: **UF/DF** (tight
ultrafiltration + diafiltration), **NF** (nanofiltration 200–1000 Da), **Q/S** (charged membrane
adsorber), **0.2 µm / depth**.

| Impurity | UF/DF | NF | Q/S adsorber | 0.2 µm / depth |
|---|---|---|---|---|
| Block-internal n-1 (~330 Da, ~5%) | No — needs ≥~10× MW ratio | No (both retained) | No (~5% charge diff) | No |
| Unreacted blocks / partials (whole block) | Partial; very short → yes | Short blocks/mononucleotides → yes | Marginal | No |
| Ligase protein (tens kDa) | No in solution; **immobilise** → yes | No | Unreliable (polyanion competes) | Only if precipitated |
| Splint oligo (same chemistry) | No | No | No | No |
| Adenylylated dead-end (~329 Da) | No | No | No | No |
| ATP / AMP / PPi / Mg²⁺ / salts (<1 kDa) | **Yes** (diafiltration) | Yes | n/a | No |
| Endotoxin (LPS ~10³ kDa micelles) | Co-retained (counter-productive) | No | Yes in protein feeds; unproven for oligo | No |
| Aggregates / particulates / bioburden | Retained with product | No | No | **Yes** |

Source basis: [SRC-ZYDNEY-2024](../registers/sources.md), [SRC-BPT-TFF](../registers/sources.md),
[SRC-PMC12226154](../registers/sources.md), [SRC-PMC7415879](../registers/sources.md). Most flux
data is protein/pDNA/mRNA surrogate — see evidence-quality note below.

## UF/DF design basis

- **Membrane cut-off** for a ~7 kDa strand / ~14–17 kDa duplex: tested MWCOs 1/3/10/30 kDa, with
  30 kDa the upper limit for sufficient retention of an siRNA duplex; 1–3 kDa for a single strand
  (<span class="prov-fact">fact</span> for the duplex; <span class="prov-inference">inference</span>
  for the strand; [SRC-ZYDNEY-2024](../registers/sources.md)).
- **Concentration:** charged membranes reached >190 g/L siRNA vs <60 g/L unmodified; oligo UF/DF
  routinely 40–100 mg/mL; patent retentate 150–225 mg/mL (<span class="prov-fact">fact</span>;
  [SRC-ZYDNEY-2024](../registers/sources.md), [SRC-PMC7415879](../registers/sources.md),
  [SRC-WO2023164631](../registers/sources.md)).
- **Diafiltration:** `EQ-DIAF`; 7 diavolumes → 99.9% small-solute clearance at σ≈1. Sets the
  dominant clean-water and aqueous-waste volumes (`P-DF-DIAVOL`, Q-020).
- **Flux / sizing:** `EQ-FLUX`; area \(A = V_\text{perm}/(J_\text{avg}t)\). Flux figures available
  are protein/pDNA/mRNA (25–60 / 10–30 LMH; ~80% RNA recovery) — oligo-specific flux is a **gap**.
- **Scale-up invariants:** constant flux, wall shear, loading (L/m²), diavolumes, TMP.
- **Yield:** TFF loss <10% if hold-up is flushed (protein surrogate).

## Final matrix (hard constraint)

The final diafiltration must exchange into a **spray-dry-compatible matrix** (excipient + minimal
or volatile salts). Otherwise evaporation concentrates Tris/Mg/NaCl into the powder (risk R-005).
See [buffers](../registers/buffers.md) `BUF-FINAL`.

!!! warning "Evidence quality"
    The only oligo-specific UF source is abstract-only; separation-limit conclusions (n-1, splint,
    ligase) rest on established membrane first principles plus the ≥10× MW-ratio rule. Endotoxin
    adsorber data is protein-feed only and the top experimental gap (R-007).
