# Governing equations

Each equation lists its terms, assumptions, validity range, and a note on whether it is
well founded for this application or borrowed from another industry. Equations render via
MathJax.

---

## EQ-PURITY — block-ligation purity floor

\[
P_{\text{FL}} \;\approx\; \prod_{i=1}^{k} f_i
\]

- \(P_{\text{FL}}\): internal-limited full-length fraction of the isolated product.
- \(f_i\): full-length (deletion-free) fraction of block \(i\); \(k\): number of blocks.
- **Assumes** unreacted blocks and partial-ligation products are cleanly removed (they differ
  by a whole block and are filterable), so only block-internal deletions survive.
- **Validity:** order-of-magnitude design use. <span class="prov-inference">inference</span> —
  our synthesis; no published closed form for siRNA blockmer ligation. Grounded in
  [SRC-WO2020227618](../registers/sources.md) (measured 89–96% blocks) and
  [SRC-NATCOMM-2024](../registers/sources.md) (~5% fragment-internal carry-through).
- **Empirically validated.** Two independent routes reproduce the multiplicative floor. An 18-mer
  assembled from four blocks was measured at **80% purity at 200 g without chromatography**, which
  implies an effective per-block full-length fraction of \(0.80^{1/4} = 0.946\)
  (<span class="prov-inference">inference</span>; [SRC-NAR-2025](../registers/sources.md)); separately
  a 1–3% per-cycle synthesis failure rate gives \(0.97^4 = 0.885\) to \(0.99^4 = 0.961\) for a 5-mer
  (<span class="prov-inference">inference</span>; [SRC-US6087491](../registers/sources.md)). Both land
  in the measured 89–96% block band, so the model reproduces a real assembly to within a point or two.
  Caveat: 80% is the purity of the *protected* 18-mer by that paper's own assay, and chemical coupling
  is not enzymatic ligation.
- **Purity multiplies only within one analytical dimension.** This floor multiplies *denaturing*
  single-strand full-length fractions. It must **not** be used to predict a *non-denaturing* duplex
  purity, which is a different measurement and can read higher than either single strand
  (<span class="prov-fact">fact</span>, method architecture; [SRC-FDA-OXLUMO-CHEMR](../registers/sources.md)).
  Which analytical dimension the drug-substance specification is written in is open (Q-044).
- Central to the [filtration finding](../findings/filtration.md).

## EQ-SPOS — solid-phase full-length yield

\[
\text{FL} = y^{n}
\]

- \(y\): stepwise coupling yield; \(n\): number of couplings.
- **Well founded** for SPOS (<span class="prov-fact">fact</span>; [SRC-ATDBIO-SPOS](../registers/sources.md)).
  Basis figures are unmodified DNA; modified RNA couplings are often lower.

## EQ-DIAF — diafiltration clearance

\[
\frac{C}{C_0} = e^{-\sigma N}
\qquad\Longleftrightarrow\qquad
N = -\frac{\ln(C/C_0)}{\sigma}
\]

- \(C, C_0\): final / initial small-solute concentration; \(\sigma\): sieving coefficient
  (0 fully retained … 1 freely permeable); \(N\): diavolumes.
- \(\sigma \approx 1\): 5 DV → 99.3%, 7 DV → 99.9% cleared. The vendor diavolume table reproduces
  these figures exactly (<span class="prov-fact">fact</span>; [SRC-PALL-TFF](../registers/sources.md)).
- **Well founded** for buffer exchange/desalting, now cited to peer-reviewed primaries that apply the
  relation to a nucleic acid (<span class="prov-fact">fact</span>;
  [SRC-NOURAFKAN-2024](../registers/sources.md), [SRC-KELLY-OPRD-2025](../registers/sources.md); see
  also [SRC-BPT-TFF](../registers/sources.md)).
- **On the σ definition.** The field-standard form is \(e^{-\sigma N}\) with σ the *sieving*
  coefficient, as written above; the complementary form \(e^{-N(1-\sigma)}\) is correct only when σ is
  the *rejection* coefficient. The two are consistent once the coefficient is named, and the vendor
  table's numbers confirm this page's form; see `EQ-SIEVE` for the sieving/rejection relation. The
  complementary form is a live trap in the wider literature, but this page states it correctly.

## EQ-SIEVE — sieving / rejection

\[
S = \frac{C_{\text{permeate}}}{C_{\text{retentate}}}, \qquad R = 1 - S
\]

