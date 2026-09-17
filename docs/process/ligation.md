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
  enzymatically by a polynucleotide kinase; Almac screened a kinase panel and ran a one-pot
  phosphorylation at 5 mM blockmer (<span class="prov-fact">fact</span>;
  [SRC-ALMAC-2023](../registers/sources.md)). The paper uses kinase cell-free extracts rather than a
  named T4 enzyme, so the specific enzyme is not pinned down here.

## Annealing is interleaved (Q-001)

dsRNA ligases need a duplex nick, so the complementary strand (or an overlap) templates each
ligation and the duplex is **co-assembled**, not built as free single strands annealed at the end
(<span class="prov-fact">fact</span>/<span class="prov-inference">inference</span>;
[SRC-ALMAC-2023](../registers/sources.md), [SRC-HONGENE](../registers/sources.md)). Almac used a directional "3-2-3-2" assembly, each stage starting with three blockmers and ending
with two partially complementary strands whose overhang templates the next annealing step. (An
often-quoted "3 bp overlap" could not be found in the paper or its SI and is **not** carried here.)

## Conditions (documented set, Almac, fully modified siRNA, bench→1 L)

| Parameter | Value | Note |
|---|---|---|
| Anneal | 50 mM Tris-HCl pH 7.5, 100 mM KCl, 10 mM MgCl₂, 65 °C, 15 min | [SRC-ALMAC-2023](../registers/sources.md) |
| Ligation | + 1 mM DTT, 25 °C, 400 rpm, 1–20 h | same |
| Product conc | ~1 mM duplex (1 L jacketed) | largest real public scale |
| Blockmer conc | up to 10 mM, but slow and **did not go to completion** | flagged by the authors as an optimisation target |
| ATP conc | 2 mM | from the SI, now retrieved ([SRC-ALMAC-2023](../registers/sources.md)) |
| Ligase loading | RNA ligase cell-free extract 1 mg/mL | SI Table S1 |

Vendor claims (not peer-reviewed): >95% conversion, substrate loads up to 100 g/L, and >98%
post-purification purity ([SRC-CODEXIS](../registers/sources.md)). A product titre for the vendor
route is a **gap** — no titre figure appears in the vendor material (Q-034). Peer-reviewed conversion
figures for *modified* oligos are not established either: the 82–96% range often quoted from
[SRC-NATCOMM-2024](../registers/sources.md) is that paper's initial ligase screen on an **unmodified**
shortmer, and its 5'-monophosphorothioate substrates reacted only ~30% against >95% for
5'-monophosphate. See conversion assumption `P-LIG-CONV` and Q-010.

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
