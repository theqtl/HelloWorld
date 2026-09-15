# Greenfield facility design basis

> **[SEED]**. This is the skeleton of the Basis of Design. It must not be filled in until
> the demand scenarios in `01-product/qtpp.md` are bracketed, because every number below
> derives from them.

## 1. Design basis inputs

| Input | Source | Status |
|---|---|---|
| Annual demand, three scenarios | QTPP | **[TBD]** OQ-001 |
| Batch size and campaign structure | QTPP, mass balance | **[TBD]** OQ-003 |
| Number of products, single or multi-product | Business | **[TBD]** OQ-009 |
| Clinical or commercial or both | Business | **[TBD]** |
| Route, synthetic or chemoenzymatic | Decision record | **[TBD]** |
| Drug substance form, solid or frozen liquid | QTPP | **[TBD]** OQ-018 |
| Sterile or low-bioburden drug substance | Quality | **[TBD]** OQ-017 |

**Nothing downstream of this table can be designed until it is filled in.** A design that
proceeds on assumed values should record them in the assumptions register so that the
rework scope is known when the real numbers arrive.

## 2. What makes an oligonucleotide facility different

A team coming from biologics will find the following unfamiliar, and each has significant
capital consequence:

1. **Large flammable solvent inventory and throughput.** Synthesis and ion-pair reverse
   phase purification both consume solvent at a scale that puts substantial areas into
   hazardous electrical classification, with the associated equipment, ventilation,
   drainage, and fire protection cost. This is usually the largest single driver of
   difference from a biologics facility.
2. **No bioreactor, no cell culture, no viral clearance.** The upstream half of a biologics
   facility simply is not present, and the contamination control strategy is
   correspondingly different.
3. **Chromatography sized by resolution, not capacity.** Column volumes are larger than a
   binding-capacity calculation would suggest.
4. **Buffer volumes that can dominate the tank farm.** In-line dilution or formulation
   should be evaluated early.
5. **Solvent recovery as a core process, not a utility afterthought.**
6. **Lyophilisation as a potential capacity bottleneck**, with multi-day cycles.

## 3. Area concept

| Area | Function | Classification driver | Notes |
|---|---|---|---|
| Solvent storage and distribution | Bulk solvent | Hazardous area | External or dedicated, bunded |
| Synthesis suite | Solid-phase synthesis | Hazardous area, GMP | Highest solvent duty |
| Deprotection | UO-01 | Amine and fluoride handling | Scrubbed, local exhaust |
| Aqueous purification | UO-02, UO-03, UO-04, UO-07 | GMP, non-hazardous | Largest buffer demand |
| Organic purification | UO-05 | **Hazardous area, GMP** | The expensive room |
| Annealing and formulation | UO-08, UO-09 | GMP, higher grade | Both strands present |
| Filtration and filling | UO-10, UO-12 | Classification per OQ-017 | |
| Lyophilisation | UO-11 | Classification per OQ-017 | Large footprint, heavy utilities |
| Quality control laboratories | Analytics | Laboratory | Chromatography and MS heavy |
| Warehouse and cold storage | Materials and DS | Controlled | Backup power required |
| Solvent recovery | Utility | Hazardous area | Decide in concept design |
| Effluent treatment | Utility | Per stream | Salt, solvent, fluoride, amine |

## 4. Standards and references

ISPE Baseline Guides for facility concept, ASTM E2500 for verification, GAMP 5 for
computerised systems, EU GMP Annex 15 for qualification, ICH Q7 for API GMP. Local building,
fire, and environmental codes govern the hazardous area design and are jurisdiction-specific,
so site selection should precede detailed design. **[SEED]**

## 5. Expansion

Greenfield facilities are almost always expanded sooner than planned. Identify, at concept
stage, which capacity is cheapest to add later. On current understanding that is
**lyophilisation and chromatography**, both of which can be added as parallel trains if
space and utility headroom are reserved. Reserving that headroom is inexpensive at design
and very expensive to retrofit. **[SEED]**
