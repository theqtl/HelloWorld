# UO-08 — Annealing

> Status: Seeded | Owner: [TBD] | All content **[SEED]**
> The step where two separately manufactured intermediates become one drug substance.

## 1. Purpose and position
Hybridise sense and antisense strands into the siRNA duplex. Feeds UO-09.

## 2. Mechanism
Controlled thermal denaturation followed by a controlled cooling ramp in a defined ionic
environment, allowing complementary strands to form the thermodynamically favoured duplex.
The ionic strength suppresses backbone repulsion and the cooling rate determines whether
the system reaches the intended duplex rather than kinetically trapped structures.

## 3. Stream definition
| | Description | Key attributes | Typical values |
|---|---|---|---|
| Feed A | Sense strand solution | Concentration, purity | [TBD] |
| Feed B | Antisense strand solution | Concentration, purity | [TBD] |
| Product out | Annealed duplex | CQA-08, CQA-09 | [TBD] |
| Waste out | None in normal operation | | |

## 4. Equipment
EQ-080 jacketed vessel with accurate and uniform temperature control and a programmable
ramp, EQ-081 accurate charge and weighing system for stoichiometric addition.

Temperature uniformity is the specification that matters. A vessel that reaches setpoint
at the probe while the wall and centre differ will anneal non-uniformly.

## 5. Consumables, buffers and reagents
BF-080 annealing buffer, typically a defined salt and buffer system.

## 6. Process parameters
| ID | Parameter | Type | Target | Range | Basis | Impact |
|---|---|---|---|---|---|---|
| P-0801 | Strand molar ratio | CPP | 1.00 | [TBD] | [SEED] | CQA-09 |
| P-0802 | Total concentration | CPP | [TBD] | [TBD] | [SEED] | CQA-08 |
| P-0803 | Ionic strength | CPP | [TBD] | [TBD] | [SEED] | CQA-08 |
| P-0804 | Denaturation temperature and hold | CPP | [TBD] | [TBD] | [SEED] | CQA-08 |
| P-0805 | Cooling ramp rate | CPP | [TBD] | [TBD] | [SEED] | CQA-08 |
| P-0806 | Final hold temperature | KPP | [TBD] | [TBD] | [SEED] | CQA-08 |

**Strand ratio is the parameter to get right.** Excess of either strand leaves free single
strand in the drug substance, which is both a specification failure and, depending on which
strand is in excess, a potential safety consideration. The ratio is set by the concentration
assays performed at the end of UO-07, so the control for this step actually lives upstream.

## 7. In-process controls and PAT
At-line non-denaturing analysis, such as native anion exchange, size exclusion, or
non-denaturing capillary gel electrophoresis, to confirm duplex content. UV thermal melting
to confirm duplex identity and stability. At-line denaturing analysis to confirm strand
ratio. In-line temperature profile recording across multiple probes.

An in-line or at-line duplex confirmation is worth real investment here, because reworking
a failed anneal means redissolving and re-annealing very high-value material.

## 8. Scale-up and scale-down
Scale on heat transfer area per unit volume at constant ramp rate. The constraint that
breaks first is **achieving the specified cooling ramp uniformly in a large vessel**. A
ramp that is trivial in a thermocycler block is a genuine engineering specification at
hundreds of litres.

## 9. Impurity fate
Forms: none chemically. Determines: duplex content and strand ratio. Passes through: all
impurities present in either strand, which is why strand release testing before annealing
matters. There is no purification step after this point that removes a sequence impurity.

## 10. Failure modes
RSK-080 strand ratio deviation, RSK-081 incomplete annealing, RSK-082 temperature
non-uniformity, RSK-083 concentration assay error propagated from UO-07.

## 11. Cleaning, changeover and containment
Standard aqueous cleaning. This is the first point at which both strands are present, so
cross-contamination control between products matters differently here.

## 12. Environmental and utility load
Heating and cooling duty. Modest.

## 13. Open questions
OQ-015.

## 14. References
[TBD]
