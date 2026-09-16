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
| Outlet temperature | below duplex Tm; particle stays near wet-bulb while wet | integrity preserved when T-out < Tm ([SRC-KEIL-2021](../registers/sources.md)) |
| Residual moisture | low (e.g. ~2–3% for trehalose at ~10% outlet RH) | plasticiser; keep below moisture-shifted Tg (`EQ-TG`) |
| Atomiser | to be selected (rotary vs two-fluid vs pressure) | shear on the duplex; gap |
| Gas | N₂, low O₂ | limit oxidation of oligo; inference |

## Atomiser, morphology, yield

Particle morphology follows the Péclet number (`EQ-PECLET`): high Pe → hollow/wrinkled, low Pe →
dense. Atomiser choice trades droplet size against shear. Cyclone and wall losses set yield at
scale and are a **gap** (Q-019, `P-YLD-DRY`). Containment and dryer sanitisation for low-bioburden
operation are demanding and are Tier-2 (risk R-008).

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
