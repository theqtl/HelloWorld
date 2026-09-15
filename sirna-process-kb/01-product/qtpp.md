# Quality Target Product Profile — siRNA drug substance

> All entries are **[SEED]** placeholders showing the expected shape. Replace with the
> actual molecule's profile before any design decision depends on them.

| Element | Target | Rationale | Source |
|---|---|---|---|
| Modality | Double-stranded siRNA, chemically modified, typically 19 to 23 nt per strand | Defines the whole synthesis and purification strategy | [SEED] |
| Conjugation | GalNAc or unconjugated | Conjugate changes hydrophobicity, so it changes chromatographic behaviour and the point at which conjugation is performed | [SEED] |
| Backbone | Mixed phosphodiester and phosphorothioate | PS content drives diastereomer complexity and impurity profile | [SEED] |
| 2' modification | 2'-OMe and 2'-F pattern | Drives amidite cost, coupling efficiency, and nuclease stability | [SEED] |
| Drug substance form | Lyophilised powder or frozen solution | Determines final unit operations and storage infrastructure | [SEED] |
| Counterion | Sodium salt | Standard for oligonucleotide drug substance | [SEED] |
| Annual demand | [TBD] kg per year | The single most important input to facility sizing | [TBD] |
| Batch size | [TBD] kg per batch | Sets column diameter, vessel volume, and synthesiser scale | [TBD] |
| Storage | [TBD] | Drives cold chain and facility footprint | [TBD] |
| Regulatory markets | [TBD] | Determines which guidances bind | [TBD] |

## Why the blanks matter

Annual demand and batch size are not detail to be filled in later. They set the
synthesiser scale, the chromatography column diameter, the solvent recovery duty, the
electrical area classification footprint, and therefore most of the capital cost. Until
they are bracketed, every equipment entry in this knowledge base is provisional.

Recommended approach: carry **three demand scenarios** (low, base, high) through the
design and record which equipment selections are scenario-sensitive. See
`11-open-questions/open-questions.csv`, question OQ-001.
