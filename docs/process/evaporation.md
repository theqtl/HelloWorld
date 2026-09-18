# Evaporation

Evaporation concentrates the aqueous stream toward the dryer feed. That evaporation happens is
fixed; the type is open. The design task is to concentrate a heat- and shear-sensitive duplex
without degrading it.

## Type selection

| Type | Residence time | Thermal-damage risk | Fouling / viscosity | Energy | Fit here |
|---|---|---|---|---|---|
| **Falling film** | seconds | low | low pressure drop; struggles at high viscosity | good; pairs with MVR | **Recommended primary** |
| Wiped / agitated thin film | seconds | low | handles high viscosity/fouling (active wiping) | moderate | **Fallback** for viscosity/fouling |
| Thin film | seconds | low | moderate | moderate | alternative |
| Forced circulation | longer | higher (longer exposure) | robust to fouling/crystallisation | moderate | avoid (long residence) |
| MVR (drive) | n/a (a drive) | n/a | n/a | ~15–25 kWh/ton water general industrial; ~10–12.5 kWh/ton in dairy practice; minimal live steam | **energy drive at high throughput** |
| Flash | very short | low | limited concentration per stage | low | limited single-stage duty |

Sources: [SRC-FFE-WIKI](../registers/sources.md), [SRC-POPE-FFE](../registers/sources.md),
[SRC-SPX-MVR](../registers/sources.md) (qualitative only — "very low; little or no steam required"),
with the recompression energy figure from [SRC-EFSAN-MVR](../registers/sources.md) and the lower
dairy figure from [SRC-TETRAPAK-DPH](../registers/sources.md)
(<span class="prov-fact">fact</span>, general/food/vendor). Recompression energy is strongly
application-dependent, so treat the range as indicative until it is computed for this duty.

## The oligonucleotide precedent (this is no longer a "no data" step)

Thin-film evaporation of an oligonucleotide drug substance is **established practice**, not an analogy
to dairy. The maximum concentration achieved in manufacture by thin-film evaporation is **160 mg
ASO/g solution**, and the authors note that thin-film evaporation is likely to reach higher
concentrations than UF/DF because more viscous liquids are less likely to foul the evaporator
(<span class="prov-fact">fact</span>; [SRC-PMC7415879](../registers/sources.md)). Two caveats travel
with it: the source is a **single-strand antisense** oligonucleotide solution, not an siRNA duplex and
not a dryer feed; and its stated "few hours" is a **batch cycle time, not a fluid residence time** —
do not cite it as a residence time. This anchors `P-CONC-EVAP` (Q-018).

## Recommendation

**Falling-film evaporator under vacuum, MVR-driven at higher throughput, with a wiped/thin-film
fallback if viscosity or fouling become limiting** (<span class="prov-inference">inference</span>):

- Falling-film residence time is **seconds** ([SRC-FFE-WIKI](../registers/sources.md)) and the film
  runs **0.2–2 mm** thick ([SRC-MEDINA-2022](../registers/sources.md)), giving high heat transfer and
  minimal thermal exposure — it concentrates thermosensitive streams (milk, juice, pharma) without
  decomposition. This protects the duplex.
- Run under **vacuum** so the boiling temperature stays well below the duplex melting temperature
  (Tm, gap Q-030); boiling-point elevation rises as solutes concentrate (`EQ-EVAP`).
- **MVR** recompresses and reuses the vapour, cutting live steam — the energy-efficient drive when
  water duty is large.
- Switch to **wiped/thin film** if the stream fouls or gets too viscous near the target
  concentration; **avoid forced circulation** (longer residence raises degradation risk).

## Duty and sizing

Minimum duty \(Q_{\min} = \dot m_\text{water}\,\lambda\) with \(\lambda\) ≈ 2400 kJ/kg at reduced
pressure; area from \(Q = U A \Delta T_\text{lm}\) (`EQ-EVAP`). Water removed per campaign is in the
[balance results](../balance/results.md). The overall heat-transfer coefficient \(U\) for this
stream, the maximum concentration before the viscosity limit, and foaming behaviour are **gaps**
(Q-018).

**Turndown, not just duty, constrains a falling film (risk R-013).** A falling film needs a minimum
feed per unit tube perimeter — the **minimum wetting rate**, reported at 0.10–0.22 kg m⁻¹ s⁻¹ for
water on vertical steel (<span class="prov-fact">fact</span>, water/simple aqueous solutions;
[SRC-HUGHES-2024](../registers/sources.md)). Below it the film breaks into rivulets and dry patches
foul — a heat-transfer failure, not a throughput inconvenience. For a single 48 mm tube the wetted
perimeter is 0.151 m, so the minimum feed is about 57 kg/h **for one tube**
(<span class="prov-inference">inference</span>, arithmetic ours). A small pharmaceutical batch
therefore cannot run single-pass; it must recirculate, and recirculation multiplies cumulative
thermal exposure — the quantity R-004 is about. **A rotary evaporator is not a scale-down model of a
falling film.** These numbers are for water, not a polyelectrolyte solution, so the transfer is
plausible but unproven.

!!! warning "Transferability & open question"
    Evaporator hydrodynamic correlations are largely from food, dairy, and fine chemicals. Thin-film
    evaporation of an oligonucleotide drug substance **is** a documented precedent
    ([SRC-PMC7415879](../registers/sources.md)), but for a single-strand ASO solution, not an siRNA
    duplex, so the transferability caveat still applies. Whether evaporation is even needed depends on
    how far UF concentrates first — if UF reaches near the dryer-feed solids (~193 g/L is achievable at
    bench; [SRC-ZYDNEY-2025](../registers/sources.md)), evaporation duty is small (Q-017, the
    concentration cascade).
