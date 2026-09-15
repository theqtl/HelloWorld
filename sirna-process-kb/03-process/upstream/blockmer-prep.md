# Blockmer preparation

> **[SEED]** throughout. This entry covers preparation of short oligonucleotide blocks
> intended for subsequent joining, whether chemically or enzymatically.

## 1. Terminology, stated precisely

"Blockmer" is used loosely in the field and it is worth fixing the meaning before
designing anything, because the three meanings imply completely different processes.

| Meaning | What it is | Joining method |
|---|---|---|
| Block phosphoramidite | A pre-formed dimer or trimer amidite | Chemical coupling on the synthesiser |
| Synthetic block for ligation | A short, fully deprotected oligonucleotide | Enzymatic ligation |
| Convergent block | A purified intermediate joined to another intermediate | Either |

This knowledge base uses **"block"** for the second meaning unless stated otherwise.
Record which meaning the project adopts as a decision record.

## 2. Block design

The design problem is choosing junction positions. Constraints, in rough order of how
often they are binding:

1. **Modification pattern at the junction.** Enzymatic ligation needs near-native ribose
   and backbone at the nick and usually for one or two positions either side. A fully
   modified siRNA may offer no compliant site at all.
2. **Secondary structure.** Junctions inside stable structure ligate poorly.
3. **Sequence context.** Homopolymer runs allow the splint to anneal out of register,
   which produces deletion products that are very hard to resolve later.
4. **Block length balance.** Roughly equal blocks keep synthesis yield and purification
   burden balanced across the set.
5. **Platform reuse.** If blocks are shared across products, junction choice should favour
   conserved regions.

## 3. Block synthesis

Standard phosphoramidite solid-phase synthesis, but at short length the stepwise yield
penalty is small and crude purity is correspondingly higher than for a full-length strand.

| Parameter | Typical | Note |
|---|---|---|
| Support | CPG or polystyrene | Polystyrene generally preferred at larger scale |
| Coupling activator | Ethylthiotetrazole, dicyanoimidazole, or similar | |
| Oxidation | Iodine and water for PO, or a sulfurising reagent for PS | |
| Cleavage and deprotection | Ammonia or ammonia and methylamine | Conditions constrained by the modification set |
| 2' deprotection | Fluoride-based, where 2'-OH positions exist | Not needed if fully 2'-modified |

## 4. End chemistry required for ligation

This is the part most often underestimated. For the standard T4-type ligation:

- The **acceptor** block needs a free 3'-hydroxyl, and must not carry a 3'-phosphate or
  2',3'-cyclic phosphate.
- The **donor** block needs a 5'-monophosphate.

Two ways to install the 5' phosphate:

| Approach | Advantages | Disadvantages |
|---|---|---|
| Chemical phosphorylation reagent on support | No enzyme, no extra unit operation, scales with synthesis | Adds a coupling step, reagent cost, and its own impurity |
| T4 polynucleotide kinase and ATP | Flexible, high conversion | Adds an enzymatic step, protein clearance, and ATP removal |

Recommendation for a commercial process: **install the phosphate chemically** if the
chemistry permits, because it avoids adding a second enzyme and its clearance burden to
the process. **[SEED]**

## 5. Block purification

Each block is purified before ligation. This is a real and often unbudgeted cost: a
three-block strand requires three purification trains, not one.

The counterargument is that short block purification is easier per unit, since n-1
resolution on a short oligonucleotide is more favourable than on a full-length strand. Whether
the net is favourable is an **empirical question for the specific sequence set**, and it
should be answered with data before the route is fixed. Tracked as OQ-004.

## 6. Block release and control

Blocks joined enzymatically are, in regulatory terms, **starting materials or
intermediates** feeding the drug substance. They need defined specifications, and the
choice of where the GMP boundary sits is a filing decision with real cost consequences.
Tracked as OQ-005.

## 7. Open questions

OQ-002, OQ-004, OQ-005. See `11-open-questions/open-questions.csv`.
