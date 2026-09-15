# UO-06 — Detritylation

> Status: Seeded | Owner: [TBD] | All content **[SEED]**
> Applies only if purification is run DMT-on. Not applicable in a DMT-off process.

## 1. Purpose and position
Remove the 5' dimethoxytrityl group retained through purification, so that the product is
the final chemical entity. Feeds UO-07.

## 2. Mechanism
Acid-mediated cleavage of the acid-labile trityl ether. The DMT-on strategy uses the
trityl group as a hydrophobic handle, so that full-length product separates strongly from
failure sequences that lack it. The cost is this extra step plus a second conditioning
operation afterwards.

## 3. Stream definition
| | Description | Key attributes | Typical values |
|---|---|---|---|
| Feed | DMT-on purified pool | Purity, DMT-on content | [TBD] |
| Product out | Detritylated product solution | Residual DMT-on, depurination | [TBD] |
| Waste out | Trityl cation and quench stream | | [TBD] |

## 4. Equipment
EQ-060 reaction vessel with pH control and rapid mixing, EQ-061 quench addition system.

## 5. Consumables, buffers and reagents
RG-060 acetic acid or equivalent acid, RG-061 neutralising base.

## 6. Process parameters
| ID | Parameter | Type | Target | Range | Basis | Impact |
|---|---|---|---|---|---|---|
| P-0601 | pH during detritylation | CPP | [TBD] | [TBD] | [SEED] | CQA-06 |
| P-0602 | Contact time | CPP | [TBD] | [TBD] | [SEED] | CQA-06 |
| P-0603 | Temperature | CPP | [TBD] | [TBD] | [SEED] | CQA-06 |
| P-0604 | Quench timing and mixing | CPP | [TBD] | [TBD] | [SEED] | CQA-06 |

**Acid exposure causes depurination.** The parameter set is a race between complete trityl
removal and minimal purine loss, so mixing quality and quench speed matter more than they
appear to. Poor mixing at scale gives locally over-acidified material and a depurination
excursion that a well-mixed lab flask never shows.

## 7. In-process controls and PAT
At-line IP-RP confirming DMT-on clearance and monitoring depurination. In-line pH is the
controlling measurement. Trityl cation is strongly coloured, so in-line visible absorbance
is a cheap and direct reaction progress indicator.

## 8. Scale-up and scale-down
Scale on mixing time relative to reaction time. The constraint that breaks first is
**blend time in a large vessel**.

## 9. Impurity fate
Clears: DMT-on species by conversion. Forms: depurination and abasic products, trityl
alcohol. Passes through: everything else.

## 10. Failure modes
RSK-060 incomplete detritylation, RSK-061 depurination excursion, RSK-062 local pH
excursion from poor mixing.

## 11. Cleaning, changeover and containment
Standard aqueous cleaning. Acid handling controls.

## 12. Environmental and utility load
Modest. Acidic waste neutralisation.

## 13. Open questions
OQ-013, the DMT-on versus DMT-off strategy decision, which must be taken together with
UO-04 and UO-05 rather than in isolation.

## 14. References
[TBD]
