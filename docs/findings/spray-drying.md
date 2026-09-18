# Does the duplex survive spray drying?

**Short answer:** The evidence says a duplex can be spray dried intact **if the particle stays
below its melting temperature and is embedded in an amorphous sugar glass.** The recommended
base case is to dry the annealed duplex in a trehalose matrix at a low outlet temperature, with
"dry the strands separately and anneal afterward" kept as a fallback. The decision is also a
**product-form** decision, and it is coupled to where annealing sits (question **Q-001**).

## 1. The concern, stated precisely

Atomisation and drying expose the product to shear and to heat. A duplex is held together by
base pairing; above its melting temperature (Tm) the strands dissociate. The question is whether,
during the seconds a droplet dries, the material ever exceeds Tm, and whether the dry solid then
holds the duplex during storage.

## 2. What the evidence shows — the glass transition binds first

- **The binding constraint is the glass transition, not the melting temperature.** The spray-dried
  powder must be held below its *moisture-shifted* glass transition, and that sits **below** the
  duplex melting temperature, so it is the limit that binds. In the siRNA spray-drying study, **all
  trehalose formulations showed glass transitions between 38 and 53 °C**, set by residual moisture of
  **3.8–4.6%** (0.2–0.4% for mannitol) (<span class="prov-fact">fact</span>, bench;
  [SRC-KEIL-2021](../registers/sources.md)). Water plasticises the glass (Gordon–Taylor;
  [Equations](../equations/index.md), `EQ-TG`), so moisture and Tg move together. Anhydrous trehalose
  is often quoted near 117 °C; that is *not* what the dried product does, and designing to it would
  overstate the thermal margin by decades of degrees. Driving residual moisture down raises Tg and is
  the main lever available. **This binds on storage and handling, not just on the dryer.**
- **The melting temperature is the looser of the two limits.** A 21-nucleotide siRNA duplex melts at
  **58.1 °C** unmodified, rising to 60.4–64.1 °C with 2'-F or 2'-OMe at three positions, in 100 mM
  NaCl (<span class="prov-fact">fact</span>, bench UV melting; [SRC-MALEK-2019](../registers/sources.md)).
  Against a 38–53 °C glass transition, a 58–64 °C melting point is **5–25 °C higher** — necessary to
  respect but not the constraint that binds. Keeping the outlet below Tm is still required: both
  matrices "preserved siRNA integrity … at outlet temperature below the siRNA melting temperature"
  (<span class="prov-fact">fact</span>; [SRC-KEIL-2021](../registers/sources.md)). **Do not extrapolate
  the +1 to +2 °C/nt modification increment across all 21 positions** — it was measured over three, and
  multiplying it to claim a fully modified duplex melts near 100 °C is unsupported (Q-030).
- **Trehalose gives full recovery; the matrix matters more than the fact of drying.** Trehalose
  formulations allowed **full siRNA recovery** where crystalline **mannitol lost ~20% of the siRNA**
  (and 50–60% of polymer) (<span class="prov-fact">fact</span>, bench, siRNA polyplex;
  [SRC-KEIL-2021](../registers/sources.md)).
- **Evaporative cooling helps.** A drying droplet stays near the wet-bulb temperature until the
  surface dries, so the material runs cooler than the gas outlet during the critical wet period
  (<span class="prov-inference">inference</span>, standard drying theory).
- **Atomisation shear is not a governing risk for a short duplex.** Naked siRNA kept **>80% band
  intensity and full silencing activity** through sonication, vortexing, atomisation and
  lyophilisation, whereas naked plasmid DNA did not survive the same treatments
  (<span class="prov-fact">fact</span>, bench, naked nucleic acids;
  [SRC-NAKED-NA-2023](../registers/sources.md)). The shear worry is real for a large flexible molecule
  like plasmid DNA; a short rigid duplex is not damaged by atomisation. This lets R-003 refocus
  entirely on temperature and the glass transition.

## 3. Recommendation, with the fallback

