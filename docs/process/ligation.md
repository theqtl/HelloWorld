# Enzymatic ligation

Chemically synthesised blocks are joined into the siRNA strand(s) by enzymatic ligation. This is
a fixed decision; the work here is how to make it robust.

This page is the narrative. The evidence behind it — every band with each endpoint beside its own
source and scale, the couplings that stop the bands forming a box, the information-requirement
checklist and the acceptance panel — is generated from the registers on the
[ligation design envelope](ligation-envelope.md) page. Where the two disagree, the envelope page
is derived from `data/*.csv` and this one is hand-written, so the envelope wins.

How well each of those numbers is actually known — which were re-checked against the document,
which a research pass asserted and nothing verified, and the four claims that were **withdrawn**
after checking — is the [ligation evidence](../sources/ligation-evidence.md) page. Read it before
quoting any figure from either page: it is where the corrections live.

## Enzyme and chemistry

- The viable class is **double-stranded RNA (nick-sealing) ligases** — T4 RNA ligase 2 family and
  engineered variants (<span class="prov-fact">fact</span>, bench→1 L, fully modified siRNA;
  [SRC-ALMAC-2023](../registers/sources.md); vendor [SRC-CODEXIS](../registers/sources.md)).
- **Wild-type T4 DNA ligase is poor at** 2'-OMe substrates (not "unable"): it is "poor at ligating
  2′-OMe substituted oligonucleotide segments", and on an RNA-splinted substrate T4 DNA ligase gives
  essentially all adenylylated dead-end product (<span class="prov-fact">fact</span>;
  [SRC-USPTO-10640812](../registers/sources.md), [SRC-PBCV1-2014](../registers/sources.md)). The same
  patent — GlaxoSmithKline's engineered-ligase patent "Processes for the production of oligonucleotides",
  not a T4 negative-result patent — identifies alternatives that **do** work, including engineered
  Enterobacteria phage CC31 variants and Chlorella virus DNA ligase (SplintR)
  (<span class="prov-fact">fact</span>; [SRC-USPTO-10640812](../registers/sources.md)). That patent
  **does** report conversion — it defines it verbatim as `Conversion = product area/(template +
  product area) * 100`, tabulates it, and its Example 13 is a nine-point time series — so an earlier
  claim here that it gives "peak-area improvements only" is struck. It still does not close Q-010,
  for a narrower and more useful reason: the time series is normalised to an internal tri-template
  hub peak, making it a species *distribution* rather than that patent's own defined conversion, and
  neither is commensurable with `P-LIG-CONV`. The three figures must not be pooled or read as
  corroborating one another. Its best-converting example also runs on an **all-phosphodiester**
  backbone, while its phosphorothioate/MOE gapmer figures are 11.8% or less
  ([SRC-USPTO-10640812](../registers/sources.md), Q-010).
- All ATP-dependent ligases require **5'-phosphate + 3'-OH** at the junction. The 5'-phosphate is
  installed chemically (in-line phosphoramidite reagent, ~quantitative, DMT-trackable) or
  enzymatically by a polynucleotide kinase; Almac screened a kinase panel and ran a one-pot
  phosphorylation at 5 mM blockmer (<span class="prov-fact">fact</span>;
  [SRC-ALMAC-2023](../registers/sources.md)). The paper uses kinase cell-free extracts rather than a
  named T4 enzyme, so the specific enzyme is not pinned down here.

## Annealing is interleaved (Q-001)

dsRNA ligases need a duplex nick, so the complementary strand (or an overlap) templates each
ligation and the duplex is **co-assembled**, not built as free single strands annealed at the end
(<span class="prov-fact">fact</span>/<span class="prov-inference">inference</span>;
[SRC-ALMAC-2023](../registers/sources.md), [SRC-HONGENE](../registers/sources.md)). Almac used a directional "3-2-3-2" assembly, each stage starting with three blockmers and ending
with two partially complementary strands whose overhang templates the next annealing step. The
paper demonstrates "successful ligation with complementary portions as short as **3 bp**"
(<span class="prov-fact">fact</span>; [SRC-ALMAC-2023](../registers/sources.md), verified verbatim in
the main text). An earlier version of this page said that figure could not be found in the paper and
was not carried; that was wrong and is corrected — it is in the main text, and it travels with its
system: fully modified blockmers bearing phosphorothioate linkages and GalNAc.

## Conditions (documented set, Almac, fully modified siRNA)

**Each row states the scale it was measured at, because two of them were previously labelled
"bench→1 L" and are not.** That mislabel put a 96-well plate shaker setting and a sampling schedule
into a table headed 1 L, and it is the defect this table was rebuilt to remove.