- MWCO is conventionally the molecular weight at 90% rejection (\(S = 0.1\)).
- **Cut-off selection points below the product mass, not above it.** An oligonucleotide should be
  **at least twice the reported membrane cut-off** for robust retention
  (<span class="prov-fact">fact</span>, single-strand antisense, abstract;
  [SRC-GRONKE-2023](../registers/sources.md)); the vendor **3–6× rule** selects a cut-off three to six
  times *lower* than the molecule to be retained (<span class="prov-fact">fact</span>;
  [SRC-SCHWARTZ-BPI-2003](../registers/sources.md), [SRC-PALL-TFF](../registers/sources.md)). For a
  17 kDa duplex these give an upper bound near 8 kDa (twice rule) or 3–6 kDa (vendor rule); the only
  siRNA optimisation study ran at 10 kDa ([SRC-ZYDNEY-2025](../registers/sources.md)). A previously
  asserted **"30 kDa upper limit" is struck** — it could not be found in any openable source, and
  every quotable rule points the other way (Q-035).
- Real retention differs from nominal: higher ionic strength shrinks the effective nucleic-acid
  size and raises leakage, and charged solutes retain very differently from the uncharged tracers
  cut-offs are measured with (<span class="prov-fact">fact</span>;
  [SRC-ZYDNEY-2024](../registers/sources.md), [SRC-MWCO-REVIEW-2024](../registers/sources.md)).

## EQ-FLUX — gel-polarisation flux

\[
J = k \,\ln\!\left(\frac{C_{\text{wall}}}{C_{\text{bulk}}}\right)
\]

- \(J\): permeate flux (LMH); \(k\): mass-transfer coefficient (rises with crossflow);
  \(C_\text{wall}, C_\text{bulk}\): gel-layer and bulk concentrations.
- Valid in the pressure-independent (gel-limited) regime. Cited to a named-author primary with the
  law and its 0.37×\(C_G\) optimum (<span class="prov-fact">fact</span>;
  [SRC-SCHWARTZ-BPI-2003](../registers/sources.md)), corroborated in exponential form by a
  membrane-science preprint (<span class="prov-fact">fact</span>;
  [SRC-BIESHEUVEL-2024](../registers/sources.md)); the anonymous secondary
  [SRC-BPT-TFF](../registers/sources.md) is demoted to a see-also. **Do not** cite the gel-polarisation
  article for process time: its "Process Time = Filtrate Flow Rate × Volume" is dimensionally
  impossible (L/h × L is not a time). **Borrowed** — oligo-specific flux is a gap (Q-036).
- Membrane sizing: \(A = V_\text{permeate}/(J_\text{avg}\,t)\), with worked examples that reproduce
  by hand (<span class="prov-fact">fact</span>, vendor; [SRC-PALL-TFF](../registers/sources.md)).

## EQ-UFYIELD — UF/DF yield (not a constant)

\[
Y_{\text{UF/DF}} \;=\; \underbrace{e^{-(1-R)\,(\ln \mathrm{VCF} + N)}}_{\text{membrane passage}}
\;-\; \underbrace{L_{\text{hold-up}}}_{\text{tubing + filters}}
\;-\; \underbrace{L_{\text{ads}}}_{\text{membrane adsorption}}
\]

- \(R\): product retention coefficient (`P-UFDF-RETENTION`); \(\mathrm{VCF}\): concentration factor
  (see the note below); \(N\): diavolumes (`P-DF-DIAVOL`); \(L_\text{hold-up}\), \(L_\text{ads}\):
  additive losses (`P-UFDF-HOLDUP-LOSS`, `P-UFDF-ADSORP-LOSS`).
- **Which VCF this uses, stated precisely.** The balance computes VCF as the **concentration** ratio
  `P-CONC-UF`/`P-CONC-LIG`. That is not the volumetric ratio implied by the stream volumes, because
  product is lost across the step: with the retentate sized on what survives UF/DF, the volumetric
  ratio is larger by \(1/(Y_\text{lig}\,Y_\text{UF/DF})\), and the two coincide only at 100% recovery.
  Reconciling them properly means solving the yield and the volume together — the yield depends on VCF,
  which depends on the retentate volume, which depends on the yield — which this balance does not
  attempt. Registered as Q-048 rather than left as an unstated mismatch.
