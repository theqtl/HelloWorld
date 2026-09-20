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

1. **Overall yield** \(Y = Y_\text{lig}\,Y_\text{UFDF}\,Y_\text{evap}\,Y_\text{dry}\). The UF/DF term
   is **not a flat constant**: it is computed from product retention, the concentration factor, the
   diavolumes and two additive loss terms (hold-up and adsorption) via `EQ-UFYIELD`
   ([SRC-MILLIPORE-TFF](../registers/sources.md), [SRC-NOURAFKAN-2024](../registers/sources.md)). The
   dryer term is a **band** (61–89% optimised, 8.6–22% unoptimised; `P-YLD-DRY`,
   [SRC-KAPIL-2025](../registers/sources.md)) carried at a representative point.
2. **API required at ligation** = DS API per campaign ÷ \(Y\).
3. **Volumes** at each stage from the stage concentration: ligation at `P-CONC-LIG`,
   UF retentate at `P-CONC-UF`, evaporator outlet at `P-CONC-EVAP`, dryer feed solids at
   `P-CONC-DRYFEED`. The retentate is sized on the API that **survives** UF/DF, not on the API
   entering it — sizing it on the inlet described a volume that never exists in the process and
   overstated the evaporator feed and duty by \(1/Y_\text{UF/DF}\).
4. **Diafiltration buffer** = diavolumes × UF retentate volume (dominant clean-water and aqueous-waste driver).
5. **Water removed in evaporation** = retentate volume − evaporator outlet volume. If ultrafiltration
   already meets the evaporator target this is zero, the unit is bypassed, and it carries no duty.
6. **Dryer water** = dryer feed mass − solids (API + excipient).
7. **Thermal duty** (`EQ-ENERGY`). The **latent-heat minimum** — mass of water removed × latent heat
   (`P-H2O-LHV`) — is reported as a strict floor, and every term added to it is non-negative, so that
   ordering holds by construction rather than by luck with the placeholders. The **evaporator** raises
   the feed *mass* (volume × `P-SOLN-DENSITY`) from `P-EVAP-T-FEED` to the vacuum boiling point
   `P-EVAP-T-BOIL` at `P-CP-SOLN`, then evaporates, plus one `P-HEAT-LOSS-FRAC` uplift. The **dryer**
   reports **two different quantities**: the *process* duty (evaporate the water, raise the feed to
   `P-DRY-T-OUT`, plus losses) and the *heater* duty, which is the utility load — inlet gas heated from
   `P-DRY-T-AMBIENT` to `P-DRY-T-IN`, exactly what `UT-DRYGAS` is. The drying-gas mass is **derived**
   from the process duty, not assumed, so no gas:water ratio is carried and nothing is tuned. An
   impossible operating point (inlet below outlet, ambient above outlet) **raises** rather than
   reporting a silent zero. Temperatures and the density are assumptions (Q-045, Q-046); MVR recovers
   most of the evaporator latent load.

!!! warning "Conversion is not yield"
    Per-ligation conversion and overall mass yield are **different quantities, an order of magnitude
    apart**. Measured per-ligation conversion on modified siRNA blocks is >92% (`P-LIG-CONV`;
    [SRC-CN119265174](../registers/sources.md)), but published **overall campaign** mass yields for
    kilogram-scale ligation-built siRNA are **19–43%** (`P-YIELD-OVERALL-PUB`;
    [SRC-HONGENE-BROCHURE-2025](../registers/sources.md)) — a conservative figure, unoptimised and
    calculated from the lowest-yielding fragment. A balance that read a >92% conversion as a step yield
    would overstate drug substance several-fold. The balance's own step-yield product is a different
    construction again and is not directly comparable to the vendor's 19–43% definition.

## Concentration cascade (why evaporation duty is scenario-dependent)

The hand-off concentrations decide how much work evaporation actually does. Ultrafiltration
already concentrates: charged membranes raised achievable siRNA concentration from 52 to
**>180 mg/mL**, and to **~193 g/L** in the ligand-density follow-up
(<span class="prov-fact">fact</span>, bench; [SRC-ZYDNEY-2024](../registers/sources.md),
[SRC-ZYDNEY-2025](../registers/sources.md)). The evaporator outlet is now anchored to a real achieved
concentration, **160 mg ASO/g** by thin-film evaporation (<span class="prov-fact">fact</span>,
single-strand ASO; [SRC-PMC7415879](../registers/sources.md), `P-CONC-EVAP`). That anchor sits only
just above the placeholder UF ceiling of 150 g/L, which sharpens the cascade point: if UF alone
reaches the evaporator target, evaporation has little left to do. The cascade
`P-CONC-UF → P-CONC-EVAP → P-CONC-DRYFEED` is therefore explicit and adjustable, not assumed away.
Questions Q-017/Q-018/Q-019 hold the real limits.

## Where evaporation earns its place

The excipient decision is not a detail — it largely decides whether there is any evaporation duty at
all. That sensitivity is **computed, not transcribed**: see the *Where evaporation earns its place*
table on the [results page](results.md), which varies `P-EXCIP-FRAC-PRE-EVAP` and holds everything
else at the current placeholders.

(The figures used to be typed into this page by hand and had already drifted away from the model —
claiming 66.2 L and 158.8 MJ against the model's own output. They are generated now, so they cannot
drift again.)

With the evaporator outlet anchored just above the UF ceiling, evaporation carries only a modest duty
in the base case and **none at all once excipient is added upstream** — the retentate already sits at
or above the evaporator target, so there is nothing to remove and the unit is bypassed. That is the
concentration-cascade point made concrete: whether evaporation earns its place is decided by resolving
Q-017 (how far UF concentrates), Q-018 (the real evaporator ceiling) and Q-038 (where excipient
enters), not by arithmetic on placeholders. Evaporation is a fixed decision for this train, so the
question is not *whether* it happens but *where it earns its place*.

## What the balance does not yet do

- Buffer salt mass carried into the powder — depends on the final-matrix design (R-005).

See the [generated results](results.md).