| Parameter | Value | Scale it was measured at |
|---|---|---|
| Anneal | 50 mM Tris-HCl pH 7.5, 100 mM KCl, 10 mM MgCl₂; 65 °C for 15 min, then cooled to RT and held on ice | bench; the composition is now registered as `BUF-LIG` and the condition as `P-LIG-ANNEAL-T` / `P-LIG-ANNEAL-HOLD` ([SRC-ALMAC-2023](../registers/sources.md)) |
| Reductant | + 1 mM DTT | bench; added when the extract is resuspended ([SRC-ALMAC-2023](../registers/sources.md)) |
| Reaction temperature | 25 °C | **96-well plate screening.** Not a demonstrated optimum — see below (`P-LIG-T`) |
| Agitation | 400 rpm | **96-well plate shaker setting.** The paper gives *no* agitation rate for the 1 L vessel ([SRC-ALMAC-2023](../registers/sources.md)) |
| Sampling | T = 1 h and 20 h | **a sampling schedule, not a hold time.** The paper gives no hold time for the 1 L vessel (`P-LIG-TIME`, Q-010) |
| Product conc | ~1 mM duplex in jacketed 1 L vessels | 1 L — the largest real public scale, and an **upper bound** on titre rather than a titre, since the paper reports no conversion anywhere (`P-CONC-LIG`, Q-016) |
| Blockmer conc | up to 10 mM, but slow and **did not go to completion** | scale not stated; qualitative, and the high end of a span that is *not* a range (`P-LIG-SEG-CONC`, Q-064) |
| ATP conc | 2 mM | **96-well plate screening at 0.1 mM blockmer** — SI Table S1, titled "Reaction conditions for RNAL screening", a tenth of the demonstrated titre (`P-LIG-ATP`) |
| Ligase loading | RNA ligase cell-free extract 1 mg/mL | **the same plate screen.** The paper reports no loading for the 1 mM / 1 L run, so `P-LIG-ENZ-LOAD` stays blank (`Q-050`) |
| Kinase kill | 75 °C for 10–30 min | bench, 0.5 mM in plates; applied to **single strands before annealing**, so it is the *kinase* kill and not a ligase inactivation ([SRC-ALMAC-2023](../registers/sources.md), Q-059) |

There is **no registered reaction termination** at all: the methanol quench in this paper is an
analytical sample quench for HPLC timepoints, not a process step. The documented process
inactivations sit at 80–95 °C, above the whole measured duplex melting band, and one patent removes
an immobilised enzyme centrifugally with no thermal step whatever — so whether the step exists is
undecided (`P-LIG-INACT-T`, C-014, R-022, Q-059).

The circulating vendor trio — ">95% conversion, substrate loads up to 100 g/L, >98% post-purification
purity" — is **marketing-only**: it is traceable to a single company blog
([SRC-CODEXIS](../registers/sources.md)) and is corroborated **nowhere**, including in the company's
own press release (whose only numeric claim, >98% incorporation, is for a different, non-ligation
chemistry; [SRC-CODEXIS-PR-2024](../registers/sources.md)) and in all four of its ligation patent
families, which report only relative fold-improvement conversions
([SRC-CODEXIS-PATENTS](../registers/sources.md)). Treat it as an unverified vendor claim of unstated
basis. The design anchors are instead the **measured** figures: a ~1 mM working titre in a 1 L vessel
([SRC-ALMAC-2023](../registers/sources.md), Q-016/Q-034) and >92% per-ligation flow conversion
([SRC-CN119265174](../registers/sources.md), `P-LIG-CONV`). The often-quoted 82–96% conversion range
is a ligase screen on an **unmodified** shortmer whose 5'-monophosphorothioate substrates reacted only
~30% ([SRC-NATCOMM-2024](../registers/sources.md)). Per-ligation conversion must not be read as a step
yield or as overall mass yield (19–43% at campaign scale; `P-YIELD-OVERALL-PUB`). See Q-010.

## Side reactions to control at the reaction

The **adenylylated dead-end (+AMP)** has been directly observed in exactly this chemistry — the
by-product "2.3_2.4[+AMP]" in fully modified siRNA blockmer ligation — alongside hairpins, concatemers
and 3'-terminal-nucleotide loss (<span class="prov-fact">fact</span>;
[SRC-ALMAC-2023](../registers/sources.md), Table 1). The authors' mitigation was to change the
disconnection and reaction staging so the species does not form, not to remove it downstream: it
differs from product by ~one residue and **cannot be cleared by filtration** (risk R-010, now anchored
to this observation). Controlled by directional assembly, keeping ≤3 blockmers present at once, and
tuning temperature/time.

There is a real **ATP coupling** with no published setpoint for a modified-siRNA system (Q-040), and
it is weaker than this page previously claimed. A four-ligation assembly is said to need "at least
4 mM ATP" ([SRC-WO2025262452](../registers/sources.md)) — but read in place, that sentence is the
**statement of the problem that document's invention solves**, not its operating condition. The same
document teaches "less than about 4 mM ATP … optionally … 0.5 mM or less", says its regeneration
system "overcomes the requirement for high concentrations of ATP", and claims complete ligation with
"sub-stoichiometric quantities of ATP or AMP". The suppression side is softer too: little inhibition
is reported at 1 mM ATP for most sequences ([SRC-PBCV1-2014](../registers/sources.md), unmodified DNA
on RNA splints — the mechanism transfers, the number does not). **So there is no window empty by
6–40×, and no such claim is made here** — an earlier version of this page implied one. Regeneration
from AMP carries its own ceiling, a "maximum of 66 % conversion to ATP", and in-situ generation from
AMP and polyphosphate *is* exemplified, which also retires the claim that fed-batch has no
demonstration anywhere.

