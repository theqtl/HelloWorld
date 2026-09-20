# Microbial control

Microbial control spans the whole aqueous train. This is a Tier-1 boundary sketch; the full
contamination-control strategy (CCS) is Tier-2.

## Why this process needs a contamination-control strategy of its own

The published argument that oligonucleotide processes are intrinsically low-bioburden rests on
**exactly two premises**: synthesis runs in organic solvents, and only the last step is aqueous
(<span class="prov-fact">fact</span>; [SRC-PMC7415879](../registers/sources.md)). **Neither holds
here.** This train is fully aqueous with no synthesis solvents, and it carries an enzyme and its
growth-promoting buffer in the stream. That does not vindicate the old mammalian-cell-culture ladder,
but it does mean the project must **justify its microbial control from its own process** and cannot
inherit the modality's low-risk argument (risk R-020). A cell-free-extract route raises the burden
further, feeding a whole proteome and endotoxin into purification rather than one ligase (R-017).

## Bioburden: the one oligonucleotide-specific figure

The bioburden target at drug substance is **below 1 CFU/mL**
(<span class="prov-fact">fact</span>; [SRC-PMC7415879](../registers/sources.md)) — stated in the
oligonucleotide literature as a statement of practice with an explicit case-by-case escape, **not a pharmacopoeial
limit and not a specification**: "levels <1 CFU/mL demonstrate microbial control if bioburden
reduction is performed before the sterile filtration step … but higher levels may be justifiable on a
case-by-case basis" (<span class="prov-fact">fact</span>, oligo DS;
[SRC-PMC7415879](../registers/sources.md)). That is the **process control target**. It sits three
orders of magnitude below the **compendial floor** for a non-sterile substance, TAMC 2000 / TYMC 200
CFU per g or mL (<span class="prov-fact">fact</span>; [SRC-PHEUR-5-1-4](../registers/sources.md)) — the
two are not alternatives; one is the ceiling the pharmacopoeia will not let you exceed, the other is
what a well-run process actually holds.

The mammalian cell-culture ladder this page once carried (100 → 10 CFU/10 mL, endotoxin 5 → 1 EU/mL)
has been **removed**: every figure was located verbatim in an article about mammalian cell culture,
hedged there as typical practice, for the wrong modality (<span class="prov-fact">fact</span>;
[SRC-BPI-HOLDTIME-2025](../registers/sources.md)). Risk R-012 is closed by that finding.

## Endotoxin: there is no compendial ladder, and the old one was the wrong kind of quantity

There is **no compendial endotoxin ladder**. The drug-substance endotoxin limit is **calculated from
the dose**, so it is a quantity **per milligram of substance**, not per millilitre of a process
stream, and the per-mL ladder previously shown was the wrong kind of quantity. The limit is the
compendial endotoxin threshold divided by the maximum dose per kilogram per hour (\(L = K/M\)), so it
cannot be set until the dose is fixed. **The numeric limit is left blank** here against Q-037 rather
than invented, and no per-stream endotoxin ladder replaces it.

The two water figures the project carries have **different status from each other**, and the method
conditions are part of the number:

| Figure | What it is | Source |
|---|---|---|
| 10 CFU / 100 mL in WFI | an **action level**, qualified twice; only with R2A agar, ≥200 mL, 30–35 °C, ≥5 days | [SRC-PHEUR-0169](../registers/sources.md) |
| < 0.25 IU/mL endotoxin in WFI | an actual **limit** (Ph. Eur. 2.6.14) | [SRC-PHEUR-0169](../registers/sources.md) |

A page stating "10 CFU/100 mL" without R2A agar and five days has not stated the requirement
(<span class="prov-fact">fact</span>; [SRC-PHEUR-0169](../registers/sources.md)).

The endotoxin **removal** strategy behind R-007 is also weaker than a protein-feed study suggests: an
anion-exchange adsorber **alone** left 641 EU/mg against a competing polyanion and reached
specification only with an orthogonal sodium-hydroxide step, at 29% recovery
(<span class="prov-fact">fact</span>, polysialic acid on Q membrane;
[SRC-DEVRIES-2018](../registers/sources.md)). The registered buffer-matrix adsorber study had nothing
competing for the ligand ([SRC-PMC12226154](../registers/sources.md)) — precisely the condition that
will not hold for our polyanionic stream. R-007 stays open.

