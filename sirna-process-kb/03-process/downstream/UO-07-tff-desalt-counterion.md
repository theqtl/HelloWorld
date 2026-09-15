# UO-07 — Desalting and counterion exchange

> Status: Seeded | Owner: [TBD] | All content **[SEED]**

## 1. Purpose and position
Remove salts, ion-pair reagent, and organic solvent carried from purification, and convert
the product to the intended salt form. Produces the released single strand that feeds UO-08.

## 2. Mechanism
Tangential flow diafiltration against a buffer containing the target counterion, typically
sodium, followed by diafiltration against water or a low-ionic-strength buffer to remove
excess salt.

## 3. Stream definition
| | Description | Key attributes | Typical values |
|---|---|---|---|
| Feed | Polished pool | Ion-pair reagent, solvent, salt content | [TBD] |
| Product out | Desalted single strand, sodium form | CQA-12, CQA-13, concentration | [TBD] |
| Waste out | Permeate with reagent and solvent | Volume, VOC load | [TBD] |

## 4. Equipment
EQ-070 TFF skid, EQ-071 recirculation vessel. The skid must tolerate residual organic
solvent in the early diafiltration volumes.

## 5. Consumables, buffers and reagents
BF-070 sodium-containing exchange buffer, BF-071 final diafiltration medium.

## 6. Process parameters
| ID | Parameter | Type | Target | Range | Basis | Impact |
|---|---|---|---|---|---|---|
| P-0701 | Diavolumes, counterion exchange | CPP | [TBD] | [TBD] | [SEED] | CQA-12 |
| P-0702 | Diavolumes, desalting | CPP | [TBD] | [TBD] | [SEED] | CQA-13 |
| P-0703 | Transmembrane pressure | KPP | [TBD] | [TBD] | [SEED] | Flux |
| P-0704 | Final concentration | CPP | [TBD] | [TBD] | [SEED] | UO-08 stoichiometry |
| P-0705 | Temperature | KPP | [TBD] | [TBD] | [SEED] | Flux, stability |

**Final concentration is more critical here than it looks.** UO-08 requires an accurate
strand-to-strand molar ratio, and the concentration measurement made at the end of this
step is what that ratio is calculated from. Measurement error here becomes a strand ratio
deviation at annealing that cannot be corrected later.

## 7. In-process controls and PAT
In-line conductivity as the diafiltration endpoint. In-line variable pathlength UV for
concentration, which avoids the dilution error inherent in off-line measurement. At-line
ion chromatography for counterion confirmation. At-line residual solvent by headspace GC.

## 8. Scale-up and scale-down
Scale on membrane area at constant flux and diavolumes.

## 9. Impurity fate
Clears: ion-pair reagent, organic solvent, salts, small molecules. Passes through: all
oligonucleotide species.

## 10. Failure modes
RSK-070 incomplete ion-pair reagent removal, RSK-071 concentration measurement error
propagating to strand ratio, RSK-072 membrane fouling.

## 11. Cleaning, changeover and containment
Cassette cleaning and reuse validation, or single-use.

## 12. Environmental and utility load
Large permeate volumes containing solvent and amine, requiring appropriate treatment.

## 13. Open questions
OQ-014.

## 14. References
[TBD]