The coupling that nobody had registered is the one that reaches downstream: ATP chelates magnesium
roughly one-for-one, so the ATP charge draws down the free Mg²⁺ the ligase needs, and raising total
magnesium to compensate loads exactly the species that resists diafiltration (`CPL-002`, R-014,
`IMP-DIVALENT`). Both couplings are on the [envelope page](ligation-envelope.md).

## Enzyme removal — the linchpin

Soluble ligase cannot be cleared from the strand by size ultrafiltration, and the reason is now
quantitative rather than qualitative: the candidate enzymes are **2.0–5.4× the product mass**
against a vendor fractionation rule of thumb that asks for tenfold, so a membrane chosen to retain a
14 kDa duplex retains a 34–75 kDa protein *harder*. That is **0 log** — ultrafiltration
co-concentrates the ligase with the product, which makes it a concentration step and not a
separation step (`P-ENZ-CLEARANCE-LRV`, Q-032). It is also why the one adjacent measured figure does
not transfer: a 99 kDa polymerase against a ~1 MDa mRNA is about tenfold, a pair that *passes* the
rule ours fails ([SRC-T7RNAP-2024](../registers/sources.md)).

**Immobilised or solid-phase ligase**, removed by filtration or centrifugation, is therefore the
route that keeps the train filtration-led (finding: [filtration](../findings/filtration.md) §4). An
immobilised RNA ligase has held >92% conversion on fully modified siRNA blocks for over 100 h
([SRC-CN119265174](../registers/sources.md)) — and note that the ">100 h" is a **catalyst lifetime,
not a hold time**, the most mis-readable number in the set. So the *duty* half of the immobilisation
risk is answered. Two things it does **not** buy, both corrected here:

- **Choosing immobilisation does not delete the heated vessel.** The same patent heat-kills its
  immobilised arm at 85 °C on the same terms as its soluble arm (`P-LIG-INACT-T`), and that arm is
  the only one it ever assesses for product quality — while four *other* examples remove the
  immobilised enzyme centrifugally with no thermal step at all, one of them immobilised *and* batch
  *and* unheated. So the thermal step is decided neither by soluble-versus-immobilised nor by
  batch-versus-flow (C-012, Q-059). Immobilisation can even make an enzyme *harder* to kill:
  benzylguanine-agarose-immobilised T4 DNA ligase survived 55 and 65 °C where the soluble form was
  irreversibly denatured at 45 °C, and magnetic beads gave no protection at all
  ([SRC-NEB-WO2023173098](../registers/sources.md), Example 3).
- **It changes the impurity list rather than escaping it.** ICH Q6B §6.2.1(c) names "carriers",
  "ligands" and "other leachables" alongside enzymes, and the one demonstrated immobilised route runs
  a nickel-iminodiacetic-acid agarose in a buffer containing 1 mM DTT — the highest-leaching common
  chelator in a reducing buffer, with nickel, ligand and desorbed enzyme all unmeasured
  ([SRC-ICH-Q6B](../registers/sources.md), C-012, Q-060).

**Quantitative clearance data is not publicly available** for either branch: no ppm, log-reduction or
immunoassay figure exists anywhere the dive read (Q-032; risk R-002). The gap is now known to be
**two-deep** — there is no *limit* to clear to, since the EU oligonucleotide guideline omits protein
entirely and offers only toxicological qualification (Q-060), and there is no *assay* demonstrated in
this matrix, since every direct total-protein method is excluded and Ph. Eur. 2.5.33 Method 6
excludes Tris by name (Q-061, I-016). A cell-free-extract route feeds a whole proteome plus endotoxin
rather than one enzyme, which raises the burden again (R-017). A chromatographic fallback is
retained.

The one mechanistically coherent filtration-only architecture identified runs the *other* way round:
proteolysis first would **manufacture** the mass gap, leaving a 14–17 kDa product retained on a
5–8 kDa membrane while ~1–3 kDa peptides diafilter out. It is recursive — Proteinase K is itself
about 40 kDa, so the protease becomes the next residual protein — and nothing retrieved measures
peptide passage for our pair, which is the experiment Q-032 should be asking for.

## GMP sourcing

GMP-grade T4 ligases are commercially listed; the high-performance engineered dsRNA ligases and
PNKs are proprietary to the platform owners. Recombinant *E. coli* expression is animal-free;
endotoxin-controlled strains exist (<span class="prov-fact">fact</span>). Residual-enzyme
acceptance criteria specific to GMP siRNA ligation are a gap.
