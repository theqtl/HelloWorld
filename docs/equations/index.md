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
  [SRC-ZHOU-2022](../registers/sources.md), [SRC-NATCOMM-2024](../registers/sources.md).
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
- \(\sigma \approx 1\): 5 DV → 99.3%, 7 DV → 99.9% cleared.
- **Well founded** for buffer exchange/desalting (<span class="prov-fact">fact</span>;
  [SRC-BPT-TFF](../registers/sources.md)). Note: the field-standard form uses
  \(e^{-\sigma N}\); an alternative \(e^{-N(1-\sigma)}\) appears with a retentate-basis σ — reconcile
  the σ definition before use.

## EQ-SIEVE — sieving / rejection

\[
S = \frac{C_{\text{permeate}}}{C_{\text{retentate}}}, \qquad R = 1 - S
\]

- MWCO is conventionally the molecular weight at 90% rejection (\(S = 0.1\)).
- Real retention differs from nominal: higher ionic strength shrinks the effective nucleic-acid
  size and raises leakage. <span class="prov-fact">fact</span>; [SRC-ZYDNEY-2024](../registers/sources.md).

## EQ-FLUX — gel-polarisation flux

\[
J = k \,\ln\!\left(\frac{C_{\text{wall}}}{C_{\text{bulk}}}\right)
\]

- \(J\): permeate flux (LMH); \(k\): mass-transfer coefficient (rises with crossflow);
  \(C_\text{wall}, C_\text{bulk}\): gel-layer and bulk concentrations.
- Valid in the pressure-independent (gel-limited) regime. Membrane sizing:
  \(A = V_\text{permeate}/(J_\text{avg}\,t)\). <span class="prov-fact">fact</span> (protein-scale);
  [SRC-BPT-TFF](../registers/sources.md). **Borrowed** — oligo-specific flux is a gap.

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

Overall recovered yield through assembly scales with the product of junction conversions,
\(\prod_j c_j\); reported junction conversions span 82–96% (analytical, modified/PS;
[SRC-NATCOMM-2024](../registers/sources.md)) to >95% (vendor). Kinetics are enzyme-specific and a
development gap for our system (Q-010).


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
