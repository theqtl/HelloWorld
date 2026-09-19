# Does the filtration-led train close?

**Short answer:** Yes for most of the impurity burden, and the hardest separation is designed
out or pushed upstream — **but only conditionally.** A filtration-only DS train (ligation
onward) closes **if** two upstream conditions hold: block-stage purity is high, and the DS
full-length specification is no tighter than the purity floor set by the blocks. The single
nucleotide problem is not solved by filtration; it is solved by controlling impurities where
they are created. Where that is not enough, the minimum necessary chromatography is a single
final polish on each single strand, and everything else stays filtration-based.

This is the finding the brief most wanted, so the reasoning is laid out in full, with evidence
and its scale, and the negatives stated plainly.

## 1. The physical fact that frames everything

Filtration separates by size, charge, and binding. It does not separate by one nucleotide.

- A product strand is about 7 kDa (21-mer); an n-1 deletion differs by about one residue,
  ~330 Da, which is ~4.7% of the strand mass (parameters `P-MW-STRAND`, `P-DMW-N1`,
  <span class="prov-inference">inference</span> from standard residue masses).
- Ultrafiltration fractionation needs the two species to differ substantially in molecular
  weight. The published thresholds are stricter than a single round number: conventional multistage
  ultrafiltration is described as **grossly inefficient below a molecular-weight ratio of about
  five** (<span class="prov-fact">fact</span>; [SRC-US7497950](../registers/sources.md)), and the
  classical statement for clean fractionation is a difference of around two orders of magnitude.
  An n-1 deletion sits at a ratio of about **1.05**, far below every threshold in the literature.
- The cut is not sharp either. A molecular-weight cut-off is conventionally the molecular weight at
  90% rejection; an ideal membrane would cut sharply because its pores are uniform, but real
  membranes have broad pore-size distributions and correspondingly blurred cut-offs
  (<span class="prov-fact">fact</span>; [SRC-MWCO-REVIEW-2024](../registers/sources.md)).
- Charge separation is also marginal: n-1 differs by one internucleotide linkage on a 20-plus
  charge polyanion, ~4–5% of the charge (<span class="prov-inference">inference</span>).

So **no filtration mode — ultrafiltration, nanofiltration, or a charged membrane adsorber —
resolves block-internal n-1 from full-length.** The same limit applies to the adenylylated
dead-end species and to n+1/addition variants. (On the adenylylated species: adenylylation adds
about 329 Da (<span class="prov-inference">inference</span>) to the **5'-phosphorylated donor
fragment**. That dead-end fragment is far smaller than
the ligated product and its separation problem is a partial-product problem, not an n-1 problem;
what keeps it uncontrollable downstream is that suppressing it belongs at the reaction. The dead end
has now been observed directly in fully modified siRNA blockmer ligation
([SRC-ALMAC-2023](../registers/sources.md), the "[+AMP]" by-product), where the authors' fix was to
restage the reaction so it does not form — not to remove it downstream; the mechanism and its ATP
dependence are in [SRC-PBCV1-2014](../registers/sources.md), which states no mass difference.)

## 2. Not all length variants are equal

The key move is to split "length variants" into two classes that behave completely differently
under filtration (<span class="prov-inference">inference</span>, grounded in block-prep and
membrane data):

| Impurity class | Size difference vs product | Filtration verdict |
|---|---|---|
| **Block-internal n-1 / n+1** | ~1 nt in ~21 (~5%) | **Cannot be cleared** by size or charge. |
| **Unreacted blocks & partial ligation products** | a whole block (3–10 nt in 21) | **Clearable** by UF/DF (and NF for the very short ones). |
| Adenylylated dead-end (AppN) | ~1 residue | Cannot be cleared; control at the reaction. |
| ATP / AMP / PPi / monovalent salts | << 1 kDa | **Cleared** by diafiltration — the workhorse. |
| Divalent cations (Mg²⁺ / Ca²⁺) | << 1 kDa but charge-bound | **Not reliably** — they bind the polyanion and resist diafiltration (R-014). |
| Ligase protein | larger than the strand | Not by size UF in solution; **immobilise the enzyme** (see §4). |
| Splint oligo | same chemistry as product | Not by filtration; **designed out** (see §5). |
| Endotoxin (LPS micelles ~10³ kDa) | co-retained with product | UF is counter-productive; use adsorber (unproven for oligo). |
| Aggregates / particulates / bioburden | > 0.2 µm | **Cleared** by depth / sterilising filtration. |

The full matrix with quantitative bases and sources is in the
[filtration process page](../process/filtration.md).

So filtration does clear the ligation-derived species, the small solutes, and the
particulate/bioburden load. What it cannot do is the single-nucleotide job.

## 3. Control at creation: the purity floor

Because block-internal n-1 cannot be removed downstream, the achievable full-length purity is
**floored by the blocks themselves**. If a strand is assembled from \(k\) blocks with
full-length fractions \(f_1 \dots f_k\), the internal-limited full-length ceiling of the
isolated product is:

\[
P_{\text{FL}} \;\approx\; \prod_{i=1}^{k} f_i
\]

