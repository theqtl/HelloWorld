# UO-03 — Initial ultrafiltration and diafiltration

> Status: Seeded | Owner: [TBD] | All content **[SEED]**

## 1. Purpose and position
Remove small-molecule deprotection by-products, residual amines, and organic solvent, and
set the conductivity and pH required for binding on UO-04.

## 2. Mechanism
Tangential flow filtration across a membrane whose cutoff retains the oligonucleotide and
passes small molecules and salts.

## 3. Stream definition
| | Description | Key attributes | Typical values |
|---|---|---|---|
| Feed | Clarified crude | Conductivity, solvent content | [TBD] |
| Product out | Conditioned load for UO-04 | Conductivity, pH, concentration | [TBD] |
| Waste out | Permeate | Volume, amine and solvent load | [TBD] |

## 4. Equipment
EQ-030 TFF skid with cassettes, EQ-031 recirculation vessel.
**Membrane cutoff selection matters:** a single siRNA strand of roughly 20 nucleotides is
only about 7 kDa, so a nominal cutoff well below that is required, and retention should be
confirmed experimentally rather than assumed from the nominal rating.

## 5. Consumables, buffers and reagents
BF-030 diafiltration buffer. See `04-materials/buffer-register.csv`.

## 6. Process parameters
| ID | Parameter | Type | Target | Range | Basis | Impact |
|---|---|---|---|---|---|---|
| P-0301 | Transmembrane pressure | KPP | [TBD] | [TBD] | [SEED] | Flux, yield |
| P-0302 | Crossflow rate | KPP | [TBD] | [TBD] | [SEED] | Flux, shear |
| P-0303 | Diavolumes | CPP | [TBD] | [TBD] | [SEED] | CQA-13 |
| P-0304 | Final concentration | KPP | [TBD] | [TBD] | [SEED] | UO-04 load |
| P-0305 | Temperature | KPP | [TBD] | [TBD] | [SEED] | Flux, stability |

## 7. In-process controls and PAT
In-line conductivity and pH as the primary diafiltration endpoint controls. In-line
variable pathlength UV for concentration, which avoids off-line dilution steps. Permeate
UV to detect product breakthrough, which is the key membrane integrity signal.

## 8. Scale-up and scale-down
Scale on membrane area per unit mass at constant flux and constant diavolumes. The
constraint that breaks first is usually **flux decline at high concentration**.

## 9. Impurity fate
Clears: amines, salts, organic solvent, small-molecule deprotection by-products. Passes
through: all oligonucleotide species.

## 10. Failure modes
RSK-030 membrane fouling, RSK-031 product loss through membrane, RSK-032 incomplete
solvent removal affecting UO-04 binding.

## 11. Cleaning, changeover and containment
Cassette cleaning and reuse validation, or single-use. Reuse requires a carryover study.

## 12. Environmental and utility load
Large aqueous permeate volume, buffer preparation duty.

## 13. Open questions
OQ-008.

## 14. References
[TBD]
