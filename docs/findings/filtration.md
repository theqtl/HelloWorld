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
- Ultrafiltration fractionation needs the two species to differ by roughly an order of
  magnitude in molecular weight, and the practical resolution band is about ±50% of the
  membrane cut-off (<span class="prov-fact">fact</span>, general UF; Sigma/USPTO 6187190 via
  [SRC-ZYDNEY-2024](../registers/sources.md) reading list). A 5% difference is far inside a
  single membrane's cut.
- Charge separation is also marginal: n-1 differs by one internucleotide linkage on a 20-plus
  charge polyanion, ~4–5% of the charge (<span class="prov-inference">inference</span>).

So **no filtration mode — ultrafiltration, nanofiltration, or a charged membrane adsorber —
resolves block-internal n-1 from full-length.** The same limit applies to the adenylylated
dead-end species (differs by ~AMP, ~329 Da) and to n+1/addition variants.

## 2. Not all length variants are equal

The key move is to split "length variants" into two classes that behave completely differently
under filtration (<span class="prov-inference">inference</span>, grounded in block-prep and
membrane data):

| Impurity class | Size difference vs product | Filtration verdict |
|---|---|---|
| **Block-internal n-1 / n+1** | ~1 nt in ~21 (~5%) | **Cannot be cleared** by size or charge. |
| **Unreacted blocks & partial ligation products** | a whole block (3–10 nt in 21) | **Clearable** by UF/DF (and NF for the very short ones). |
| Adenylylated dead-end (AppN) | ~1 residue | Cannot be cleared; control at the reaction. |
| ATP / AMP / PPi / Mg²⁺ / salts | << 1 kDa | **Cleared** by diafiltration — the workhorse. |
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
exists for siRNA blockmer ligation), but it is grounded in cited component values and in a
direct empirical observation that ~5% of fragment-internal impurity is carried into the ligated
product (<span class="prov-fact">fact</span>, analytical scale, modified/PS oligo;
[SRC-NATCOMM-2024](../registers/sources.md)).

Worked example (<span class="prov-inference">inference</span>; inputs are cited facts):

- A 21-mer from **3 blocks of ~7 nt**, each 90–95% full-length (fragment purities reported at
  0.3–3 kg scale for modified gapmer chemistry, <span class="prov-fact">fact</span>,
  [SRC-ZHOU-2022](../registers/sources.md)):
  \(0.90^3 = 72.9\%\) to \(0.95^3 = 85.7\%\) internal-limited full-length, **before any final
  polish**.
- Compare linear solid-phase synthesis of a 21-mer at 98.5% coupling: \(0.985^{20} = 74\%\)
  crude full-length (<span class="prov-fact">fact</span>, model, [SRC-ATDBIO-SPOS](../registers/sources.md)).

The block-ligation route lands similar-to-better on internal full-length content, **and** its
dominant discardable impurities (unreacted blocks, partials) differ by a whole block, so
filtration removes them cleanly.

The crucial corollary: the single-nucleotide resolution that filtration cannot do is done at the
**block stage**, on short blocks, where one nucleotide is a much larger fractional difference
(1 in 7 versus 1 in 21) and anion-exchange or RP-HPLC resolves it (<span class="prov-fact">fact</span>,
principle; [SRC-ATDBIO-PUR](../registers/sources.md)). That chromatography sits at the **block
supplier, outside our DS facility boundary.** Inside the filtration-led facility, no
single-nucleotide separation is attempted.

## 4. The enzyme: immobilisation is the linchpin

Soluble ligase (tens of kDa) is *larger* than the 7 kDa strand, so size ultrafiltration cannot
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
   *internal-limited* purity at \(\prod f_i\) (~73–86% for 3 blocks at 90–95%). Whether that
   **meets spec** depends on the spec (next point).
3. **What would have to move for the filtration-only case to close?** Either the block
   full-length purity rises (fewer, purer blocks — 2 blocks at 97% gives ~94%), or the DS
   full-length specification sits at or below the achievable floor. Public guidance is ≥80% by
   LC with a 1% single-impurity characterisation threshold (<span class="prov-fact">fact</span>,
   non-ICH; [SRC-AMVUTRA-EPAR](../registers/sources.md) and USP/FDA), but the actual approved-siRNA
   numeric limits are **redacted**, so this is open — question **Q-033**.
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
per-strand chromatographic polish. Which of the two applies is decided by the real DS
specification (Q-033) and the achievable block purity (Q-011) — not by filtration physics, which
is unambiguous. The biggest technical risk to the thesis is not n-1 at all; it is proving
**enzyme clearance by filtration** at scale (R-002).

!!! warning "Evidence quality"
    Almost no quantitative data is specific to a fully modified 21-mer siRNA at scale. Membrane
    flux figures are protein/pDNA/mRNA surrogates; the strongest oligo-specific UF source is
    abstract-only. Block purities are from modified gapmer chemistry. Conversions span an
    abstract range (40–80%) to vendor claims (>95%). Treat the direction as firm and the numbers
    as provisional. See the [reading list](../sources/reading-list.md).