- **Why it replaces a flat "<10%".** The membrane-passage term is a tenfold swing from one membrane
  choice: at \(R=0.99\) the loss is 9.5%, at \(R=0.999\) it is 1.0% (both at \(\ln \mathrm{VCF}+N=10\)),
  reproduced from three worked points (<span class="prov-fact">fact</span>, vendor;
  [SRC-MILLIPORE-TFF](../registers/sources.md)). The **hold-up** term, absent from the old model, is the
  dominant loss at small batch size: 30–40% of a nucleic acid can remain in tubing and filters
  (<span class="prov-fact">fact</span>, mRNA at 20–80 mL; [SRC-NOURAFKAN-2024](../registers/sources.md)).
  Adsorption is additive and protein-specific.
- **Honesty note.** The Millipore relation itself sits in a graphic that did not extract; the
  exponential form above is **derived** from its three worked points, not copied from the figure. The
  hold-up loss is carried as an explicit assumption, not a transferable constant.
- **Validity:** design-level, <span class="prov-inference">inference</span> as applied to this stream.
  Used by the balance (`gen/balance.py`) in place of a flat UF/DF yield. See Q-036, R-011.

## EQ-UFRULE — UF fractionation resolution

\[
r = \frac{\text{MW}_\text{large}}{\text{MW}_\text{small}},
\qquad r \lesssim 5 \;\Rightarrow\; \text{conventional UF fractionation is ineffective}
\]

- \(r\): molecular-weight ratio of the two species to be separated.
- **Validity:** conventional multistage ultrafiltration is described as grossly inefficient for
  fractionating species with \(r < 5\) (<span class="prov-fact">fact</span>;
  [SRC-US7497950](../registers/sources.md)); the classical statement for a clean split is a
  difference of roughly two orders of magnitude. Charged and high-performance membranes push the
  achievable \(r\) down but do not approach unity.
- The cut-off itself is not a sharp line: a molecular-weight cut-off is conventionally the molecular
  weight at 90% rejection, and real membranes have broad pore-size distributions that blur it
  (<span class="prov-fact">fact</span>; [SRC-MWCO-REVIEW-2024](../registers/sources.md)).
- For our case \(r \approx 7330/7000 \approx 1.05\), which is why n-1 cannot be resolved by
  ultrafiltration — by a wide margin, under any published threshold.

## EQ-EVAP — evaporator duty

\[
Q = U A\, \Delta T_{\text{lm}}, \qquad Q_{\min} = \dot m_{\text{water}}\, \lambda
\]

- \(Q\): heat duty; \(U\): overall heat-transfer coefficient; \(A\): area;
  \(\Delta T_\text{lm}\): log-mean temperature difference; \(\dot m_\text{water}\): water
  evaporated; \(\lambda\): latent heat, parameter `P-H2O-LHV` (~2400 kJ/kg at the 0.05–0.1 bar
  vacuum regime, against 2257 kJ/kg at 100 °C; [SRC-STEAMTAB](../registers/sources.md)).
- Boiling-point elevation raises the required \(\Delta T\) as solutes concentrate.
- <span class="prov-fact">fact</span> (standard). \(U\) for this stream is a gap. Correlations
  are **borrowed** from food/fine-chemical evaporation — transferability caveat.
- \(Q_{\min}\) here is only the **latent floor**; the full evaporator duty (sensible + latent +
  losses) and the drying-gas duty are in `EQ-ENERGY`.

## EQ-ENERGY — full thermal duty (evaporator and dryer)

\[
Q_\text{evap} = \big(m_\text{feed}\,c_p\,(T_\text{boil}-T_\text{feed}) + m_\text{water}\,\lambda\big)\,(1+f_\text{loss})
\]
\[
Q_\text{dry,process} = \big(m_\text{water}\,\lambda + m_\text{feed,dry}\,c_p\,(T_\text{out}-T_\text{feed,dry})\big)\,(1+f_\text{loss})
\]
\[
m_\text{gas} = \frac{Q_\text{dry,process}}{c_{p,\text{gas}}\,(T_\text{in}-T_\text{out})}
\qquad
Q_\text{dry,heater} = m_\text{gas}\,c_{p,\text{gas}}\,(T_\text{in}-T_\text{amb})
\]

- **Evaporator:** sensible heat to raise the feed **mass** \(m_\text{feed}\) (volume × `P-SOLN-DENSITY`)
  from `P-EVAP-T-FEED` to the vacuum boiling point `P-EVAP-T-BOIL` at `P-CP-SOLN`, plus the latent term
  (`EQ-EVAP`), plus one loss uplift `P-HEAT-LOSS-FRAC`. If ultrafiltration already meets the evaporator
  target the unit is bypassed and both terms vanish. MVR recovers most of the latent part as
  recompressed vapour, so this is the thermal load, not the live-steam demand.