**Base case: dry the annealed duplex** in an amorphous trehalose (or sucrose) glass, held first
**below the moisture-adjusted Tg** (the binding limit, measured 38–53 °C for spray-dried trehalose
siRNA powders; [SRC-KEIL-2021](../registers/sources.md)) and, as the looser limit, below the duplex Tm
(58–64 °C; [SRC-MALEK-2019](../registers/sources.md)), under low-oxygen (N₂) drying. "Below Tg" is a
much tighter constraint than the anhydrous-trehalose figure suggests, and it binds on storage as well
as on drying, so residual-moisture control leads the design. This is consistent with the ligation
finding that the product is co-assembled and handled **as a duplex** (see §5).

**Fallback: dry the two single strands separately and anneal afterward** (during reconstitution or
fill-finish). Single strands have no duplex to lose in the dryer, so this removes the Tm risk
entirely — at the cost that the drug substance becomes **two powders plus a downstream annealing
step**, a materially different product definition. Registered as risk **R-003**, tied to **Q-001**.

The DoE that resolves the choice: measure the achieved-moisture **Tg** for our matrix (Q-039, the
higher-priority unknown) and the modified-duplex **Tm** for our sequence (Q-030), then map retained
duplex fraction and activity against outlet temperature, excipient:API ratio, and residual
moisture, at pilot scale where the outlet/particle temperature relationship is representative.

## 4. Particle engineering and yield

Particle morphology is governed by the **Péclet number** (ratio of evaporation rate to solute
back-diffusion): high Pe enriches the surface early and gives hollow, wrinkled particles; low Pe
gives dense spheres (<span class="prov-fact">fact</span>, general pharma;
[SRC-SD-MORPH](../registers/sources.md), and `EQ-PECLET` in [Equations](../equations/index.md)).
Yield at scale is set by cyclone and wall losses; these are a **gap** for our system (Q-019 and the
[spray-drying process page](../process/spray-drying.md)).

## 5. Why this couples to annealing (Q-001)

The enzymatic-ligation evidence is that dsRNA nick-sealing ligases require a duplex nick, so
annealing is **interleaved with ligation** and the material is a duplex through the downstream
train (<span class="prov-fact">fact</span>/<span class="prov-inference">inference</span>;
[SRC-ALMAC-2023](../registers/sources.md), [SRC-HONGENE](../registers/sources.md)). That makes the
duplex the natural thing to dry, which favours the base case. It also creates a tension with the
brief's "roughly seven kilodalton" (single-strand) basis for membrane selection — flagged in
**Q-001**. If the intended process instead purifies single strands and anneals only at the very
end, the fallback (dry strands separately) becomes the natural route. Resolving Q-001 settles both
the filtration species and the drying form.

## 6. Bottom line

Drying the duplex is feasible and evidenced, not a leap of faith, provided the powder is held below
its moisture-shifted glass transition (the binding limit) and the outlet stays below Tm (the looser
one), vitrified in a sugar glass. Atomisation shear is not a governing risk for a short duplex
([SRC-NAKED-NA-2023](../registers/sources.md)). The residual risk is real but bounded and has a clean
fallback. Spray drying does **not** force a retreat to lyophilisation — noting honestly that the one
approved siRNA process in the register dries by lyophilisation
([SRC-PATISIRAN-EPAR](../registers/sources.md)), which is a fact to record, not an argument to change
this process.

The one thing that tightened on review is the **thermal margin after drying**. With a measured Tg of
38–53 °C at 3.8–4.6% residual moisture ([SRC-KEIL-2021](../registers/sources.md), Q-039), the
powder's stability window sits much closer to ambient
than an anhydrous-trehalose figure would imply. Residual moisture specification and cold-chain
handling of the dried drug substance move from housekeeping to critical, and the DoE below must map
Tg against achieved moisture rather than assume a high-Tg glass.

!!! warning "Transferability"
    The drying correlations (Péclet/morphology, Gordon–Taylor Tg–moisture, droplet kinetics) come
    largely from food, protein, and fine-chemical drying. The siRNA-specific recovery data is bench
    scale on polyplex formulations, not kilograms of naked modified duplex. The duplex Tm for our
    sequence is a gap. Treat the mechanism as sound and the numbers as to-be-confirmed.