with terms defined in [Equations](../equations/index.md) (`EQ-PURITY`). This is
<span class="prov-inference">inference</span> (our synthesis; no published closed-form model
exists for siRNA blockmer ligation), but it is grounded in cited component values, in a
direct empirical observation that ~5% of fragment-internal impurity is carried into the ligated
product (<span class="prov-fact">fact</span>, analytical scale, modified/PS oligo;
[SRC-NATCOMM-2024](../registers/sources.md)), and — the strongest support the equation has — in two
independent routes that reproduce the floor (below).

Worked example (<span class="prov-inference">inference</span>; inputs are cited facts):

- A 21-mer from **3 blocks of ~7 nt**. Measured chromatography-free purity for 4–5 nt modified blocks
  is **89–96%** at 145–258 g (<span class="prov-fact">fact</span>;
  [SRC-WO2020227618](../registers/sources.md)): \(0.89^3 = 70.5\%\) to \(0.96^3 = 88.5\%\)
  internal-limited full-length, **before any final polish**.
- Compare linear solid-phase synthesis of a 21-mer at 98.5% coupling: \(0.985^{20} = 74\%\)
  crude full-length (<span class="prov-fact">fact</span>, model, [SRC-ATDBIO-SPOS](../registers/sources.md)).

**The floor model is empirically validated, twice.** An 18-mer built from four blocks was measured at
80% purity at 200 g without chromatography, implying an effective per-block fraction of
\(0.80^{1/4}=0.946\) (<span class="prov-inference">inference</span>;
[SRC-NAR-2025](../registers/sources.md)); independently, a 1–3% per-cycle failure rate gives
\(0.97^4=0.885\) to \(0.99^4=0.961\) for a 5-mer ([SRC-US6087491](../registers/sources.md)). Both land
in the measured 89–96% band. The block-ligation route therefore lands similar-to-better on internal
full-length content, **and** its dominant discardable impurities (unreacted blocks, partials) differ
by a whole block, so filtration removes them cleanly.

Two cautions travel with the arithmetic. The block figures are MOE/DNA gapmer chemistry with a 5'-DMTr
purity handle a 5'-phosphate block lacks, and a 6-mer 2'-OMe PS oligomer measured only 81%
([SRC-KELLY-OPRD-2025](../registers/sources.md)), so 95%-class blocks are not assured in our chemistry.
And **the floor multiplies only within one analytical dimension**: it multiplies denaturing
single-strand full-length fractions and must not be used to predict a non-denaturing duplex purity,
which is a different measurement and can read higher than either strand
(<span class="prov-fact">fact</span>, method architecture;
[SRC-FDA-OXLUMO-CHEMR](../registers/sources.md)). Which dimension the specification is written in is
itself open (Q-044).

The crucial corollary: the single-nucleotide resolution that filtration cannot do is done at the
**block stage**, on short blocks, where one nucleotide is a much larger fractional difference
(1 in 7 versus 1 in 21) and anion-exchange or RP-HPLC resolves it (<span class="prov-fact">fact</span>,
principle; [SRC-ATDBIO-PUR](../registers/sources.md)). That chromatography sits at the **block
supplier, outside our DS facility boundary.** Inside the filtration-led facility, no
single-nucleotide separation is attempted.

## 4. The enzyme: immobilisation is the linchpin

Soluble ligase (tens of kDa) is *larger* than the ~7 kDa strand (`P-MW-STRAND`), so size
ultrafiltration cannot
pass the enzyme while retaining product; a charged adsorber is unreliable because the polyanionic
product competes for the sites. Conventionally, ligase removal uses affinity or ion-exchange
**chromatography** — which would break the filtration-led thesis.

The escape is **immobilised or solid-phase ligase**: the enzyme sits on a support and is removed
by filtration or centrifugation (<span class="prov-fact">fact</span> as a general principle;
stated for siRNA DS by [SRC-CODEXIS](../registers/sources.md), vendor, no clearance numbers).
This is the single most important enabling choice for a chromatography-free train, and it is
**unproven at scale for modified siRNA** — no residual-protein clearance (ppm or log) data was
found. Registered as risk **R-002** and question **Q-032**; a chromatographic enzyme-removal
fallback is kept in the concept.

## 5. The splint: designed out for siRNA

A foreign, same-chemistry splint would be nearly impossible to remove by filtration. For siRNA
this is avoided: the **complementary product strand acts as the splint**, so there is nothing
foreign to remove (<span class="prov-fact">fact</span>, vendor; [SRC-HONGENE](../registers/sources.md),
and the convergent duplex assembly of [SRC-ALMAC-2023](../registers/sources.md)). If a sacrificial
splint were ever required (e.g. a single-strand product), it would be a DNA splint removed by
DNase digestion, which adds a protein to clear. Registered as **R-006**.

## 6. Does it close? The four sub-questions answered

1. **What each mode clears, quantitatively** — see the matrix in §2 and the
   [process page](../process/filtration.md). Diafiltration clears small solutes to 99.9% at
   7 diavolumes (σ≈1); UF/DF concentrates and clears whole-block species; depth/0.2 µm clears
   particulates and bioburden. None clears n-1.