- **Dryer — two distinct quantities, and conflating them understates the plant load.** The *process*
  duty is what drying requires: evaporate the water, raise the feed to the outlet temperature, plus
  losses. The *heater* duty is the utility load, and it is inlet-gas heating **from ambient**
  (`P-DRY-T-AMBIENT`) — which is what `UT-DRYGAS` is defined as. The enthalpy the gas gives up *across*
  the dryer, \(c_{p,\text{gas}}(T_\text{in}-T_\text{out})\), is neither: it is what sizes the gas mass.
- **The gas mass is derived, not assumed.** It follows from the process duty, so no gas:water ratio is
  carried. It remains scale-parametric because it scales with the water evaporated, so it does not
  resolve Q-002.
- **The latent minimum is a strict floor by construction.** Every term added to it is non-negative, and
  \(Q_\text{heater}/Q_\text{process} = (T_\text{in}-T_\text{amb})/(T_\text{in}-T_\text{out}) \ge 1\)
  whenever \(T_\text{out} \ge T_\text{amb}\). An inverted temperature pair is a data error and **raises**
  rather than silently reporting a zero duty.
- <span class="prov-inference">inference</span> — a standard sensible/latent/gas construction applied
  to this train; the temperatures, the density and the loss fraction are assumptions (Q-045, Q-046).

## EQ-PECLET — spray-dried particle morphology

\[
\mathrm{Pe} = \frac{\kappa}{8 D}
\]

- \(\mathrm{Pe}\): Péclet number; \(\kappa\): droplet evaporation rate, with units of
  area per time, defined by the d-squared law (`EQ-DROPLET`); \(D\): solute diffusion coefficient in
  the liquid phase, also area per time — so the group is dimensionless.
- Low Pe: solutes stay evenly distributed and the particle approaches true density. High Pe: the
  surface becomes enriched, a shell forms early, and the particle is hollow, dimpled or wrinkled.
- <span class="prov-fact">fact</span> (general pharma); [SRC-VEHRING-2008](../registers/sources.md),
  which is the origin of this formulation. [SRC-SD-MORPH](../registers/sources.md) qualifies it:
  solute crystallisation kinetics also govern shell formation, and inlet temperature alone is an
  insufficient predictor of morphology. **Borrowed** from general particle engineering —
  transferability caveat.

## EQ-TG — glass transition vs moisture (Gordon–Taylor)

\[
T_g = \frac{w_1 T_{g,1} + k\, w_2 T_{g,2}}{w_1 + k\, w_2}
\]

- \(w_i\): mass fractions (solid, water); \(T_{g,i}\): component glass transitions;
  \(k\): Gordon–Taylor constant. Water (\(T_g \approx -137\,^\circ\mathrm{C}\)) is a strong
  plasticiser, so residual moisture lowers the powder \(T_g\).
- **Measured values matter more than the anhydrous figure here.** Spray-dried trehalose siRNA
  formulations showed glass transitions of **38–53 °C** at **3.8–4.6%** residual moisture
  (<span class="prov-fact">fact</span>, bench; [SRC-KEIL-2021](../registers/sources.md)). The
  anhydrous-trehalose value often quoted near 117 °C is **not** what the dried product exhibits, and
  designing to it would overstate the thermal margin by decades of degrees.
- Keep the powder below its moisture-shifted \(T_g\), in storage as well as in the dryer.
  **Borrowed** from amorphous-solid pharmaceutics.

## EQ-LIG — ligation conversion (yield term)

Per-ligation conversion and overall mass yield are **different quantities, an order of magnitude
apart**, and must never be conflated. Recovered yield through assembly scales with the product of
junction conversions \(\prod_j c_j\), but each junction also loses material to workup, so the campaign
yield is far below the per-junction conversion. Measured **per-ligation conversion** on fully modified
siRNA blocks is >92% single-feed / >94% split-feed (<span class="prov-fact">fact</span>;
[SRC-CN119265174](../registers/sources.md), `P-LIG-CONV`), while measured **overall campaign mass
yield** for kilogram-scale ligation-built siRNA is **19–43%** (<span class="prov-fact">fact</span>;
[SRC-HONGENE-BROCHURE-2025](../registers/sources.md), `P-YIELD-OVERALL-PUB`) — a conservative figure,
unoptimised and calculated from the lowest-yielding fragment. The 82–96% range often quoted is a
ligase screen on an *unmodified* shortmer whose phosphorothioate donors reacted only ~30%
([SRC-NATCOMM-2024](../registers/sources.md)); >95% is an unreviewed vendor claim. Kinetics are
enzyme-specific and a development gap for our system (Q-010).


