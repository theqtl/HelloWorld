# Mass & energy balance — method

The balance is **executable**. It is a Python module (`gen/balance.py`) that reads every input
from the [parameter register](../registers/parameters.md) and computes stream flows, water and
buffer volumes, waste, and thermal duties for each [throughput scenario](../registers/questions.md).
The [results page](results.md) is generated from it; change the CSV inputs, run
`python -m gen.build`, and every figure updates.

!!! danger "Read this before using any number"
    Most balance inputs are flagged **assumption** — illustrative placeholders registered as open
    questions, not validated values. The module **refuses to run on a blank input** (it raises
    rather than inventing one), so a gap can never silently become a fabricated result. The
    throughput scenarios themselves are illustrative (Q-002).

## Boundary and basis

- **Boundary:** received purified, 5'-phosphorylated blocks → ligation → clarification →
  UF/DF → evaporation → spray drying → DS powder. Fully aqueous, no solvents.
- **Basis:** DS demand is taken as siRNA **active** mass (API). The powder additionally carries
  excipient at the ratio `P-EXCIPIENT-RATIO`.
- **Per campaign** = annual demand ÷ campaigns per year.

## The chain

1. **Overall yield** \(Y = Y_\text{lig}\,Y_\text{UFDF}\,Y_\text{evap}\,Y_\text{dry}\).
2. **API required at ligation** = DS API per campaign ÷ \(Y\).
3. **Volumes** at each stage from the stage concentration: ligation at `P-CONC-LIG`,
   UF retentate at `P-CONC-UF`, evaporator outlet at `P-CONC-EVAP`, dryer feed solids at
   `P-CONC-DRYFEED`.
4. **Diafiltration buffer** = diavolumes × UF retentate volume (dominant clean-water and aqueous-waste driver).
5. **Water removed in evaporation** = UF volume − evaporator outlet volume.
6. **Dryer water** = dryer feed mass − solids (API + excipient).
7. **Thermal duty** = mass of water removed × latent heat (`P-H2O-LHV`). This is the
   latent-heat **minimum**; the real duty adds sensible heat, gas heating, and losses (Tier-2).

## Concentration cascade (why evaporation duty is scenario-dependent)

The hand-off concentrations decide how much work evaporation actually does. Ultrafiltration
already concentrates: charged-membrane siRNA has reached >190 g/L at bench scale
(<span class="prov-fact">fact</span>; [SRC-ZYDNEY-2024](../registers/sources.md)). If UF reaches
close to the dryer-feed solids, evaporation duty is small; if viscosity limits UF earlier,
evaporation carries more. The cascade `P-CONC-UF → P-CONC-EVAP → P-CONC-DRYFEED` is therefore
explicit and adjustable, not assumed away. Questions Q-017/Q-018/Q-019 hold the real limits.

## What the balance does not yet do

- Species-resolved impurity tracking (n-1, partials) per stream — Tier 2.
- Full energy balance with sensible heat and gas loads — Tier 2.
- Buffer salt mass carried into the powder — depends on the final-matrix design (R-005).

See the [generated results](results.md).
