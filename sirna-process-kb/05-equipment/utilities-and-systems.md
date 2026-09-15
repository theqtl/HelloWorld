# Utilities and systems

> **[SEED]**. Loads cannot be quantified until batch size is bracketed, see OQ-001.

| System | Driven by | Design note |
|---|---|---|
| Purified water and water for injection | Buffer preparation, diafiltration, cleaning | Specify grade per step. Over-specifying WFI everywhere is a common and expensive error |
| Clean steam | Sterilisation, where applicable | Scope depends on OQ-017 sterile versus low-bioburden |
| Process nitrogen | Blanketing, solvent transfer, drying | Flammable solvent handling makes this safety-critical, not just a utility |
| Compressed dry air | Instrumentation, actuation | |
| Chilled water and glycol | Column temperature control, annealing ramp, lyophiliser | Annealing and lyophilisation drive the low-temperature duty |
| Heating | Deprotection, drying | |
| Vacuum | Lyophilisation | Sustained duty over multi-day cycles |
| HVAC | Classification, solvent areas, containment | Solvent areas may require once-through rather than recirculated air, which is a major energy cost |
| Solvent storage and distribution | Synthesis and IP-RP | Tank farm, bunding, transfer, and area classification |
| Solvent recovery | Acetonitrile volume | Decide in concept design. See EQ-201 |
| Effluent treatment | Salt, solvent, amine, fluoride streams | Perchlorate, fluoride, and fluorinated compounds each carry specific obligations |
| Emergency and backup power | Cold storage, lyophilisers in cycle, safety systems | A power loss mid-lyophilisation cycle can destroy a batch worth more than the generator |
| Building management and data historian | GMP data, PAT integration | GAMP 5 and data integrity requirements apply |

## Utility loads worth flagging early

Three loads routinely surprise greenfield teams designing oligonucleotide facilities:

1. **Buffer preparation and hold volume**, driven by anion exchange. In-line buffer
   dilution or formulation should be evaluated before the tank farm is sized.
2. **Once-through HVAC in flammable solvent areas**, which can dominate facility energy.
3. **Sustained vacuum and refrigeration for multi-day lyophilisation cycles.**
