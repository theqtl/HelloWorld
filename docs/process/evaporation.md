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
| MVR (drive) | n/a (a drive) | n/a | n/a | ~15–25 kWh/ton water; minimal live steam | **energy drive at high throughput** |
| Flash | very short | low | limited concentration per stage | low | limited single-stage duty |

Sources: [SRC-FFE-WIKI](../registers/sources.md), [SRC-POPE-FFE](../registers/sources.md),
[SRC-SPX-MVR](../registers/sources.md) (<span class="prov-fact">fact</span>, general/food/vendor).

## Recommendation

**Falling-film evaporator under vacuum, MVR-driven at higher throughput, with a wiped/thin-film
fallback if viscosity or fouling become limiting** (<span class="prov-inference">inference</span>):

- Falling-film residence time is **seconds** and the film is 0.2–2 mm, giving high heat transfer
  and minimal thermal exposure — it concentrates thermosensitive streams (milk, juice, pharma)
  without decomposition. This protects the duplex.
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

!!! warning "Transferability & open question"
    Evaporator correlations are largely from food, dairy, and fine chemicals; evaporation of an
    oligonucleotide duplex is not a documented precedent (transferability caveat). Whether
    evaporation is even needed depends on how far UF concentrates first — if UF reaches near the
    dryer-feed solids (>190 g/L is achievable at bench), evaporation duty is small (Q-017, the
    concentration cascade).
