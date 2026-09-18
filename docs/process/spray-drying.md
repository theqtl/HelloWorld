# Spray drying

Spray drying produces the DS powder. That spray drying happens is fixed (lyophilisation cannot
meet throughput). The [duplex-survival finding](../findings/spray-drying.md) holds the argument;
this page holds the configuration.

## Configuration recommendation

**Dry the annealed duplex in an amorphous trehalose glass, at an outlet temperature below the
duplex melting temperature and comfortably below the moisture-adjusted glass transition, under
low-oxygen (N₂) drying** (<span class="prov-inference">inference</span>, grounded):

| Choice | Recommendation | Basis |
|---|---|---|
| Product form | Duplex (fallback: dry strands separately, anneal after) | ligation co-assembles the duplex; Q-001 |
| Matrix | Trehalose (or sucrose) amorphous glass | full siRNA recovery vs 20% loss for mannitol ([SRC-KEIL-2021](../registers/sources.md)) |
| Excipient role | a **drying / powder-property aid**, not a chemical stabiliser | approved siRNA products are stable at 160–200 mg/mL in near-pure water and four of seven carry no weighed excipient ([SRC-SIRNA-LABELS](../registers/sources.md)); Q-021 |
| Residual moisture (binding limit) | as low as achievable; measured 3.8–4.6% gives Tg 38–53 °C | keep powder below moisture-shifted Tg ([SRC-KEIL-2021](../registers/sources.md), `EQ-TG`, Q-039) |
| Outlet temperature (looser limit) | below duplex Tm (58–64 °C); particle stays near wet-bulb while wet | integrity preserved when T-out < Tm ([SRC-KEIL-2021](../registers/sources.md), [SRC-MALEK-2019](../registers/sources.md)) |
| Atomiser | to be selected (rotary vs two-fluid vs pressure) | atomisation shear is not a governing risk for a short duplex ([SRC-NAKED-NA-2023](../registers/sources.md)); trade droplet size against morphology |
| Gas | N₂, low O₂ | limit oxidation of oligo; inference |

## Atomiser, morphology, yield

Particle morphology follows the Péclet number (`EQ-PECLET`, from
[SRC-VEHRING-2008](../registers/sources.md)): high Pe → surface enrichment → hollow, dimpled or
wrinkled particles; low Pe → dense particles near true density. Note that
[SRC-SD-MORPH](../registers/sources.md) qualifies a purely Péclet-based reading, concluding that
solute crystallisation kinetics also dictate shell formation and that inlet temperature alone is an
insufficient predictor. Atomiser choice trades droplet size against morphology; atomisation shear is
**not** a governing risk for a short duplex, which survives it intact
([SRC-NAKED-NA-2023](../registers/sources.md)) even though it is a real risk for a large flexible
molecule such as plasmid DNA. Cyclone and wall losses set yield at scale, and that yield is a **band,
not a point**: measured spray-dryer recoveries run 8.6–22% unoptimised and 61–89% optimised across
5–400 g (<span class="prov-fact">fact</span>, sticky small molecule; [SRC-KAPIL-2025](../registers/sources.md),
`P-YLD-DRY`, Q-012), with optimised conditions transferring between scales and unoptimised ones not.
Containment and dryer sanitisation for low-bioburden operation are demanding and Tier-2 (risk R-008),
and a dried organic powder brings dust-explosion controls into scope (risk R-016).

## The buffer constraint

The feed must already be in a spray-dry-compatible matrix (excipient + minimal/volatile salts);
otherwise non-volatile buffer salts end up in the powder (risk R-005). This is set at the final
diafiltration, not here.

## The DoE that resolves the risk

Measure the modified-duplex **Tm** (Q-030), then map retained duplex fraction and activity against
outlet temperature, excipient:API ratio, and residual moisture, at **pilot scale** where the
outlet/particle temperature relationship is representative (bench under-represents it).

!!! warning "Transferability"
    Droplet-drying, Péclet-morphology, and Gordon–Taylor relations come from food/protein/
    fine-chemical drying. siRNA recovery data is bench-scale on polyplex formulations, not kg of
    naked modified duplex. The duplex Tm for our sequence is a gap.
