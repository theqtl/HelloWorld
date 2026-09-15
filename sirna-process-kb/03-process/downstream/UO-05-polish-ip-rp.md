# UO-05 — Polish chromatography, ion-pair reverse phase

> Status: Seeded | Owner: [TBD] | All content **[SEED]**
> The second purity-defining step, and orthogonal to UO-04.

## 1. Purpose and position
Resolve the closely related species that anion exchange leaves behind, using a separation
mechanism based on hydrophobicity rather than charge. Feeds UO-06 or UO-07.

## 2. Mechanism
An alkylamine ion-pairing reagent pairs with the phosphate backbone, making the
oligonucleotide retain on a reverse phase stationary phase. A fluorinated alcohol modifier,
most commonly hexafluoroisopropanol, controls ion-pair strength and improves peak shape and
mass spectrometry compatibility. Selectivity depends on the ion-pair reagent chain length,
which is a genuine tuning handle rather than a fixed choice.

Because the mechanism is hydrophobic rather than charge-based, it is **orthogonal** to
UO-04, which is why the two steps together clear impurities that neither clears alone.

## 3. Stream definition
| | Description | Key attributes | Typical values |
|---|---|---|---|
| Feed | UO-04 pool | Purity, salt content | [TBD] |
| Product out | Polished pool | Purity, solvent and ion-pair reagent content | [TBD] |
| Waste out | Side fractions, organic waste | Product loss, solvent volume | [TBD] |

## 4. Equipment
EQ-050 preparative chromatography skid rated for organic solvent, EQ-051 column,
EQ-052 fraction vessels. **This skid and its room are in a flammable-solvent area.** That
single fact propagates into electrical classification, HVAC, drainage, and fire protection,
and it is the main reason this step drives facility cost out of proportion to its size.

## 5. Consumables, buffers and reagents
Stationary phase: polymeric or silica-based C18 or C8. Mobile phase RG-050 ion-pair
reagent such as triethylamine, RG-051 hexafluoroisopropanol, RG-052 acetonitrile,
BF-050 aqueous phase.

**Supply and regulatory risk on hexafluoroisopropanol.** It is a fluorinated compound, it is
expensive, and fluorochemical restrictions under evaluation in several jurisdictions create
a real medium-term availability and compliance question for a facility being designed now.
A greenfield design should either secure supply, plan recovery, or qualify an alternative.
Tracked as risk RSK-052 and open question OQ-011.

## 6. Process parameters
| ID | Parameter | Type | Target | Range | Basis | Impact |
|---|---|---|---|---|---|---|
| P-0501 | Load mass per litre of stationary phase | CPP | [TBD] | [TBD] | [SEED] | CQA-02 to CQA-05, yield |
| P-0502 | Ion-pair reagent identity and concentration | CPP | [TBD] | [TBD] | [SEED] | Selectivity |
| P-0503 | Fluorinated modifier concentration | CPP | [TBD] | [TBD] | [SEED] | Selectivity, peak shape |
| P-0504 | Organic gradient slope | CPP | [TBD] | [TBD] | [SEED] | Resolution |
| P-0505 | Temperature | CPP | [TBD] | [TBD] | [SEED] | Selectivity, structure |
| P-0506 | Linear velocity | KPP | [TBD] | [TBD] | [SEED] | Resolution |
| P-0507 | Pooling criteria | CPP | [TBD] | [TBD] | [SEED] | CQA-02, yield |

## 7. In-process controls and PAT
Multi-wavelength in-line UV, in-line conductivity, at-line UPLC for purity-based pooling,
and optionally on-line mass spectrometry for identity confirmation on the pool. Column
performance testing between cycles.

## 8. Scale-up and scale-down
Same scaling logic as UO-04. Additional constraint: **temperature uniformity across a
large-diameter bed**, since this separation is more temperature-sensitive than anion
exchange, and a radial gradient degrades resolution in a way small columns do not reveal.

## 9. Impurity fate
Clears: n-1, n+1, PO impurities, depurination products, DMT-on species if operating
DMT-on, residual protecting group species. Introduces: ion-pair reagent and organic
solvent, both of which must be cleared by UO-07. Passes through: species matching product
in both charge and hydrophobicity, which after two orthogonal steps should be very few.

## 10. Failure modes
RSK-050 resolution loss at scale, RSK-051 temperature non-uniformity, RSK-052 ion-pair
reagent supply or regulatory restriction, RSK-053 solvent recovery failure,
RSK-054 stationary phase lifetime shortfall.

## 11. Cleaning, changeover and containment
Organic-compatible cleaning, solvent flush, and column storage in organic. Operator
exposure to acetonitrile and fluorinated alcohol requires closed transfer and local exhaust.

## 12. Environmental and utility load
**The largest solvent consumer in the process.** Acetonitrile recovery by distillation
should be evaluated explicitly, since it changes both operating cost and the environmental
permit. Waste solvent volume, VOC emissions, and fluorinated waste disposal are all
material design inputs. Tracked as OQ-012.

## 13. Open questions
OQ-011, OQ-012.

## 14. References
[TBD]