2. **Does block control + high conversion hold final purity without a polish?** It holds the
   *internal-limited* purity at \(\prod f_i\) (~70–88% for 3 blocks at 89–96%). Whether that
   **meets spec** depends on how the spec is set (next point).
3. **What would have to move for the filtration-only case to close?** The old framing — "does the
   floor beat the published number" — has no answer because **there is no such number and there is not
   meant to be one.** No published full-length percentage or single-impurity limit exists for any
   approved siRNA drug substance in any jurisdiction; regulators disclose the test methods and redact
   every acceptance criterion (<span class="prov-fact">fact</span>;
   [SRC-AMVUTRA-EPAR](../registers/sources.md), [SRC-PATISIRAN-EPAR](../registers/sources.md)). The
   criterion is instead **indexed to the applicant's own toxicology batches**: the FDA's stated
   position is that specified impurity limits must "not exceed the maximum levels observed in the
   nonclinical batches", and it ratchets downward as commercial batches accumulate
   (<span class="prov-fact">fact</span>; [SRC-FDA-OXLUMO-CHEMR](../registers/sources.md),
   [SRC-FDA-INCLISIRAN-CHEMR](../registers/sources.md)). So the question becomes **what capability the
   route demonstrates, and whether the toxicology programme can qualify what the route leaves behind.**
   A route whose floor is structurally capped near 80% does not fail against a threshold; it sets its
   own specification at its own capability and must then qualify every impurity above that level
   toxicologically rather than purify it away. The often-cited numbers are adjacent, not applicable:
   the 1.0%/1.5% identification and qualification thresholds are draft oligonucleotide guidance
   ([SRC-EMA-OLIGO-2024](../registers/sources.md)), and "≥80% full-length" is an FDA recommendation for
   **guide RNA in genome editing**, not siRNA ([SRC-FDA-CBER-2024](../registers/sources.md));
   oligonucleotides are outside ICH Q3A/Q6A scope entirely
   ([SRC-ICH-Q3A-SCOPE](../registers/sources.md)). This reframing (Q-033) is the largest single change
   this evidence dive produced.
4. **If chromatography cannot be avoided, where is the minimum?** A single final polish
   (anion-exchange or IP-RP HPLC) on each **single strand** before annealing — exactly the
   orthogonal AX + IPRP control used for an approved siRNA (<span class="prov-fact">fact</span>;
   [SRC-AMVUTRA-EPAR](../registers/sources.md)). Even then, filtration still does all buffer
   exchange, desalting, concentration, enzyme clearance (if immobilised), aggregate and bioburden
   control, and final formulation.

## 7. Bottom line

The filtration-led train is sound as the **workhorse** and closes **inside the facility** for
everything except single-nucleotide resolution. That last job is either (a) pushed to the block
supplier and held by high block purity plus high ligation conversion, or (b) met by one final
per-strand chromatographic polish. Which of the two applies is decided by the demonstrated capability
of the route against a batch-derived specification (Q-033) and the achievable block purity (Q-011) —
not by filtration physics, which is unambiguous. The biggest technical risk to the thesis is not n-1 at
all; it is proving **enzyme clearance by filtration** at scale (R-002).

**The strongest external check on the thesis cuts against it, and it must be stated plainly.** The
only named commercial practitioner of ligation-built siRNA runs **HPLC purification of the siRNA
itself in *both* of its routes** — in its own words, "P-to-P = HPLC purified fragments and purified
siRNA; C-to-P = UF/DF processed fragments and HPLC purified siRNA" — on kilogram-scale GMP batches
(<span class="prov-fact">fact</span>; [SRC-HONGENE-BROCHURE-2025](../registers/sources.md)). Filtration
there replaces *fragment* chromatography, not final-product chromatography. The honest statement is
that **no public ligation route omits final-product chromatography, so this site is ahead of
demonstrated practice at the final-purification step** (risk R-019). That is not a reason to change the
process — the physics of what filtration clears is unchanged — but it is the gap between this concept
and the current state of the art, and it belongs on the page.

!!! warning "Evidence quality"
    Almost no quantitative data is specific to a fully modified 21-mer siRNA at scale. Membrane
    flux figures are protein and plasmid-DNA surrogates; the strongest oligo-specific UF source is
    abstract-only. Block purities are from modified gapmer chemistry. **No verified conversion range
    exists for a fully modified siRNA at scale**: the 82–96% figure in the literature is a ligase
    screen on an *unmodified* shortmer, and phosphorothioate donors in that same work reacted at only
    ~30% ([SRC-NATCOMM-2024](../registers/sources.md)); the >95% figure is an unreviewed vendor claim.
    The sharpest statement is no longer "no data is specific to siRNA" but this: **no public ligation
    route omits final-product chromatography of the siRNA itself**
    ([SRC-HONGENE-BROCHURE-2025](../registers/sources.md)). Treat the direction as firm, the numbers as
    provisional, and the final-purification step as ahead of demonstrated practice. See the
    [reading list](../sources/reading-list.md).
