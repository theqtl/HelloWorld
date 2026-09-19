# Enzymatic ligation

Chemically synthesised blocks are joined into the siRNA strand(s) by enzymatic ligation. This is
a fixed decision; the work here is how to make it robust.

## Enzyme and chemistry

- The viable class is **double-stranded RNA (nick-sealing) ligases** — T4 RNA ligase 2 family and
  engineered variants (<span class="prov-fact">fact</span>, bench→1 L, fully modified siRNA;
  [SRC-ALMAC-2023](../registers/sources.md); vendor [SRC-CODEXIS](../registers/sources.md)).
- **Wild-type T4 DNA ligase is poor at** 2'-OMe substrates (not "unable"): it is "poor at ligating
  2′-OMe substituted oligonucleotide segments", and on an RNA-splinted substrate T4 DNA ligase gives
  essentially all adenylylated dead-end product (<span class="prov-fact">fact</span>;
  [SRC-USPTO-10640812](../registers/sources.md), [SRC-PBCV1-2014](../registers/sources.md)). The same
  patent — GlaxoSmithKline's engineered-ligase patent "Processes for the production of oligonucleotides",
  not a T4 negative-result patent — identifies alternatives that **do** work, including engineered
  Enterobacteria phage CC31 variants and Chlorella virus DNA ligase (SplintR), reported as peak-area
  improvements only, so it states no conversion, yield or purity number and does not close Q-010
  (<span class="prov-fact">fact</span>; [SRC-USPTO-10640812](../registers/sources.md)).
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

The circulating vendor trio — ">95% conversion, substrate loads up to 100 g/L, >98% post-purification
purity" — is **marketing-only**: it is traceable to a single company blog
([SRC-CODEXIS](../registers/sources.md)) and is corroborated **nowhere**, including in the company's
own press release (whose only numeric claim, >98% incorporation, is for a different, non-ligation
chemistry; [SRC-CODEXIS-PR-2024](../registers/sources.md)) and in all four of its ligation patent
families, which report only relative fold-improvement conversions
([SRC-CODEXIS-PATENTS](../registers/sources.md)). Treat it as an unverified vendor claim of unstated
basis. The design anchors are instead the **measured** figures: a ~1 mM working titre in a 1 L vessel
([SRC-ALMAC-2023](../registers/sources.md), Q-016/Q-034) and >92% per-ligation flow conversion
([SRC-CN119265174](../registers/sources.md), `P-LIG-CONV`). The often-quoted 82–96% conversion range
is a ligase screen on an **unmodified** shortmer whose 5'-monophosphorothioate substrates reacted only
~30% ([SRC-NATCOMM-2024](../registers/sources.md)). Per-ligation conversion must not be read as a step
yield or as overall mass yield (19–43% at campaign scale; `P-YIELD-OVERALL-PUB`). See Q-010.

## Side reactions to control at the reaction

The **adenylylated dead-end (+AMP)** has been directly observed in exactly this chemistry — the
by-product "2.3_2.4[+AMP]" in fully modified siRNA blockmer ligation — alongside hairpins, concatemers
and 3'-terminal-nucleotide loss (<span class="prov-fact">fact</span>;
[SRC-ALMAC-2023](../registers/sources.md), Table 1). The authors' mitigation was to change the
disconnection and reaction staging so the species does not form, not to remove it downstream: it
differs from product by ~one residue and **cannot be cleared by filtration** (risk R-010, now anchored
to this observation). Controlled by directional assembly, keeping ≤3 blockmers present at once, and
tuning temperature/time.

There is an **ATP tension** with no public resolution for a modified-siRNA system (Q-040): a
four-ligation assembly needs "at least 4 mM ATP" ([SRC-WO2025262452](../registers/sources.md)), yet
abortive adenylylation is suppressed only at "<100 µM" ATP
([SRC-PBCV1-2014](../registers/sources.md), unmodified DNA on RNA splints — the mechanism transfers,
the number does not). ATP regeneration from AMP has a hard 66% equilibrium ceiling. The
mechanistically indicated route is an ATP-limited fed-batch or AMP regeneration that holds free ATP
low (<span class="prov-inference">inference</span>, ours; neither patent says this).

## Enzyme removal — the linchpin

Soluble ligase cannot be cleared from the smaller strand by size ultrafiltration. **Immobilised or
solid-phase ligase**, removed by filtration/centrifugation, is the route to keep the train
filtration-led (finding: [filtration](../findings/filtration.md) §4). An immobilised RNA ligase has
held >92% conversion on fully modified siRNA blocks for over 100 h
([SRC-CN119265174](../registers/sources.md)), so the *duty* half of the immobilisation risk is
answered — but the same patent still heat-kills and runs an ion column, and **quantitative clearance
data is not publicly available**: no ppm, log-reduction or immunoassay figure for ligase clearance
exists anywhere the dive read (Q-032, restated; risk R-002). A cell-free-extract route feeds a whole
proteome plus endotoxin, not one enzyme, which raises the clearance burden (R-017). A chromatographic
fallback is retained.

## GMP sourcing

GMP-grade T4 ligases are commercially listed; the high-performance engineered dsRNA ligases and
PNKs are proprietary to the platform owners. Recombinant *E. coli* expression is animal-free;
endotoxin-controlled strains exist (<span class="prov-fact">fact</span>). Residual-enzyme
acceptance criteria specific to GMP siRNA ligation are a gap.
