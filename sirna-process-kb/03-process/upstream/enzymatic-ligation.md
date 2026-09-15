# Enzymatic ligation

> **[SEED]** throughout. Applies only if the chemoenzymatic route is selected.

## 1. Purpose

Join purified synthetic blocks into the full-length strand using an RNA ligase, avoiding
the compounding stepwise yield loss of long solid-phase synthesis.

## 2. Enzyme options

| Enzyme | Requires splint | Donor 5' end | Acceptor 3' end | Cofactor | Notes |
|---|---|---|---|---|---|
| T4 RNA ligase 2, full length | Yes, seals a nick in duplex | 5'-phosphate | 3'-OH | ATP, Mg | Workhorse for splinted RNA joining |
| T4 RNA ligase 2, truncated | No | 5'-adenylylated | 3'-OH | None, pre-adenylylated donor | Avoids ATP side reactions, needs pre-adenylylated block |
| T4 RNA ligase 1 | No | 5'-phosphate | 3'-OH | ATP, Mg | Single-strand ligation, gives circles and concatemers |
| RtcB | No | 5'-OH | 3'-phosphate or 2',3'-cyclic phosphate | GTP, Mn | Opposite end chemistry, splint-free |
| T4 DNA ligase | Yes | 5'-phosphate | 3'-OH | ATP, Mg | Poor on RNA nicks, generally not preferred |

## 3. Junction design constraints

The controlling constraint. **2'-OMe, 2'-F, LNA, and phosphorothioate at or adjacent to
the nick slow or abolish ligation**, and the two phosphorothioate diastereomers do not
ligate at equal rates. A viable junction generally needs near-native chemistry at the nick
and for one to two positions on each side.

**For a fully modified siRNA this may mean no viable junction exists.** Establish this
before any other work on this route. See OQ-002.

## 4. Splint design

| Attribute | Guidance |
|---|---|
| Chemistry | DNA, or a 2'-OMe or LNA chimera for higher melting temperature and nuclease resistance |
| Arm length | Long enough that the melting temperature sits comfortably above reaction temperature |
| Specificity | Screened against off-register annealing elsewhere in the construct |
| Handle | Biotin allows affinity removal instead of enzymatic digestion |
| Removal | Nuclease digestion, affinity capture, or chromatographic resolution |

A modified splint is more expensive but survives the reaction and simplifies removal. A
plain DNA splint is cheap and is cleanly digested by DNase, at the cost of adding a second
enzyme and its own clearance burden.

## 5. Reaction conditions

| Parameter | Typical range | Note |
|---|---|---|
| Temperature | 25 to 37 C | Higher if a thermostable ligase and a high-melting splint are used |
| pH | 7.5 to 8.0 | |
| ATP | 0.1 to 1 mM | Tuned, not maximised. See below |
| Magnesium | 2 to 10 mM | |
| Crowding agent | PEG 8000, 5 to 15 percent | Significantly improves conversion, but complicates downstream removal |
| Splint to acceptor ratio | 1.0 to 1.3 | |
| Anneal | Controlled ramp before enzyme addition | Anneal first, then add enzyme |
| Step conversion | 60 to 90 percent | The dominant economic variable |

**On ATP:** too little stalls turnover; too much keeps re-adenylylating the ligase and
accumulates the 5'-adenylylated dead-end species. That species runs very close to product
and is among the hardest impurities to resolve, so ATP concentration deserves a designed
experiment rather than a default.

## 6. Scale-up concerns not present at the bench

1. **PEG removal.** A crowding agent that helps conversion must be cleared, and it loads
   the first downstream step.
2. **Enzyme cost and supply.** Kilogram-scale ligation needs a GMP-grade, secure enzyme
   supply. This is a genuine supply chain dependency and an audit obligation.
3. **Enzyme and splint clearance validation.** Adds CQA-17 and CQA-18, each requiring a
   validated clearance argument and an assay.
4. **Anneal at volume.** Controlled thermal ramps are straightforward in a tube and are a
   real equipment specification in a vessel.
5. **Unreacted blocks.** Failed ligation leaves blocks that must be resolved from product,
   and a block is a much larger mass difference than n-1, so this is comparatively easy.
6. **Adenylylated species.** Hardest of the new impurities. A deadenylase treatment can
   convert it back, at the cost of yet another enzyme.

## 7. Honest position

For siRNA at 19 to 23 nucleotides per strand, enzymatic ligation adds two unit operations,
three impurity classes, two new assays, and an enzyme supply dependency, in exchange for a
yield benefit that is **much smaller than it would be for a long RNA**. The route deserves
a deliberate justification rather than adoption by momentum.

The strongest siRNA-specific case is a **shared block library across a portfolio**, where
the economics come from reuse rather than from yield. If that is the rationale, it should
be stated and tested as such.

## 8. Open questions

OQ-002, OQ-004, OQ-005, OQ-006.
