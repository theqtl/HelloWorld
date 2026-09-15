# Process overview

> **[SEED]**. Block flow shown for the base case. Route decision is open, see
> `10-decisions/decision-log.md`.

## Block flow, base case fully synthetic route

```
   SENSE STRAND TRAIN                    ANTISENSE STRAND TRAIN
   ------------------                    ----------------------
   Solid-phase synthesis                 Solid-phase synthesis
           |                                      |
   UO-01 Cleavage and deprotection        UO-01 Cleavage and deprotection
           |                                      |
   UO-02 Clarification                    UO-02 Clarification
           |                                      |
   UO-03 Initial UF/DF                    UO-03 Initial UF/DF
           |                                      |
   UO-04 Capture chromatography (AEX)     UO-04 Capture chromatography (AEX)
           |                                      |
   UO-05 Polish chromatography (IP-RP)    UO-05 Polish chromatography (IP-RP)
           |                                      |
   UO-06 Detritylation, if DMT-on         UO-06 Detritylation, if DMT-on
           |                                      |
   UO-07 Desalt and counterion exchange   UO-07 Desalt and counterion exchange
           |                                      |
           +------------------+-------------------+
                              |
                    UO-08 Annealing to duplex
                              |
                    UO-09 Final UF/DF and formulation
                              |
                    UO-10 Sterile filtration
                              |
                    UO-11 Lyophilisation, if applicable
                              |
                    UO-12 Drug substance packaging and storage
```

## Chemoenzymatic route variant

If the blockmer plus enzymatic ligation route is selected, insert into each strand train,
before UO-02:

```
   Block synthesis (multiple short blocks)
           |
   Block cleavage, deprotection, purification    <- each block purified separately
           |
   5' phosphorylation, where not installed chemically
           |
   UO-L1 Splinted enzymatic ligation
           |
   UO-L2 Splint digestion and protein clearance
```

This variant adds two unit operations per strand, one chromatographic burden for protein
and splint clearance, and a per-block purification obligation that partly offsets the
simpler full-length purification. See `03-process/upstream/enzymatic-ligation.md`.

## Where the difficulty concentrates

| Step | Why it is hard |
|---|---|
| UO-04 and UO-05 | Resolving n-1, n+1, and PO impurities from product. Determines yield, purity, and cost of goods simultaneously |
| UO-08 | Strand ratio must be controlled tightly, and the assay to confirm duplex content is not trivial at release |
| UO-11 | Long cycles on a high-value material, with a large facility footprint |
| Solvent handling throughout | Drives area classification, recovery, and permitting more than any GMP consideration |

## Mass balance

`[TBD]` A mass balance model should be built as soon as batch size is bracketed. Suggested
as a spreadsheet in this repository with the step yields taken from the UO entries so that
the model and the process description cannot diverge. Tracked as OQ-003.
