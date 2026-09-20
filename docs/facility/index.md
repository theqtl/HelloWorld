# Greenfield facility concept (Tier 3 — sketch)

Full facility design is Tier 3. This page records the concept-level consequences that already
follow from the process decisions, so the capital team has a starting frame.

## The big simplification: no solvents

The DS train is fully aqueous. Block synthesis (solvent-intensive) is a supplier operation. So the
facility has **essentially no flammable-solvent inventory**, which collapses the hazardous-area
(ATEX/NEC) electrical classification that normally dominates an oligonucleotide-synthesis plant.
This is a genuine capital and footprint saving and is a **finding**, not a driver
(<span class="prov-inference">inference</span> from the solvent-free boundary). It removes the
*solvent-vapour* hazard; the dried powder still carries a *dust* hazard, treated separately below.

## What drives area classification instead

Not solvents but **bioburden/low-bioburden control**: aqueous processing, buffer prep, and the
open-ish handling around spray-dried powder. Classification is driven by the low-bioburden
boundary and powder containment, not solvent fire/explosion. To be developed.

## Dust explosion: the one combustion hazard a solvent-free plant still carries

A spray-dried organic drug substance is a combustible powder, so the dryer, cyclone and receiver
carry a **dust-explosion** hazard even though the plant has no solvent (risk R-016). The current
combustible-dust standard is **NFPA 660-2025**, which consolidated NFPA 654, applied with explosion
protection (NFPA 68-2023, NFPA 69-2024) (<span class="prov-fact">fact</span>;
[SRC-STANDARDS-CURRENT](../registers/sources.md)). The explosion parameters of the actual powder
(K\(_{st}\), minimum ignition energy, minimum explosible concentration) are a **testing deliverable,
not a literature lookup**.

## Standards, at current editions

Citing a superseded standard dates a package on sight. The current editions
(<span class="prov-fact">fact</span>; [SRC-STANDARDS-CURRENT](../registers/sources.md)):

- **ASME BPE-2026** (bioprocessing equipment), superseding BPE-2024/2022.
- **ASTM E2500-25** (commissioning & qualification, now "Science and Risk Based Approach", adding
  ICH Q12/Q13), superseding E2500-20.
- **NFPA 660-2025** (combustible dusts), consolidating NFPA 654.
- **IEC 60079-10-2:2026** (explosive dust atmospheres classification), superseding the 2015 edition —
  the most likely stale citation in any package written before 2026.

Two scope answers this settles: **EU GMP Annex 1** (sterile manufacture) does **not** apply to a
non-sterile drug substance, though it invites partial adoption for low-bioburden intermediates on
condition the manufacturer documents which principles were applied; and **Annex 15** is optional
supplementary guidance for an active substance, so its three-batch expectation is a default to justify,
not a rule.

## Water grade per step

For this non-sterile active substance intended for a parenteral product, EMA guidance permits
**purified water** at all steps including final isolation of a dried (not-in-solution) powder —
water for injection is not automatically required — **provided** an endotoxin and microbiological
specification is set on the drug substance (<span class="prov-fact">fact</span>, risk-based;
[SRC-EMA-WATER-2018](../registers/sources.md), and the [microbial page](../process/microbial.md)).

## Utilities dominated by water and thermal duty

- **Water (WFI/purified):** the dominant consumer is diafiltration (diavolumes × retentate
  volume). See [utilities](../registers/utilities.md) and the [balance](../balance/results.md).
- **Thermal:** the spray dryer dominates, and by more than a latent-heat figure suggests. The balance
  reports the dryer's *process* duty and, separately, its **heater** duty — inlet gas heated from
  ambient, which is what `UT-DRYGAS` actually is and the number to size the utility on. The evaporator
  is much the smaller load and is bypassed entirely if ultrafiltration already meets its target
  (`EQ-ENERGY`, [balance](../balance/results.md); utilities `UT-STEAM`, `UT-DRYGAS`). MVR reduces
  evaporator steam. Absolute loads scale with demand (Q-002).
- **Waste:** large aqueous waste (spent permeate + condensate) — a facility and EHS driver.

## To be developed (Tier 3)

Area classification map, layout and personnel/material flows, expansion strategy, and the capital
cost drivers, all as a function of the real throughput scenario (Q-002).
