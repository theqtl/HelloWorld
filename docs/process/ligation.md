# Enzymatic ligation

Chemically synthesised blocks are joined into the siRNA strand(s) by enzymatic ligation. This is
a fixed decision; the work here is how to make it robust.

## Enzyme and chemistry

- The viable class is **double-stranded RNA (nick-sealing) ligases** — T4 RNA ligase 2 family and
  engineered variants (<span class="prov-fact">fact</span>, bench→1 L, fully modified siRNA;
  [SRC-ALMAC-2023](../registers/sources.md); vendor [SRC-CODEXIS](../registers/sources.md)).
- Plain **T4 DNA ligase fails**: it gives essentially all adenylylated dead-end product on
  RNA-splinted substrate and cannot ligate fully 2'-OMe segments
  (<span class="prov-fact">fact</span>; [SRC-USPTO-10640812](../registers/sources.md),
  [SRC-PBCV1-2014](../registers/sources.md)).
- All ATP-dependent ligases require **5'-phosphate + 3'-OH** at the junction. The 5'-phosphate is
  installed chemically (in-line phosphoramidite reagent, ~quantitative, DMT-trackable) or
  enzymatically (T4 PNK; sequence/modification-sensitive; Almac ran PNK one-pot at 5 mM)
  (<span class="prov-fact">fact</span>; [SRC-ALMAC-2023](../registers/sources.md)).

## Annealing is interleaved (Q-001)

dsRNA ligases need a duplex nick, so the complementary strand (or an overlap) templates each
ligation and the duplex is **co-assembled**, not built as free single strands annealed at the end
(<span class="prov-fact">fact</span>/<span class="prov-inference">inference</span>;
[SRC-ALMAC-2023](../registers/sources.md), [SRC-HONGENE](../registers/sources.md)). Almac
demonstrated ligation with overlaps as short as 3 bp using a directional "3-2-3-2" assembly.

## Conditions (documented set, Almac, fully modified siRNA, bench→1 L)

| Parameter | Value | Note |
|---|---|---|
| Anneal | 50 mM Tris-HCl pH 7.5, 100 mM KCl, 10 mM MgCl₂, 65 °C, 15 min | [SRC-ALMAC-2023](../registers/sources.md) |
| Ligation | + 1 mM DTT, 25 °C, 400 rpm, 1–20 h | same |
| Product conc | ~1 mM duplex (1 L jacketed) | largest real public scale |
| Blockmer conc | up to 10 mM (slow/incomplete) | same |
| ATP conc | **gap** (in SI, not accessed) | Q-010 reading list |

Vendor claims (not peer-reviewed): >95% conversion, substrate up to 100 g/L, 30 g/L titer
([SRC-CODEXIS](../registers/sources.md)). Peer-reviewed conversion for a modified oligo is
40–80% (abstract only). See conversion assumption `P-LIG-CONV` and Q-010.

## Side reactions to control at the reaction

Adenylylated dead-end (+AMP), hairpins, concatemers, and 3'-terminal-nucleotide loss are observed
for modified siRNA (<span class="prov-fact">fact</span>; [SRC-ALMAC-2023](../registers/sources.md)).
Controlled by directional assembly, keeping ≤3 blockmers present at once, and tuning temperature/time.
The adenylylated species differs from product by ~one residue and **cannot be removed downstream by
filtration** (risk R-010) — it must be suppressed at the reaction (enzyme choice, controlled ATP).

## Enzyme removal — the linchpin

Soluble ligase cannot be cleared from the smaller strand by size ultrafiltration. **Immobilised or
solid-phase ligase**, removed by filtration/centrifugation, is the route to keep the train
filtration-led (finding: [filtration](../findings/filtration.md) §4). Quantitative clearance data
is a gap (Q-032, risk R-002); a chromatographic fallback is retained.

## GMP sourcing

GMP-grade T4 ligases are commercially listed; the high-performance engineered dsRNA ligases and
PNKs are proprietary to the platform owners. Recombinant *E. coli* expression is animal-free;
endotoxin-controlled strains exist (<span class="prov-fact">fact</span>). Residual-enzyme
acceptance criteria specific to GMP siRNA ligation are a gap.
