# UO-01 — Cleavage and deprotection

> Status: Seeded | Owner: [TBD] | All content **[SEED]**

## 1. Purpose and position
Release the oligonucleotide from the solid support and remove the base, phosphate, and
2' protecting groups. Feeds UO-02. If this step is incomplete, the resulting partially
protected species are difficult to resolve downstream, so it is a purity-defining step
despite being conceptually simple.

## 2. Mechanism
Nucleophilic cleavage of the succinyl support linkage and of base-protecting groups, using
aqueous or anhydrous ammonia, or ammonia with methylamine. Fluoride-mediated removal of
silyl 2' protecting groups where 2'-OH positions exist. Fully 2'-modified constructs may
not require the fluoride step.

## 3. Stream definition
| | Description | Key attributes | Typical values |
|---|---|---|---|
| Feed | Loaded solid support | Loading, mass | [TBD] |
| Product out | Crude oligonucleotide in aqueous or aqueous-organic solution | Crude purity, concentration | [TBD] |
| Waste out | Spent support, protecting group by-products, amine vapour | Amine load, VOC | [TBD] |

## 4. Equipment
EQ-010 deprotection vessel with jacket and reflux, EQ-011 support filtration.
Ammonia and methylamine handling drives a dedicated scrubbed vessel and local exhaust.

## 5. Consumables, buffers and reagents
RG-010 ammonium hydroxide, RG-011 methylamine, RG-012 triethylamine trihydrofluoride or
equivalent, RG-013 quench. See `04-materials/reagent-register.csv`.

## 6. Process parameters
| ID | Parameter | Type | Target | Range | Basis | Impact |
|---|---|---|---|---|---|---|
| P-0101 | Deprotection temperature | CPP | [TBD] | [TBD] | [SEED] | CQA-06, CQA-07 |
| P-0102 | Deprotection time | CPP | [TBD] | [TBD] | [SEED] | CQA-07 |
| P-0103 | Reagent ratio and excess | KPP | [TBD] | [TBD] | [SEED] | CQA-07 |
| P-0104 | 2' deprotection time and temperature | CPP | [TBD] | [TBD] | [SEED] | CQA-07 |

Temperature and time trade directly against depurination. Aggressive conditions clear
protecting groups but generate abasic species, so this is an optimisation with a genuine
optimum rather than a maximise-or-minimise.

## 7. In-process controls and PAT
At-line IP-RP or LC-MS confirming complete deprotection before release to UO-02.
In-line temperature and pressure. A residual-protecting-group check is the meaningful
control here.

## 8. Scale-up and scale-down
Scale on reagent-to-support ratio and on heat transfer. The constraint that breaks first
is **heat and mass transfer in a large vessel**, giving position-dependent deprotection
extent that a small vessel does not show.

## 9. Impurity fate
Forms: depurination and abasic products (CQA-06). Clears: protecting groups. Passes
through: all synthesis-derived sequence impurities, n-1, n+1, PO species.

## 10. Failure modes
RSK-010 incomplete deprotection, RSK-011 depurination from excessive conditions,
RSK-012 amine release to workplace.

## 11. Cleaning, changeover and containment
Amine and fluoride handling both require engineered controls. Fluoride reagents demand
specific material compatibility and dedicated first-aid provision.

## 12. Environmental and utility load
Amine scrubbing duty, fluoride-bearing waste segregation, cooling.

## 13. Open questions
OQ-007.

## 14. References
[TBD]