## EQ-CASCADE — membrane cascade staging

\[
Y_{\text{1-stage}} = 1 - L, \qquad
Y_{\text{2-stage}} \approx 1 - L\,(1 - R_2)
\]

- \(L\): fraction of product lost to the permeate of the first stage at the target purity;
  \(R_2\): fraction of that lost product recovered by a second stage treating the first stage's
  permeate and recycling the retentate.
- **What it buys.** A single constant-volume diafiltration forced to a demanding purity throws
  product away with the impurity. A second stage recovers most of it. In a worked separation of two
  polyethylene glycols, single-stage diafiltration lost **41%** of product to reach 98% purity, and
  a second stage cut that loss to **6%** at the same purity; a related case moved yield from 58% to
  95% (<span class="prov-fact">fact</span>, non-oligo; [SRC-NAR-2025](../registers/sources.md)
  reading list context and the cascade literature).
- **Why it matters here.** The filterable impurity classes in this train — unreacted blocks and
  partial ligation products — differ from product by a whole block, so the separation is feasible but
  not sharp, and pushing a single stage to high purity is exactly the situation that costs yield.
  Staging is the lever that decouples purity from yield.
- **Assumes** the second stage sees the same separation factor as the first and that recycle does
  not change the feed materially. **Validity:** design-level. <span class="prov-inference">inference</span>
  as applied to this train — no cascade has been demonstrated for a ligated siRNA stream.
  **Borrowed** from organic-solvent nanofiltration and PEG purification.

## EQ-BPE — boiling-point elevation

\[
\Delta T_b = K_b \, m \, i
\]

- \(\Delta T_b\): rise in boiling point over the pure solvent; \(K_b\): ebullioscopic constant of
  the solvent (water: \(0.512\ \mathrm{K\,kg\,mol^{-1}}\)); \(m\): molality of dissolved
  species; \(i\): van 't Hoff factor, the number of particles each solute yields.
- **Why it is in this train.** `EQ-EVAP` assumes a driving temperature difference. As the stream
  concentrates, its boiling point climbs, so at fixed heating-medium temperature the available
  \(\Delta T_\text{lm}\) shrinks and duty falls — and the product sees a higher temperature at the
  very point it is most concentrated. Under vacuum the absolute temperature stays low, which is the
  reason for running the evaporator there.
- **Assumes** a dilute ideal solution. **This assumption is weak exactly where it matters**: a
  concentrated polyanion with its counter-ion cloud is not dilute or ideal, and the colligative
  estimate should be treated as a lower bound and confirmed experimentally. A 14 kDa duplex
  contributes little molality directly; the buffer salts dominate, which is a further argument for
  exchanging into a minimal-salt matrix before evaporation (risk R-005).
- <span class="prov-fact">fact</span> (standard physical chemistry), **applied as
  <span class="prov-inference">inference</span>** to this stream. Gap: measured boiling-point
  elevation for the real matrix (Q-018).

## EQ-DROPLET — droplet drying kinetics (d-squared law)

\[
d^2(t) = d_0^2 - \kappa t
\]

- \(d\): droplet diameter at time \(t\); \(d_0\): initial diameter; \(\kappa\): evaporation
  rate, units of area per time. Droplet **surface area** falls linearly with time, so the lifetime of
  a pure droplet is \(\tau = d_0^2/\kappa\).
- \(\kappa\) is what feeds the Péclet number in `EQ-PECLET`; the two equations are one model.
- **Assumes** a quiescent surrounding gas, quasi-steady liquid and vapour phases, constant
  thermophysical properties, and no solute. **Validity:** the constant-rate period only. Once a shell
  forms, drying becomes diffusion-limited and this law stops applying — which is precisely the regime
  that decides particle morphology and residual moisture, so it must not be extrapolated to the end
  of drying.
- While the surface is wet the droplet sits near the **wet-bulb** temperature, well below the gas
  temperature. This is why outlet temperature is a conservative proxy for what the product
  experiences, and why the duplex survives an outlet below its melting temperature.
- <span class="prov-fact">fact</span> (standard); [SRC-VEHRING-2008](../registers/sources.md).
  **Borrowed** from combustion and food/pharma drying — transferability caveat.
