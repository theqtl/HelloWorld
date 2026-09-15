# UO-04 — Capture chromatography, anion exchange

> Status: Seeded | Owner: [TBD] | All content **[SEED]**
> This is one of the two purity-defining steps. It deserves the most experimental effort
> of any operation in the train.

## 1. Purpose and position
Capture full-length product from the conditioned crude and reject synthesis-derived
sequence impurities. Feeds UO-05.

## 2. Mechanism
Strong anion exchange on the phosphate backbone. Retention increases with charge, so it
increases with length, which is the basis of n-1 and n+1 separation. Commonly run at
elevated pH, sometimes with a chaotrope or organic modifier, to suppress secondary
structure so that separation depends on charge rather than on conformation.

Phosphorothioate content complicates this: PS and PO species of the same length differ in
retention, so the missing-sulfur impurity (CQA-05) is partly addressed here, and the
diastereomer distribution broadens peaks.

## 3. Stream definition
| | Description | Key attributes | Typical values |
|---|---|---|---|
| Feed | Conditioned crude, low conductivity | Crude purity, load mass | [TBD] |
| Product out | Enriched full-length pool | Purity, pool volume, salt content | [TBD] |
| Waste out | Early and late eluting fractions, regeneration stream | Product loss | [TBD] |

## 4. Equipment
EQ-040 process chromatography skid, EQ-041 axial compression or packed column,
EQ-042 fraction collection vessels. Column diameter is set by required bed volume at the
resolution-limited load, not by binding capacity.

## 5. Consumables, buffers and reagents
Stationary phase: polymeric strong anion exchanger, for example a quaternary amine on a
polystyrene-divinylbenzene or methacrylate base. Buffers BF-040 equilibration, BF-041
elution with a salt gradient, BF-042 strip, BF-043 regeneration, BF-044 storage.

Salt selection is a real decision. Chloride, bromide, and perchlorate give different
selectivity and different corrosion and disposal consequences. Perchlorate in particular
carries handling and effluent obligations that can surprise a facility team late in design.

## 6. Process parameters
| ID | Parameter | Type | Target | Range | Basis | Impact |
|---|---|---|---|---|---|---|
| P-0401 | Load mass per litre of resin | CPP | [TBD] | [TBD] | [SEED] | CQA-02 to CQA-05, yield |
| P-0402 | Linear velocity | CPP | [TBD] | [TBD] | [SEED] | Resolution |
| P-0403 | Gradient slope | CPP | [TBD] | [TBD] | [SEED] | Resolution |
| P-0404 | Elution pH | CPP | [TBD] | [TBD] | [SEED] | Selectivity |
| P-0405 | Temperature | CPP | [TBD] | [TBD] | [SEED] | Selectivity, structure |
| P-0406 | Bed height | KPP | [TBD] | [TBD] | [SEED] | Resolution |
| P-0407 | Pooling criteria | CPP | [TBD] | [TBD] | [SEED] | CQA-02, yield |
| P-0408 | Resin cycle number | CPP | [TBD] | [TBD] | [SEED] | Carryover, resolution |

**The central trade-off.** Load, purity, and yield cannot be optimised independently.
Raising load degrades n-1 resolution, which forces tighter pooling, which loses yield. The
commercial process sits at a deliberately chosen point on that surface, and that point
should be selected with a documented rationale rather than inherited from development.

## 7. In-process controls and PAT
| Technique | Placement | Decision driven |
|---|---|---|
| Multi-wavelength UV | In-line | Pooling start and stop |
| Conductivity and pH | In-line | Gradient verification, step confirmation |
| On-line or at-line UPLC | At-line on fractions | Purity-based pooling rather than UV-based |
| Column performance test, HETP and asymmetry | Between cycles | Column health and repack trigger |

**Purity-based pooling using at-line chromatography is the single highest-value PAT
opportunity in this process.** UV-based pooling cannot distinguish n-1 from product, so it
forces conservative pooling and therefore costs yield on every batch.

## 8. Scale-up and scale-down
Scale on constant bed height, constant linear velocity, and constant load per unit volume
of resin, increasing diameter. The constraints that break first are **packing quality at
large diameter** and **extra-column dispersion in the skid**, both of which erode the
resolution demonstrated at small scale.

A qualified scale-down model is essential, because most of the process characterisation
work will be done on it.

## 9. Impurity fate
Clears: shortmers, some n-1, longmers, some PO species, residual small molecules. Partially
clears: n-1, n+1, and PO impurities, which are the resolution-limited ones. Passes through:
species of identical charge and near-identical structure.

## 10. Failure modes
RSK-040 resolution loss at scale, RSK-041 column packing failure, RSK-042 resin fouling and
lifetime shortfall, RSK-043 pooling decision error, RSK-044 carryover between campaigns.

## 11. Cleaning, changeover and containment
Cleaning in place with alkali, salt strip, and storage solution. Resin lifetime and
carryover studies are required for a multi-product facility, and a decision is needed on
whether columns are dedicated per product. That decision drives floor area directly and
should be taken early. Tracked as OQ-009.

## 12. Environmental and utility load
Large buffer volumes, high salt effluent, column temperature control duty. Buffer
preparation and hold capacity for this step alone can dominate the facility's tank farm.
In-line buffer dilution or formulation should be evaluated to reduce that footprint.

## 13. Open questions
OQ-009, OQ-010.

## 14. References
[TBD]