## Water grade per step

For a non-sterile active substance intended for a parenteral product, **purified water** is acceptable
at any step excluding final isolation, and — for a spray-dried powder that is not in solution at
isolation — **purified water is acceptable at final isolation too**, so water for injection is not
automatically required (<span class="prov-fact">fact</span>, risk-based guideline;
[SRC-EMA-WATER-2018](../registers/sources.md), Table 3). That is a real capital and utility saving.
But the guideline's footnote **shifts the burden**: a process using purified water must then set an
endotoxin and microbiological **specification on the drug substance** (see [utilities](../registers/utilities.md)
`UT-WFI`, Q-037). A process on purified water carrying no endotoxin specification would be
indefensible.

## Hold times

Aqueous intermediates in growth-promoting buffers support microbial growth. Controls: refrigerated
storage, limited hold times, and bioburden-reduction filtration into a sanitised vessel for extended
holds, with bioburden/endotoxin testing (<span class="prov-inference">inference</span> — no published
hold-time study exists for any oligonucleotide process, Q-043). Guidance sets a 24 h default beyond
which holds must be justified with data (<span class="prov-fact">fact</span>;
[SRC-EMA-STERILISATION-2019](../registers/sources.md)). Hold points feed the
[stream](../registers/streams.md) and balance definitions (risk R-009).

## Nuclease control

Chemical modification is **protective, but the claim must be kept to what is evidenced.** Internal
2'-modification raises plasma half-life roughly a thousandfold, and protection is **positional**:
"synthetic siRNA molecules with internal 2'-O-methyl modification, but not molecules with terminal
modifications, are protected" (<span class="prov-fact">fact</span>, serum/plasma challenge;
[SRC-CZAUDERNA-2003](../registers/sources.md), [SRC-LAYZER-2004](../registers/sources.md)). Two limits
travel with this: the evidence is **serum challenge, not a manufacturing hold**, and nobody has
measured nuclease carried by process bioburden in a hold vessel, for any modality. So Q-031 is only
half closed — modification does not, on this evidence, make aggressive nuclease control demonstrably
unnecessary in a manufacturing hold. Right-size against this, do not over- or under-engineer.

## Contamination control, CIP/SIP and cleaning validation

The whole train is shared, aqueous equipment run for low bioburden, so a **contamination-control
strategy (CCS)** has to be built from this process's own risk rather than inherited from the modality
(R-020). It spans the levers above — bioburden-reduction filtration into sanitised vessels, controlled
hold times (R-009, Q-043), endotoxin-controlled water and reagents (see [utilities](../registers/utilities.md)),
and a dose-derived endotoxin specification on the drug substance — plus the cleaning of shared
product-contact surfaces between campaigns.

**CIP/SIP.** The evaporator and spray dryer are the hardest-to-clean items — wall deposits on the
falling film, product in the cyclone and receiver — so they set the clean-in-place/steam-in-place
design (risk R-008). CIP loops must reach every product-contact surface at adequate coverage and
velocity; where a surface cannot be cleaned to a defensible limit, single-use contact is the fallback
and is worth evaluating item by item. The CIP/SIP system is registered as `U06-CIP` in the
[equipment register](../registers/equipment.md); its connectivity to each vessel is a P&ID (Tier-3)
detail rather than a block-flow stream, which is why it does not appear on the flowsheet.

**Cleaning validation needs a health-based exposure limit, and there is not one yet.** Cleaning
validation is judged against a **health-based exposure limit (HBEL)**: a permitted daily exposure (PDE)
is derived from toxicology data, then carried into a maximum allowable carryover and per-swab and
per-rinse acceptance limits (`P-HBEL-DS`, method after
[SRC-WHO-TRS1044](../registers/sources.md)). **The HBEL value is left blank** against Q-047 rather than
invented: a PDE cannot be derived without toxicology data, which does not exist in the public record
for this molecule. That gap is **independent of annual demand (Q-002)** — it is blocked on data, not on
scale — and it is a named technology-transfer deliverable (risk R-015). Until it exists, cleaning
acceptance limits for the shared evaporator and dryer cannot be set, so it is a prerequisite for
qualifying that equipment, not a detail to defer.
