# Risk assessment method

> **[SEED]**

## Framework

ICH Q9 quality risk management. The register in `risk-register.csv` is a process FMEA in
tabular form, with severity, likelihood, and detectability assessed per row.

## Scales

Define numeric scales before the first formal assessment session, and keep them fixed
thereafter. Changing a scale mid-assessment invalidates comparison between rows. **[TBD]**

## Practice notes

1. **Detectability is where most FMEAs go wrong.** A risk that is detected only at final
   release, after the material is committed, is poorly detectable regardless of how good the
   assay is. Rate detection by when it is detected, not by how accurately.
2. **Score the current state, then the mitigated state.** A register that only records the
   post-mitigation score hides whether the mitigation has actually been implemented.
3. **Link every row to a unit operation and a CQA**, or it cannot be traced into the control
   strategy.
4. **Risks without owners do not get closed.** The owner column is not optional.

## Highest risks on current understanding

These carry HIGH severity and warrant attention before design freeze:

| Risk | Why it leads |
|---|---|
| RSK-040 and RSK-050 | Chromatographic resolution at scale is the core technical risk of the whole process |
| RSK-043 | Ultraviolet-based pooling cannot see the impurity it needs to exclude |
| RSK-052 | Ion-pair modifier supply and regulatory exposure could invalidate the purification design |
| RSK-113 | A conservative lyophilisation cycle silently consumes facility capacity every batch |
| RSK-200 | If no viable ligation junction exists, the chemoenzymatic route is closed entirely |
| RSK-300 | Amidite supply drives both schedule and cost of goods |
| RSK-302 | Hazardous area scope recognised late is the classic greenfield capital overrun |
