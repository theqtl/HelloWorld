# UO-11 — Lyophilisation

> Status: Seeded | Owner: [TBD] | All content **[SEED]**
> Applies only if drug substance is supplied as a solid. Not applicable for frozen liquid.

## 1. Purpose and position
Remove water to produce a stable solid drug substance. Feeds UO-12.

## 2. Mechanism
Freezing, then primary drying by sublimation under vacuum, then secondary drying by
desorption of bound water at elevated shelf temperature.

## 3. Stream definition
| | Description | Key attributes | Typical values |
|---|---|---|---|
| Feed | Filtered drug substance solution | Concentration, fill depth | [TBD] |
| Product out | Lyophilised solid | CQA-11 water content, CQA-08 | [TBD] |
| Waste out | Condensed water vapour | | |

## 4. Equipment
EQ-110 production lyophiliser with bulk trays, EQ-111 loading and unloading isolation.
**This is typically the longest single operation in the train and often the capacity
bottleneck.** Cycle duration in days rather than hours means lyophiliser count, not
chromatography, can set facility throughput.

## 5. Consumables, buffers and reagents
None beyond the formulated solution. Any bulking agent or cryoprotectant, if used, must be
defined in UO-09.

## 6. Process parameters
| ID | Parameter | Type | Target | Range | Basis | Impact |
|---|---|---|---|---|---|---|
| P-1101 | Freezing rate and final freeze temperature | CPP | [TBD] | [TBD] | [SEED] | Cake structure |
| P-1102 | Primary drying shelf temperature | CPP | [TBD] | [TBD] | [SEED] | CQA-11, cycle time |
| P-1103 | Chamber pressure | CPP | [TBD] | [TBD] | [SEED] | Sublimation rate |
| P-1104 | Primary drying duration | CPP | [TBD] | [TBD] | [SEED] | CQA-11 |
| P-1105 | Secondary drying temperature and duration | CPP | [TBD] | [TBD] | [SEED] | CQA-11 |
| P-1106 | Fill depth | CPP | [TBD] | [TBD] | [SEED] | Cycle time, uniformity |

## 7. In-process controls and PAT
| Technique | Placement | Decision driven |
|---|---|---|
| Product temperature probes | In-line | Primary drying control |
| Comparative pressure measurement, Pirani versus capacitance | In-line | Primary drying endpoint |
| Tunable diode laser absorption spectroscopy | In-line | Sublimation rate, endpoint |
| Near infrared | At-line or in-line | Residual moisture |
| Karl Fischer | Off-line | Release moisture |

Endpoint determination by in-line measurement rather than by fixed time is the main PAT
opportunity, and on a multi-day cycle it converts directly into capacity.

## 8. Scale-up and scale-down
Scale on heat and mass transfer per unit area at constant product temperature history. The
constraint that breaks first is **shelf-to-shelf and edge-to-centre uniformity**, which
laboratory dryers systematically fail to represent.

## 9. Impurity fate
Concentrates everything. Removes water. Risk of duplex destabilisation if the cycle is
poorly designed.

## 10. Failure modes
RSK-110 cake collapse, RSK-111 incomplete drying, RSK-112 non-uniform drying across the
chamber, RSK-113 extended cycle consuming capacity, RSK-114 duplex integrity loss.

## 11. Cleaning, changeover and containment
Chamber cleaning and sanitisation, loading and unloading under appropriate classification.

## 12. Environmental and utility load
Significant refrigeration and vacuum duty, sustained over long cycles. A material
contributor to facility energy demand.

## 13. Open questions
OQ-018, solid versus frozen liquid drug substance, which should be decided early because
it determines whether lyophilisers are in the facility at all.

## 14. References
[TBD]
