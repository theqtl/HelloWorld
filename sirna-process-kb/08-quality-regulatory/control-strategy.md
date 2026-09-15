# Control strategy

> **[SEED]**. Rendered from the unit operation entries. Do not edit values here. Edit the
> unit operation entry and regenerate.

## Structure

Per ICH Q10 and Q11, the control strategy is the planned set of controls, derived from
product and process understanding, that assures process performance and product quality.
It comprises:

1. Material controls, in `04-materials/`.
2. Process parameter controls, in the unit operation entries, section 6.
3. In-process controls and PAT, in the unit operation entries, section 7, and `06-pat-analytics/`.
4. Facility and equipment controls, in `05-equipment/` and `07-facility/`.
5. Specifications and release testing, in `01-product/cqa-register.md` and the analytical method register.

## CQA to control map

| CQA | Primary control | Secondary control | Release test |
|---|---|---|---|
| CQA-01 identity | Synthesis fidelity, sequence verification of amidite addition | Purification | AM-001, AM-002 |
| CQA-02 full-length content | UO-04 and UO-05 pooling criteria | Load control | AM-003, AM-004 |
| CQA-03 n-1 | UO-04 and UO-05 resolution and pooling | Coupling efficiency in synthesis | AM-003, AM-005 |
| CQA-04 n+1 | UO-04 and UO-05 resolution and pooling | Capping efficiency in synthesis | AM-003, AM-005 |
| CQA-05 PO impurities | Sulfurisation control in synthesis | UO-04 and UO-05 | AM-003 |
| CQA-06 depurination | UO-06 pH, time, mixing, quench | UO-01 conditions | AM-003 |
| CQA-07 residual protecting group | UO-01 parameters | Purification | AM-003 |
| CQA-08 duplex content | UO-08 ramp and ionic strength | UO-09 conditions | AM-006, AM-008 |
| CQA-09 strand ratio | UO-08 charge accuracy, driven by UO-07 concentration assay | | AM-007 |
| CQA-10 assay | UO-09 concentration control | | AM-009 |
| CQA-11 water | UO-11 secondary drying, UO-12 humidity | | AM-010 |
| CQA-12 counterion | UO-07 diavolumes | | AM-011 |
| CQA-13 residual solvent | UO-07 diavolumes, UO-11 | | AM-012 |
| CQA-14 elemental impurities | Raw material control, risk-based | Contact material selection | AM-013 |
| CQA-15 bioburden | UO-10, hold time control from UO-09 | Facility controls | AM-014 |
| CQA-16 endotoxin | Water and raw material control | UF/DF clearance | AM-015 |
| CQA-17 residual splint | Nuclease digestion and chromatography | | AM-016 |
| CQA-18 residual ligase | Chromatography and UF/DF clearance | | AM-017 |
| CQA-19 adenylylated species | Ligation condition control, chromatography | Deadenylase treatment | AM-018 |
| CQA-20 appearance and pH | UO-09 formulation | | AM-019 |

## The structural weakness to be honest about

**Everything after UO-08 is non-purifying.** Once the strands are annealed, no subsequent
operation removes a sequence-related impurity. The control strategy therefore rests almost
entirely on the two chromatography steps and on the release testing of each single strand
before annealing.

This has a direct design consequence: **single strands should be tested and released as
intermediates before annealing**, not merely sampled. Discovering an out-of-specification
strand after annealing means losing both strands. Tracked as OQ-024.
