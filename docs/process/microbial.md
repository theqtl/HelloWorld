# Microbial control

Microbial control spans the whole aqueous train. This is a Tier-1 boundary sketch; the full
contamination-control strategy (CCS) is Tier-2.

## Where the limits sit

Bioburden and endotoxin tighten toward the DS stage. **The numeric ladder below is not verified for
oligonucleotide drug substance and must not be used as a specification** (Q-037). It reproduces a
published ladder for **mammalian cell-culture biologics**
([SRC-BPI-HOLDTIME-2025](../registers/sources.md)); the oligonucleotide-specific paper it was
previously attributed to is paywalled and could not be read, and its visible preview text quotes
different figures (a pharmacopoeial maximum of 200 CFU/g or mL, and <1 CFU/mL to demonstrate
control).

| Stage | Bioburden | Endotoxin | Status |
|---|---|---|---|
| Upstream | 1 CFU/10 mL | 10 EU/mL | <span class="prov-assumption">unverified for oligo DS</span> |
| Intermediate | 100 CFU/10 mL | ~5 EU/mL | <span class="prov-assumption">unverified for oligo DS</span> |
| Approaching DS | 30 → 10 CFU/10 mL | down to ~1 EU/mL | <span class="prov-assumption">unverified for oligo DS</span> |
| Final purification | <10 CFU/100 mL | 0.25–1 EU/mL | <span class="prov-assumption">unverified for oligo DS</span> |

The one oligonucleotide-specific figure we can cite is that levels below 1 CFU/mL demonstrate
microbial control where bioburden reduction precedes sterile filtration
(<span class="prov-fact">fact</span>, oligo DS; [SRC-PMC7415879](../registers/sources.md)).

## Hold times

Aqueous intermediates in growth-promoting buffers support microbial growth. Controls: refrigerated
storage, limited hold times, and bioburden-reduction filtration into a sanitised vessel for
extended holds, with bioburden/endotoxin testing (<span class="prov-inference">inference</span> —
the oligonucleotide-specific hold-time source is paywalled and unread;
[SRC-OPRD-2025](../registers/sources.md)). Hold points feed the [stream](../registers/streams.md)
and balance definitions (risk R-009).

## Nuclease control

Chemical modification (2'-OMe/2'-F/PS) is expected to make the duplex nuclease-resistant, so
aggressive RNase control may be disproportionate — but this needs evidence for our system
(Q-031). This is a place to right-size, not over-engineer.

## Water and boundaries

Water quality per step (WFI vs purified water) and the low-bioburden vs sterile boundary for a
spray-dried DS (typically not a sterile product) are to be set (gaps). Sterilising-grade filter
validation (bacterial retention, integrity testing) applies at the defined boundary.

## Hard-to-clean equipment

The evaporator and spray dryer are hard to clean (wall deposits, cyclone product). CIP/SIP design
and cleaning validation for low-bioburden operation are Tier-2 and flagged as risk R-008; single-use
contact is worth evaluating where feasible.
