# Process development (Tier 3 — sketch)

Full development strategy is Tier 3. The Tier-1 point is what breaks first on scale-up and where
small scale misleads.

## What must be characterised first

- **Duplex Tm** for our sequence (Q-030) — gates the spray-dryer outlet temperature.
- **Ligation conversion and side-reaction profile** at scale for our modified 21-mer (Q-010) —
  the largest real public scale today is ~1 L.
- **Block full-length purity** and its propagation (Q-011) — sets the purity floor.
- **Immobilised-enzyme clearance** (Q-032) — the filtration-led linchpin.

## Where small scale misleads

- **Spray drying:** the outlet/particle temperature relationship, cyclone/wall losses, and
  morphology are notoriously unrepresentative at bench scale — qualify at **pilot** scale.
- **Evaporation:** residence-time distribution and fouling/viscosity limits do not scale down
  cleanly. **A rotary evaporator is not a scale-down model of a falling film**: a falling film has a
  minimum wetting rate below which it breaks into rivulets and fouls, so a small batch must recirculate
  and multiply thermal exposure (<span class="prov-fact">fact</span>;
  [SRC-HUGHES-2024](../registers/sources.md), R-013, R-004).
- **UF/DF:** flux, fouling, and hold-up losses scale by area/shear rules, not by simple volume. Yield
  is an equation, not a "<10%" rule (`EQ-UFYIELD`), and its dominant term at small batch is
  unrecoverable hold-up, not membrane passage.

## Mass-balance discipline the site must apply

Do not track yield alone. To know where product goes, calculate a **mass balance across every UF/DF
step**: total product in the retentate, in the filtrate, **and** in the unrecoverable hold-up volume
(<span class="prov-fact">fact</span>; [SRC-MILLIPORE-TFF](../registers/sources.md)). Hold-up is where
the loss hides — 30–40% of a nucleic acid can remain in tubing and filters at small scale
(<span class="prov-fact">fact</span>, mRNA; [SRC-NOURAFKAN-2024](../registers/sources.md)), and it is
not captured by a retention coefficient. Membrane-passage loss itself swings tenfold (9.5% at R=0.99,
1.0% at R=0.999), so the retention target is a real development decision, not a rounding choice.

## Scale-down models to qualify

Representative scale-down for UF/DF (constant wall shear, loading, diavolumes, TMP), for
evaporation (residence time and film temperature), and for spray drying (outlet temperature,
atomisation, drying gas ratio). Each must be qualified against pilot data before it is trusted.
