# PAT options by unit operation

> **[SEED]**. Placement conventions: **in-line** means the sensor is in the process stream,
> **on-line** means an automated sample loop returns to the stream, **at-line** means a
> sample is taken and measured nearby, **off-line** means the laboratory.

## Options by step

| UO | Technique | Placement | Measures | Decision enabled | Maturity |
|---|---|---|---|---|---|
| UO-01 | Temperature, pressure | In-line | Reaction conditions | Cycle control | Routine |
| UO-01 | LC-MS or IP-RP | At-line | Deprotection completeness | Release to next step | Routine |
| UO-02 | Turbidity, differential pressure | In-line | Filtration health | Filter change | Routine |
| UO-02 | UV at 260 nm on flush | In-line | Product recovery | Flush endpoint | Routine |
| UO-03 | Conductivity, pH | In-line | Diafiltration progress | Endpoint | Routine |
| UO-03 | Variable pathlength UV | In-line | Concentration | Concentration endpoint | Established |
| UO-03 | Permeate UV | In-line | Product breakthrough | Membrane integrity | Routine |
| UO-04 | Multi-wavelength UV | In-line | Elution profile | Pooling | Routine |
| UO-04 | Conductivity, pH | In-line | Gradient verification | Step confirmation | Routine |
| UO-04 | **On-line or at-line UPLC** | At-line | Fraction purity | **Purity-based pooling** | Established, high value |
| UO-04 | HETP and asymmetry testing | Between cycles | Column health | Repack trigger | Routine |
| UO-05 | Multi-wavelength UV | In-line | Elution profile | Pooling | Routine |
| UO-05 | **On-line or at-line UPLC** | At-line | Fraction purity | **Purity-based pooling** | Established, high value |
| UO-05 | On-line MS | On-line | Identity, impurity identity | Pool confirmation | Emerging |
| UO-06 | pH | In-line | Reaction condition | Quench timing | Routine |
| UO-06 | Visible absorbance of trityl cation | In-line | Reaction progress | Endpoint | Established, cheap |
| UO-07 | Conductivity | In-line | Diafiltration progress | Endpoint | Routine |
| UO-07 | Variable pathlength UV | In-line | Concentration | **Feeds strand ratio at UO-08** | Established, high value |
| UO-07 | Ion chromatography | At-line | Counterion | CQA-12 | Routine |
| UO-07 | Headspace GC | At-line | Residual solvent | CQA-13 | Routine |
| UO-08 | Multi-point temperature | In-line | Ramp uniformity | Cycle control | Routine |
| UO-08 | Non-denaturing AEX, SEC, or CGE | At-line | Duplex content | **Anneal confirmation** | Established, high value |
| UO-08 | UV thermal melting | At-line | Duplex identity and stability | Confirmation | Routine |
| UO-09 | Conductivity, variable pathlength UV | In-line | Matrix and concentration | Endpoint | Routine |
| UO-10 | Pressure, integrity test | In-line | Filter integrity | Release | Routine |
| UO-11 | Product temperature probes | In-line | Product temperature history | Primary drying control | Routine |
| UO-11 | **Pirani versus capacitance comparison** | In-line | Sublimation endpoint | **Cycle endpoint, not fixed time** | Established, high value |
| UO-11 | Tunable diode laser absorption spectroscopy | In-line | Sublimation rate | Cycle optimisation and endpoint | Established |
| UO-11 | Near infrared | At-line or in-line | Residual moisture | Secondary drying endpoint | Established |
| UO-12 | Environmental monitoring, humidity | In-line | Handling environment | Release of operation | Routine |

## Where PAT actually pays here

Three opportunities are worth real investment, and the rest are conventional instrumentation.

1. **Purity-based pooling at UO-04 and UO-05.** Ultraviolet absorbance cannot distinguish
   n-1 from full-length product. Pooling on ultraviolet signal alone therefore forces
   conservative cut points, and that conservatism costs yield on every single batch of the
   facility's life. At-line chromatography that returns a purity result fast enough to drive
   the cut is the highest-value measurement in this process.
2. **Lyophilisation endpoint detection at UO-11.** On a cycle measured in days, ending
   primary drying on a measured endpoint rather than a validated fixed time converts
   directly into facility capacity. Comparative pressure measurement is the cheapest route
   and is well established.
3. **Concentration accuracy at UO-07.** The strand ratio control point for annealing is
   really the concentration assay at the end of desalting. In-line variable pathlength
   ultraviolet removes the dilution step that is the main error source in an off-line assay.

## Real-time release

Full real-time release for this drug substance is not a realistic near-term target, mainly
because duplex content, sequence identity, and microbial attributes are not measurable
in-line today. **[SEED]** A more achievable goal is parametric control of individual steps
plus reduced end-product testing, and the control strategy should be written to that
ambition rather than to an aspirational one. Tracked as OQ-021.
