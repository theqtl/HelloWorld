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

### Concentration basis (stated explicitly, because it differs across the train)

- Ligation and ultrafiltration concentrations are on an **siRNA basis**, matching the cited
  literature, which reports siRNA concentrations rather than total solids.
- The evaporator outlet concentration is on a **total dissolved solids basis**, because a viscosity
  limit constrains everything in solution, not only the active.
- How much excipient is in solution *at the evaporator* is a process choice, not a constant, so it is
  carried explicitly as `P-EXCIP-FRAC-PRE-EVAP`: 0 means the bulk excipient is added after
  evaporation (the base case), 1 means the full load is present from the final diafiltration.
  Risk R-005 requires the salts to be exchanged **out** at the final diafiltration; it does not
  require the excipient load to go **in** there. See Q-038.

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
already concentrates: charged membranes raised achievable siRNA concentration from 52 to
**>180 mg/mL** at bench scale (<span class="prov-fact">fact</span>;
[SRC-ZYDNEY-2024](../registers/sources.md)). If UF reaches
close to the dryer-feed solids, evaporation duty is small; if viscosity limits UF earlier,
evaporation carries more. The cascade `P-CONC-UF → P-CONC-EVAP → P-CONC-DRYFEED` is therefore
explicit and adjustable, not assumed away. Questions Q-017/Q-018/Q-019 hold the real limits.

## Where evaporation earns its place

The excipient decision is not a detail — it largely decides whether there is any evaporation duty at
all. Holding everything else at the current placeholders and varying only that one input:

| Excipient in solution at the evaporator | Evaporator outlet solids (kg) | Water removed (L) | Duty (MJ) |
|---|---|---|---|
| none (base case, added after evaporation) | 28.3 | 115.5 | 277.1 |
| half | 42.5 | 68.2 | 163.8 |
| all (added at final diafiltration) | 56.7 | 21.0 | 50.4 |

*(Per campaign, scenario S1. Figures regenerate from the data layer; the inputs are illustrative
assumptions, not validated values.)*

A five-fold swing in duty from one unresolved process choice. And it compounds with Q-017: if
ultrafiltration alone reaches close to the dryer feed solids, evaporation has little left to do
regardless. Evaporation is a fixed decision for this train, so the question is not *whether* it
happens but *where it earns its place* — which is answered by resolving Q-017, Q-018 and Q-038, not
by arithmetic on placeholders.

## What the balance does not yet do

- Species-resolved impurity tracking (n-1, partials) per stream — Tier 2.
- Full energy balance with sensible heat and gas loads — Tier 2.
- Buffer salt mass carried into the powder — depends on the final-matrix design (R-005).

See the [generated results](results.md).
