# UO-09 — Final UF/DF and formulation

> Status: Seeded | Owner: [TBD] | All content **[SEED]**

## 1. Purpose and position
Exchange the annealed duplex into the final drug substance matrix and adjust to target
concentration. Feeds UO-10.

## 2. Mechanism
Tangential flow diafiltration into the final medium, followed by concentration adjustment.
Conditions must stay below the duplex melting temperature throughout, since this step
operates on an annealed product that can be dissociated by heat or by low ionic strength.

## 3. Stream definition
| | Description | Key attributes | Typical values |
|---|---|---|---|
| Feed | Annealed duplex | CQA-08, concentration | [TBD] |
| Product out | Formulated drug substance solution | CQA-10, CQA-08 | [TBD] |
| Waste out | Permeate | Volume | [TBD] |

## 4. Equipment
EQ-090 TFF skid, EQ-091 formulation vessel, EQ-092 accurate concentration measurement.

## 5. Consumables, buffers and reagents
BF-090 final formulation medium.

## 6. Process parameters
| ID | Parameter | Type | Target | Range | Basis | Impact |
|---|---|---|---|---|---|---|
| P-0901 | Diavolumes | CPP | [TBD] | [TBD] | [SEED] | Matrix exchange |
| P-0902 | Final concentration | CPP | [TBD] | [TBD] | [SEED] | CQA-10 |
| P-0903 | Temperature | CPP | [TBD] | [TBD] | [SEED] | CQA-08, duplex integrity |
| P-0904 | Transmembrane pressure and crossflow | KPP | [TBD] | [TBD] | [SEED] | Flux, shear |
| P-0905 | Hold time before UO-10 | CPP | [TBD] | [TBD] | [SEED] | CQA-15, CQA-16 |

Ionic strength during diafiltration must be checked against duplex stability. Diafiltering
an annealed duplex into water is a plausible-looking step that can partially dissociate the
product.

## 7. In-process controls and PAT
In-line conductivity, in-line variable pathlength UV for concentration, at-line duplex
confirmation to verify the product survived the step, bioburden sampling at the hold.

## 8. Scale-up and scale-down
Scale on membrane area at constant flux and diavolumes.

## 9. Impurity fate
Clears: residual salts from annealing buffer. Risk of forming: dissociated single strand if
conditions are wrong.

## 10. Failure modes
RSK-090 duplex dissociation during diafiltration, RSK-091 concentration out of range,
RSK-092 bioburden excursion during hold.

## 11. Cleaning, changeover and containment
Cassette cleaning and reuse validation. Bioburden control becomes the dominant concern from
this step onward.

## 12. Environmental and utility load
Buffer preparation and permeate handling.

## 13. Open questions
OQ-016.

## 14. References
[TBD]
