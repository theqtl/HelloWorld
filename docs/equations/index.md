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
\frac{\text{MW}_\text{large}}{\text{MW}_\text{small}} \gtrsim 10
\quad\text{for a clean UF split; band}\approx \text{MWCO} \pm 50\%
\]

- Why n-1 (~5% difference) cannot be resolved by UF. <span class="prov-fact">fact</span>;
  Sigma / USPTO 6187190 (reading list).

## EQ-EVAP — evaporator duty

\[
Q = U A\, \Delta T_{\text{lm}}, \qquad Q_{\min} = \dot m_{\text{water}}\, \lambda
\]

- \(Q\): heat duty; \(U\): overall heat-transfer coefficient; \(A\): area;
  \(\Delta T_\text{lm}\): log-mean temperature difference; \(\dot m_\text{water}\): water
  evaporated; \(\lambda\): latent heat (~2400 kJ/kg at reduced pressure).
- Boiling-point elevation raises the required \(\Delta T\) as solutes concentrate.
- <span class="prov-fact">fact</span> (standard). \(U\) for this stream is a gap. Correlations
  are **borrowed** from food/fine-chemical evaporation — transferability caveat.

## EQ-PECLET — spray-dried particle morphology

\[
\mathrm{Pe} = \frac{\kappa}{8 D}
\]

- \(\mathrm{Pe}\): Péclet number; \(\kappa\): droplet evaporation rate; \(D\): solute diffusion
  coefficient. High Pe → surface enrichment → hollow/wrinkled particles; low Pe → dense spheres.
- <span class="prov-fact">fact</span> (general pharma); [SRC-SD-MORPH](../registers/sources.md).
  **Borrowed** from general particle engineering — transferability caveat.

## EQ-TG — glass transition vs moisture (Gordon–Taylor)

\[
T_g = \frac{w_1 T_{g,1} + k\, w_2 T_{g,2}}{w_1 + k\, w_2}
\]

- \(w_i\): mass fractions (solid, water); \(T_{g,i}\): component glass transitions;
  \(k\): Gordon–Taylor constant. Water (\(T_g \approx -137\,^\circ\mathrm{C}\)) is a strong
  plasticiser, so residual moisture lowers the powder \(T_g\).
- Keep the powder below its moisture-shifted \(T_g\). <span class="prov-fact">fact</span>;
  [SRC-KEIL-2021](../registers/sources.md). **Borrowed** from amorphous-solid pharmaceutics.

## EQ-LIG — ligation conversion (yield term)

Overall recovered yield through assembly scales with the product of junction conversions,
\(\prod_j c_j\); reported junction conversions span 82–96% (analytical, modified/PS;
[SRC-NATCOMM-2024](../registers/sources.md)) to >95% (vendor). Kinetics are enzyme-specific and a
development gap for our system (Q-010).
