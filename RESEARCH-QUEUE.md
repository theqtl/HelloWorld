# Research queue — flagged findings for a future session

**Created 2026-09-18.** This file is deliberately outside `docs/` so it is not a site page and
cannot affect the strict build.

This session was scoped to evidence, not to edits. It could write only `data/sources.csv`,
`docs/sources/reading-list.md`, `gen/test_balance.py` and this file. Everything below is a change
that a future session — one allowed to edit the rest of the site — should make. **Nothing here has
been applied to the process, findings, equations, balance, facility, development, tech-transfer or
diagram pages, or to any register other than `sources.csv`.**

Every entry carries a verbatim quotation. If a claim below has no quotation, it is labelled as
inference and must not be recorded as a fact.

## How to read the confidence field

- **read in full** — the source document was opened and the quoted text read in it.
- **abstract only** — only an abstract or record summary was seen. Do not design against it.
- **inferred** — our reasoning or arithmetic on top of a sourced fact. The fact is cited; the step
  is ours.

---

# Call-outs

## A. Findings that CONTRADICT something currently on the site

| ID | What is on the site | What the evidence says |
|---|---|---|
| F-001 | The filtration-led train is presented as an achievable drug-substance architecture, with chromatography pushed to the block supplier. | The only named commercial practitioner of ligation-built siRNA runs **HPLC purification of the siRNA itself** in *both* of its routes. Filtration replaces *fragment* chromatography, not final-product chromatography. |
| F-002 | `Q-018` notes "No oligo/biologic evaporation data found". | Wiped-film evaporation of an oligonucleotide drug substance is **established practice**, with a stated maximum achieved concentration of **160 mg ASO/g solution**. |
| F-003 | The spray-drying finding makes the duplex melting temperature the governing outlet constraint. | A 21-nucleotide siRNA duplex melts at **58–64 °C**. The measured moisture-shifted glass transition of the powder is **38–53 °C**. **Tg binds first, by 5–25 °C.** |
| F-004 | `SRC-ZHOU-2022` is cited for fragments "assembled without chromatography", supporting a chromatography-free case. | The abstract says purities are suitable for clinical use **"after applying standard full-length product purification process"**, and calls eliminating it a **"potential"**. |
| F-005 | `SRC-USPTO-10640812` is registered as "Inability of T4 DNA ligase to ligate fully 2'-OMe segments". | It is **"Processes for the production of oligonucleotides"**, GlaxoSmithKline, an **engineered-ligase** patent. "Inability" also overstates it: T4 is "poor at" the job. |
| F-006 | The microbial page carries a bioburden and endotoxin ladder reproduced from a mammalian cell-culture article. | An **oligonucleotide-specific** statement exists and is open access: **"levels <1 CFU/mL demonstrate microbial control"**. |
| F-007 | `SRC-CODEXIS` supplies ">95% conversion, up to 100 g/L, >98% purity". | Traceable **only** to a marketing blog. Absent from the company's own press release and all four of its ligation patent families. |
| F-008 | The balance treats ligation conversion and step yield as broadly aligned. | Per-ligation conversion (>92%) and **overall mass yield (19–43%)** differ by an order of magnitude. |
| **F-017** | The four governing equations lean on an anonymous secondary website whose domain is six months old. | Peer-reviewed and named-author primaries now exist for all four, two of them on nucleic acids. The anonymous source is no longer needed for any of them. |
| **F-018** | `P-YLD-DRY` carries a flat 90% dryer yield. | Measured spray-dryer recoveries run **8.6–22% before optimisation and 61–89% after**, across 5 g to 400 g. A point value is indefensible. |
| **F-019** | `P-YLD-UFDF` carries 90%, justified as "TFF loss <10%" from a protein surrogate. | Loss is an **exponential function** of retention and of the combined concentration-and-diavolume term, plus an additive adsorption term and a hold-up term. At 0.99 retention it is 9.5%; at 0.999 it is 1.0%. |
| **F-020** | The microbial page implies oligonucleotide processes are intrinsically low-bioburden. | The published argument rests on two premises — synthesis runs in solvents, and only the last step is aqueous. **Neither holds for a fully aqueous enzymatic route.** |
| **F-021** | Four standards are likely cited at superseded editions in any package written before 2026. | ASME BPE-2026, ASTM E2500-25, NFPA 660-2025 (which consolidated NFPA 654) and IEC 60079-10-2:2026 are the current editions. |

## B. Findings that CLOSE an open question

| Question | Status after this dive | The answer |
|---|---|---|
| **Q-010** conversion | **Closed for per-ligation conversion**, with a caveat | >92% single-feed / >94% split-feed on fully modified blocks in continuous flow, held >100 h. Overall mass yield is 19–43%. |
| **Q-011** block purity | **Narrowed, not closed** | 89–96% measured for 4–5 nt MOE/DNA blocks at 145–258 g by precipitation alone; 81% for a 6-mer 2'-OMe PS. Nobody has published the number for short 2'-OMe/2'-F/PS blocks carrying a 5'-phosphate. |
| **Q-012** step yields | **Bounded, not closed** | Dryer 61–89% optimised (8.6–22% unoptimised); UF/DF loss is an equation, not a constant; overall ligation-route yield 19–43%. Evaporation yield remains wholly unsupported. |
| **Q-016 / Q-034** titre | **Closed at the demonstrated level** | 1 mM (~14–16 g/L) in a 1 L vessel; 10 mM "failed to go completion". 100 g/L is unsupported. |
| **Q-017** UF ceiling | **Closed at bench scale** | ~193 g/L for siRNA on a charged 10 kDa membrane; 200 mg/mL at ≥95% yield and <15 cP for an antisense oligonucleotide on 3 kDa. Viscosity is **not** what stops it. |
| **Q-018** evaporator outlet | **Closed in kind** | 160 mg ASO/g solution achieved in manufacture by thin-film evaporation. |
| **Q-020** diavolumes | **Closed for the theory, open for our stream** | Vendor tables reproduce the site's removal percentages exactly; a nucleic-acid process is documented at 4–6 diavolumes. |
| **Q-021** excipient ratio | **Closed in one direction** | Four of seven approved siRNA products contain **no weighed excipient at all**, at 160–200 mg/mL in water. Excipient in a dried matrix is therefore for the **dryer**, not for the molecule. |
| **Q-030** duplex Tm | **Closed as a bound, not for our sequence** | 58.1 °C unmodified 21-mer; 60.4–64.1 °C with 2'-F or 2'-OMe at three positions, in 100 mM NaCl. |
| **Q-031** nuclease control | **Half closed** | Modification is protective by roughly 1000-fold in plasma half-life, and protection is **positional** — end caps do not work. Nobody has measured nuclease from process bioburden in a hold. |
| **Q-033** DS specification | **Closed; confirmed closed to the public** | No published full-length percentage or single-impurity limit exists for any approved siRNA drug substance in any of five jurisdictions. The criterion is set from **the applicant's own toxicology batches** and from batch capability. |
| **Q-035** membrane cut-off | **Refuted, not closed** | The "30 kDa upper limit" is unsupported. What is quotable points the other way: **at least twice the cut-off** for robust retention, the vendor three-to-six-times rule, and 10 kDa in the only siRNA optimisation study. |
| **Q-036** flux and recovery | **Partially closed** | 40–100 mg/mL routine for oligonucleotide UF/DF; sieving <0.008 achievable. **No siRNA-specific flux number exists in anything reachable.** |
| **Q-037** bioburden/endotoxin | **Bioburden closed; endotoxin still open** | <1 CFU/mL at drug substance. The compendial floor is three orders looser. **No compendial endotoxin ladder exists** — the limit is calculated from dose, and the site's ladder is the wrong kind of quantity. |
| **Q-039** glass transition | **Closed for the constants** | Gordon–Taylor k for trehalose and water is 4.76; anhydrous trehalose is 389 K or 380 K depending on which primary you believe; anhydrous sucrose is 343 K. |
| **R-012** | **CLOSED** | Every figure on the microbial page was located verbatim in the mammalian cell-culture article, hedged there as a description of typical practice. |

## C. NEW questions and risks, not yet on any register

| Proposed | Statement |
|---|---|
| **new risk** | Falling-film **minimum wetting rate** (0.065–0.222 kg m⁻¹ s⁻¹ for water) sets a hard minimum feed per unit tube perimeter, about 65 kg/h for one 48 mm tube. A small batch must recirculate, multiplying cumulative thermal exposure. **A rotary evaporator is not a scale-down model of a falling film.** |
| **new risk** | **Magnesium and calcium bind the polyanion and can block impurity passage in diafiltration.** The ligation buffer contains magnesium chloride. |
| **new risk** | Published routes feed **cell-free extract**, so the protein burden entering purification is a whole proteome plus endotoxin, not one ligase. |
| **new risk** | A block route that **omits capping** converts coupling failures into block-internal deletions rather than truncations — the harder class. |
| **new risk** | **Dust explosion** on the dryer, cyclone and receiver. Explosion parameters on the actual powder are a testing deliverable, not a literature lookup. |
| **new risk** | No **health-based exposure limit** exists anywhere in the registers for cleaning validation of shared filtration and drying equipment. |
| **new question** | **ATP tension.** Four ligations need "at least 4 mM ATP"; suppressing the adenylylated dead end wants "<100 µM". Unresolved for a modified-siRNA system. |
| **new question** | If viscosity is only ~120 mPa·s at 500 mg/mL, **what actually sets the ultrafiltration ceiling** — osmotic pressure, or fouling? |
| **new question** | **In-line ultraviolet concentration measurement will saturate** on a 21-mer at process concentration; the path length implied is on the order of ten micrometres. The deployed answer is variable-pathlength slope spectroscopy, which is at-line. |
| **new question** | **Hold-time limits** on the aqueous intermediates. No published hold-time study exists for any oligonucleotide process. |
| **new question** | **Q-032 should be restated.** No ppm, log-reduction, immunoassay or total-protein figure for ligase clearance exists anywhere in the public record. It is not "not yet found"; it is "not publicly available". |
| **new question** | **Purity multiplies only within one analytical dimension.** Duplex purity by non-denaturing chromatography is not the product of two denaturing single-strand purities, and can read higher than either. |

---

# The queue, ordered by impact

### F-001 — Both of the only named commercial ligation routes end in HPLC purification of the siRNA itself
- Stream: A (ligation) / B (blocks)
- Type: contradiction
- Affects: `docs/findings/filtration.md` §7 and the "Evidence quality" admonition; `docs/process/filtration.md`; R-002; the whole filtration-led premise
- Source: SRC-HONGENE-BROCHURE-2025 (registered in `data/sources.csv`)
- Verbatim: "1. P-to-P = HPLC purified fragments and purified siRNA; C-to-P = UF/DF processed fragments and HPLC purified siRNA"
- Verbatim: "Importantly, we have now translated the technology to our GMP facilities where we have manufactured siRNA at kilogram scale to support clinical trials."
- Scale/system: vendor brochure naming specific GMP batches, ~960 g and ~1,020 g of 2'-OMe/2'-F PS/PO siRNA
- Confidence: read in full. The kilogram sentence, every table row and all three footnotes were independently re-extracted from the PDF and checked character for character by the lead session, not taken on the researching agent's word.
- Why it matters: the site's central claim is that filtration can carry the drug-substance train with chromatography pushed upstream to the block supplier. In the only public commercial practice, filtration *is* used that way for fragments — and the product is *still* HPLC purified. The site is not wrong about what filtration does; it is ahead of demonstrated practice about what filtration replaces.
- Proposed action: add this to `docs/findings/filtration.md` §7 as the strongest external check on the thesis, and soften the "Evidence quality" note from "no quantitative data is specific to siRNA at scale" to the sharper and now-evidenced statement that no public ligation route omits final-product chromatography. Register a new risk: "no demonstrated chromatography-free ligation drug-substance train exists in the public record."

### F-002 — Wiped-film evaporation of an oligonucleotide drug substance is established practice, contradicting the site's "no data" note
- Stream: D (evaporation), run directly by the lead session
- Type: contradiction / closes-gap
- Affects: `data/questions.csv` Q-018 (whose note reads "No oligo/biologic evaporation data found"); `docs/process/evaporation.md`; R-004; P-CONC-EVAP
- Source: SRC-PMC7415879 (Muslehiddinoglu et al., *Nucleic Acid Therapeutics* 2020, 30(4):189–197)
- Verbatim: "The maximum concentration of API solution achieved during manufacture by the authors to date is 160 mg ASO/g solution."
- Verbatim: "In addition, it is likely that TFE will achieve higher concentrations of API solution compared with UF/DF, as more viscous liquids are less likely to foul the evaporator."
- Verbatim: "The main benefits of TFE include the short residence time at elevated temperatures compared with still/pot distillation, which reduces the risk of thermal degradation."
- Scale/system: manufacturing scale, antisense oligonucleotide **solution** drug substance — a single strand, not an siRNA duplex, and not a spray-dryer feed
- Confidence: read in full, by the lead session directly
- Why it matters: the evaporation step is currently justified by analogy to dairy and fine-chemical practice with an explicit admission that no oligonucleotide precedent was found. There is one, it is open access, it was in the register the whole time marked as reachable with nobody recorded as having read it, and it supports both the choice of evaporator type and the decision to evaporate rather than push ultrafiltration further.
- Proposed action: rewrite the Q-018 note; cite this source on `docs/process/evaporation.md` as the oligonucleotide precedent; give P-CONC-EVAP a sourced anchor at 160 mg/g with the single-strand caveat stated.
- **Trap to avoid when applying this:** the paper's "time frame of a few hours" is total batch cycle time, not fluid residence time. Do not cite it as a residence time.

### F-003 — The glass transition, not the melting temperature, is the binding thermal constraint on the dried product
- Stream: E (drying), run directly by the lead session
- Type: contradiction / closes-gap
- Affects: `docs/findings/spray-drying.md` §2, §3 and §6; R-003; Q-030; Q-039
- Source: SRC-MALEK-2019 (measured Tm) against SRC-KEIL-2021 (measured Tg, already registered)
- Verbatim (Tm, Table 1): unmodified 21-nucleotide siRNA duplex "Tm = 58.1°C"; with 2'-F at three guide positions 64.1 °C; with 2'-OMe 61.2 °C
- Verbatim: "Tm values of duplexes increased upon incorporation of modified ribouridines and 4'-OMe-dT (+1 °C/nt to 2 °C/nt), whereas a slight decrease (ca. −0.3 °C/nt to 0.7 °C/nt) was observed for the arabinose modifications."
- Verbatim (conditions): "a buffer containing 10 mM sodium phosphate (pH 7.2) with 100 mM NaCl and 0.1 mM EDTA"
- Scale/system: bench UV thermal denaturation; 21-nucleotide siRNA duplexes with three modified positions — not a fully modified duplex, and not our sequence
- Confidence: read in full, by the lead session directly
- Why it matters: the drying finding is built around "keep the outlet below Tm". Against a measured moisture-shifted glass transition of 38–53 °C, a duplex melting at 58–64 °C is not the constraint that binds. The Tm rule is necessary but not sufficient, and the real design limit sits 5–25 °C lower and applies to storage as well as drying.
- Proposed action: reorder §2 and §3 of the drying finding so the glass transition leads and the melting temperature follows as the looser of the two limits; re-rank Q-039 above Q-030; restate R-003's mitigation to lead with residual-moisture control.
- **An extrapolation that must not be made:** +1 to +2 °C per modified nucleotide was measured over three positions. Multiplying it across twenty-one positions to claim a fully modified duplex melts near 100 °C is unsupported. Add it to "claims to not repeat".

### F-004 — "Assembled without chromatography" is chromatography-free assembly, not a chromatography-free drug substance
- Stream: B (blocks)
- Type: contradiction
- Affects: `docs/findings/filtration.md` §3 worked example; `docs/process/blocks.md`; Q-011
- Source: SRC-ZHOU-2022
- Verbatim (abstract): "Critical impurities are controlled in the fragment syntheses to provide oligonucleotides of purities suitable for clinical use after applying standard full-length product purification process. Impurity control in the assembly steps demonstrated the potential to eliminate chromatography of full-length oligonucleotides, which should enhance scalability and reduce the environmental impact of the process."
- Scale/system: 18-mer MOE/DNA gapmer, fragments at 0.3–3 kg per batch
- Confidence: abstract only — the full text is genuinely closed, verified across five independent indexes rather than assumed
- Why it matters: the site leans on this paper for the proposition that a block route can dispense with chromatography. The paper's own abstract says the opposite about the full-length product, and describes elimination only as a demonstrated potential.
- Proposed action: split the claim in two wherever this source is cited, and correct the page range to 2087–2110.

### F-005 — A registered source carries the wrong title, assignee and characterisation
- Stream: A (ligation), confirmed by the lead session
- Type: source-upgrade / contradiction
- Affects: `data/sources.csv` row SRC-USPTO-10640812 (the `citation` field, which was outside this session's write scope); `docs/process/ligation.md`
- Source: SRC-USPTO-10640812, read in full at Google Patents
- Verbatim: "Wild-type T4 DNA ligase is poor at ligating 2′-OMe substituted oligonucleotide segments, but slightly less sensitive to modification of the 5′ oligonucleotide segment than the 3′ segment."
- Verbatim: "Chlorella virus DNA ligase (SEQ ID NO:29, commercially available as SplintR® ligase, NEB) was able to ligate modified oligonucleotide segments"
- Scale/system: patent; bench examples at 20 µM segment concentration, roughly 0.14 g/L
- Confidence: read in full, by the lead session directly
- Why it matters: the row is registered as a negative result about T4. It is actually GlaxoSmithKline's engineered-ligase patent, "Processes for the production of oligonucleotides", inventors Crameri, Hill and Tew, granted 2020-05-05. That is far more useful to this project than the negative result it was filed under — and the negative result itself is overstated, since the patent says "poor at", not "unable".
- Proposed action: correct the `citation` field to the true title and assignee; rewrite the ligation page's use of it from "T4 cannot" to "T4 is poor at, and these engineered alternatives can". Note the patent reports **no** conversion, yield or purity percentage anywhere — peak areas only — so it does not close Q-010.

### F-006 — An oligonucleotide-specific bioburden statement exists and should replace the cell-culture ladder
- Stream: F (microbial), found by the lead session while reading a register row nobody had opened
- Type: closes-gap / contradiction
- Affects: `docs/process/microbial.md`; Q-037; R-009; R-012
- Source: SRC-PMC7415879
- Verbatim: "During the drug substance manufacturing process, levels <1 CFU/mL demonstrate microbial control if bioburden reduction is performed before the sterile filtration step in DP manufacturing but higher levels may be justifiable on a case-by-case basis."
- Verbatim: "Frozen conditions are not conducive to microbial growth in API, and pre-sterilized modern drug substance primary containers are well designed to maintain closure integrity over the range of conditions anticipated during storage and shipping."
- Scale/system: oligonucleotide drug substance manufacture, solution API
- Confidence: read in full, by the lead session directly
- Why it matters: R-012 says the site's microbial numbers are carried over from mammalian cell culture and are unverified for an oligonucleotide. Here is an oligonucleotide-specific number, peer reviewed and open access.
- Proposed action: replace the ladder on the microbial page with this figure, **stated as what it is** — a statement of practice with an explicit case-by-case caveat, not a pharmacopoeial limit and not a specification. Keep R-012 open for the **endotoxin** half, because this paper states no numeric endotoxin limit.

### F-007 — The vendor conversion, loading and purity trio is marketing-only
- Stream: A (ligation)
- Type: contradiction
- Affects: `docs/process/ligation.md`; P-LIG-CONV; P-CONC-LIG; Q-010; Q-016; Q-034
- Sources: SRC-CODEXIS-PR-2024 and SRC-CODEXIS-PATENTS
- Verbatim (the press release's only numeric claim, and it is a different chemistry): "Achieved incorporation efficiency of >98% during sequential enzymatic oligo synthesis"
- Verbatim (how the patents actually report activity): "The relative percent conversion was measured as the % product of the variant relative to the % product of the reference."
- Verbatim (enzyme loading is a range, not a result): "the ligase is provided at concentrations from about 0.01 g/L to about 50 g/L"
- Scale/system: n/a — the finding is an absence
- Confidence: read in full (four patent families and the press release)
- Why it matters: ">95% conversion, up to 100 g/L, >98% purity" is doing real work on the ligation page and in the balance. It is corroborated nowhere, including by the company that said it.
- Proposed action: down-weight every use to "unverified vendor claim, basis unstated"; replace the design anchor with the measured 1 mM titre from SRC-ALMAC-2023 and the >92% flow conversion from SRC-CN119265174.

### F-008 — Per-ligation conversion and overall mass yield differ by an order of magnitude and must never be conflated
- Stream: A (ligation)
- Type: new-number / contradiction
- Affects: `gen/balance.py` inputs via `data/parameters.csv` (P-YLD-LIG and related); Q-012; `docs/balance/index.md`
- Sources: SRC-HONGENE-BROCHURE-2025 (overall) and SRC-CN119265174 (per-ligation)
- Verbatim (overall): table rows "Inclisiran siRNA … P-to-P 26% 97%", "Divalent siRNA … P-to-P 19% 97%", "C-to-P siRNA … C-to-P 43% 96%"
- Verbatim (the yield definition, which is conservative and must travel with the number): "2. Unoptimized yields based on theoretical MEC, calculated from lowest yielding fragment"
- Verbatim (per-ligation): "the product conversion rate reaches over 92%, and the sample can be continuously operated for over 100 hours without reduction of the conversion rate"
- Scale/system: overall yields are vendor GMP campaign figures on ~1 kg batches; the >92% is a 5 mL packed-bed flow column at 600 µM
- Confidence: read in full; the vendor table independently re-extracted and checked by the lead session
- Why it matters: a balance that takes >92% as a step yield will overstate drug substance out of the ligation section by roughly two to four times against the only published campaign figures.
- Proposed action: separate the two quantities explicitly in `data/parameters.csv` — a per-ligation conversion parameter and an overall-yield parameter — and re-run the balance. State the vendor yield definition wherever the 19–43% band is used.

### F-009 — Minimum wetting rate makes the evaporator turndown-limited, which is a new risk
- Stream: D (evaporation), run directly by the lead session
- Type: new-risk / new-number
- Affects: `docs/process/evaporation.md`; `data/equipment.csv` evaporator sizing; R-004
- Source: SRC-HUGHES-2024 (open access, read in full), reporting SRC-MORISON-2006 (genuinely closed, verified via Unpaywall, registered for the provenance chain)
- Verbatim: "Values of minimum wetting rate that have been reported in the literature for water on a vertical steel surface are presented in terms of the mass flowrate per unit width of surface (Γ*)."
- Verbatim: "Morison et al. [18] obtained a value of 0.104 kg m-1 s-1 for water at both 25 ⁰C and 60 ⁰C."
- Verbatim: "Morison and Tandon [23] obtained values of Γ* that decreased from 0.16 kg m-1 s-1 to 0.12 kg m-1 s-1 as the water temperature increased from 20 ⁰C to 70 ⁰C."
- Scale/system: water and simple aqueous solutions on stainless steel, laboratory and pilot tube rigs — not a polyelectrolyte solution. Surface tension and contact angle dominate, so transfer is plausible but unproven.
- Confidence: read in full for the reporting source; the primary is record-only and no number is attributed directly to it
- Why it matters (partly inferred, and the inference is ours): below the minimum wetting rate the film breaks into rivulets, heat transfer collapses and dry patches foul. For a single 48 mm internal-diameter tube the wetted perimeter is 0.151 m, so the minimum feed is about 57 kg/h **for one tube**. A small pharmaceutical batch therefore cannot run single-pass; it must recirculate, which multiplies the number of passes and so the cumulative thermal exposure — the exact quantity R-004 is about. Dimensions checked by hand: [kg m⁻¹ s⁻¹] × [m] = [kg s⁻¹].
- Proposed action: register a new risk for evaporator turndown at small batch size; add minimum wetting rate to the evaporator sizing basis in `data/equipment.csv`; restate R-004 in terms of cumulative passes rather than a single pass.

### F-010 — The ATP requirement and the ATP ceiling for suppressing the dead-end species are in direct tension
- Stream: A (ligation)
- Type: new-question
- Affects: `docs/process/ligation.md`; R-010; Q-010; `data/buffers.csv` ligation buffer
- Sources: SRC-WO2025262452 (requirement), SRC-PBCV1-2014 (ceiling), SRC-ALMAC-2023 (what is actually run)
- Verbatim (requirement): "to process 1 mM substrate, at least 4 mM ATP is required. In reality, an excess of ATP is necessary to achieve complete ligation of the substrate."
- Verbatim (ceiling): "Abortive adenylylation was suppressed at low ATP concentrations (<100 µM) and pH >8, leading to increased product yields."
- Verbatim (regeneration has its own ceiling): "the reaction reached equilibrium with a maximum of 66 % conversion to ATP (Fig. 2), which is consistent with previous reports."
- Scale/system: the requirement is a modified GalNAc-siRNA at 1 mM, bench. **The <100 µM ceiling is bench-scale unmodified DNA on RNA splints with DNA ligases — the mechanism transfers, the number does not.**
- Confidence: read in full for all three
- Why it matters: four ligations need millimolar ATP; suppressing the adenylylated dead end wants sub-100-micromolar. R-010 says this species cannot be filtered out, so it must be controlled at the reaction — and the two requirements pull in opposite directions. No public source resolves it for a modified-siRNA system.
- Proposed action: register as a new question. Note the inference (ours) that an ATP-limited fed-batch, or regeneration from AMP which by construction holds free ATP low, is the mechanistically indicated route — neither patent says this.

### F-011 — The adenylylated dead end has been directly observed in exactly this chemistry
- Stream: A (ligation)
- Type: closes-gap
- Affects: R-010; `docs/findings/filtration.md` §1 and §2; `docs/process/ligation.md`
- Source: SRC-ALMAC-2023, Table 1
- Verbatim (Table 1 by-product entry): "2.3_2.4[+AMP]"
- Verbatim (footnote): "An underscore designates a ligation product between blockmers. Structure for observed by-products are detailed in Supporting Information as deduced from MS analysis."
- Verbatim (how the authors dealt with it): "The results show clean formation of the sense and antisense strand, with none of the by-products observed from the individual ligation site screening."
- Scale/system: bench screening at 0.1 mM blockmer, fully modified siRNA blockmers — transfers in kind
- Confidence: read in full; the table entry re-extracted from the PDF and confirmed character for character by the lead session
- Why it matters: R-010 is currently supported only by a source in unmodified DNA. It is now observed in a fully modified siRNA system, and the authors' mitigation was to change the disconnection and reaction staging so the species does not form — not to remove it downstream. That is exactly the control philosophy R-010 asserts.
- Proposed action: re-point R-010's `source_key` to SRC-ALMAC-2023 and cite the by-product entry directly.

### F-012 — Measured block purities: 89–96% for 4–5 nt modified blocks, and what chromatography adds
- Stream: B (blocks)
- Type: new-number / closes-gap (partially)
- Affects: P-BLOCK-PUR; Q-011; `docs/findings/filtration.md` §3; `docs/process/blocks.md`; R-001
- Source: SRC-WO2020227618 (free full text; 7 of the 9 authors of SRC-ZHOU-2022 are inventors)
- Verbatim: "deoxy- TTACC 5mer (145.5 g, 57.8 mmol, 92.4% yield, 93.6% purity) was obtained as a white solid."
- Verbatim: "Compound 3-5 (UTTC 4mer) (258 g, 134 mmol, 89.0% yield, 95.6% purity) was obtained as a light yellow solid."
- Verbatim (what one chromatographic step adds): "Compound 7-3-5 (30.0 g, 13.4 mmol, 95.7% yield, 81.6% purity) was obtained as a white solid. The crude product was purified by reversed-phase HPLC (pH=7 condition). Compound 7-3-5 (24.0 g, 13.0 mmol, 96.9% yield, 98.8% purity) was obtained as a white solid."
- Scale/system: liquid phase, 145–258 g isolated blocks; 2'-MOE + DNA gapmer with mixed PS/PO; 4- and 5-mer blocks carrying a 5'-DMTr, **which is itself a purity handle that a 5'-phosphate block does not have**. The word "kg" does not appear in this patent.
- Confidence: read in full
- Why it matters: P-BLOCK-PUR is currently a summary figure from an unread paper. Here are the measured, chromatography-free, hectogram-scale numbers behind it — and the quantification of what a single preparative chromatography step adds (81–87% to 98–99% at 90–98% recovery), which is the selectivity a filtration-only train forgoes.
- Proposed action: re-anchor P-BLOCK-PUR to this source with the chemistry caveat; add the crude-versus-polished comparison to the filtration finding as the quantitative answer to "what does chromatography do that filtration cannot".

### F-013 — Two independent routes converge on the same block-purity floor
- Stream: B (blocks)
- Type: closes-gap (model validation)
- Affects: `EQ-PURITY`; `gen/balance.py` `purity_floor`; Q-011; R-001
- Sources: SRC-NAR-2025 (measured assembly), SRC-US6087491 (per-cycle failure rate), SRC-WO2020227618 (measured blocks)
- Verbatim (measured assembly): "After treatment with concentrated ammonia, the 5′-DMTr-protected 18-mer product … was obtained at a scale of 200 g with a yield of 49% and a purity of 80% without the need for chromatography."
- Verbatim (per-cycle failure): "1-3% of the reactions fail during each cycle in which a nucleotide monomer is to be added … in a typical 20mer synthesis, the 20mer product represents only 50-80% of the recovered oligonucleotide product."
- Scale/system: 200 g assembly of an 18-mer from four blocks; the per-cycle figure is 1990s solid-phase DNA phosphorothioate
- Confidence: read in full
- Why it matters (the arithmetic is ours, and it is labelled as inference): 18 = 4+5+4+5, so four blocks. The measured 80% assembled purity implies an effective per-block full-length fraction of 0.80^(1/4) = 0.946, which sits inside the measured 89–96% block band. Separately, applying the 1–3% per-cycle failure rate to a 5-mer gives 0.97⁴ = 0.885 to 0.99⁴ = 0.961 — the same band from a completely different direction. **The multiplicative purity-floor model reproduces a real measured assembly to within a point or two.** That is the strongest quantitative validation the site's core equation has.
- Proposed action: cite this as empirical validation of `EQ-PURITY` on the filtration finding and the equations page. State the caveat: 80% is the purity of the *protected* 18-mer by the paper's own assay, and chemical coupling is not enzymatic ligation.

### F-014 — The drug-substance purity specification is derived from batch capability, not from a fixed threshold
- Stream: B (blocks) and G (regulatory)
- Type: closes-gap
- Affects: Q-033; `docs/findings/filtration.md` §6 point 3; `docs/process/blocks.md`
- Sources: SRC-PATISIRAN-EPAR and SRC-FDA-INCLISIRAN-CHEMR
- Verbatim (FDA): "The current drug product specification for purity and impurity content is based on the upper confidence limit (mean ± 3SD) derived from limited batch release data available for drug substance batches used in the original submission."
- Verbatim (EMA): "the applicant re-evaluated the specifications for duplex purity, sodium content and pH based on ±3SD ranges instead of TI approach."
- Verbatim (what the specification contains): "The active substance specification includes tests for visual appearance, identification by duplex retention time (SE-HPLC UV), identification by molecular mass (IPRP-HPLC MS), identification by Tm(UV Spectrophotometry (Thermal)), sodium content (Flame AAS), impurities (SE-HPLC UV and AX-HPLC UV), assay (AX-HPLC UV), pH (Ph. Eur.), water content (KF), elemental impurities (ICP-MS), residual solvents(GC), bacterial endotoxins (Ph. Eur.) and bioburden (Ph. Eur.)."
- Scale/system: two approved commercial siRNA drug substances, two jurisdictions
- Confidence: read in full, numerically redacted in both
- Why it matters: Q-033 asks what the real specification is, and the filtration finding says it is "the single input that decides whether the filtration-only case closes". The answer is that there is no fixed public number and there is not meant to be one: the criterion is set from demonstrated batch capability and tightened as batches accumulate.
- Proposed action: rewrite Q-033's framing from "what is the number" to "the number is process-capability-derived, so the question becomes what capability the route demonstrates". This substantially changes the logic of the filtration finding's §6 point 3 — a route whose floor is 80% would set a spec near 80% and then have to qualify its impurities toxicologically rather than purify them away.
- **Kill on sight:** a claim that the FDA inclisiran chemistry review states purity "exceeds 85% full-length product by HPLC". The 94-page review was read in full and contains no such sentence and no unredacted purity number.

### F-015 — Naked siRNA survives atomisation; the shear worry belongs to plasmid DNA
- Stream: E (drying), run directly by the lead session
- Type: closes-gap
- Affects: R-003; `docs/findings/spray-drying.md` §1 and §4; `docs/process/spray-drying.md`
- Source: SRC-NAKED-NA-2023 (Okuda et al., *Pharmaceutics* 2023, 15(12):2786) — a register row previously carrying only the note "Powder-formation stress on nucleic acids", with no read recorded
- Verbatim: "the relative band intensity for siGL3 was more than 80% after all the physical treatments investigated"
- Verbatim: "siGL3 after all the physical treatments investigated exhibited the almost equivalent suppression of Fluc expression to fresh siGL3 (10–20% of Control)"
- Verbatim (the contrast): "Fluc expression for pDNA treated with sonication, heating at 60 and 90 °C, atomization, or lyophilization was less than 25% of that for fresh pDNA"
- Scale/system: 80 µg of nucleic acid in 4 mL, laboratory spray dryer, **naked** siRNA and naked plasmid DNA; a standard research duplex, not a heavily modified therapeutic siRNA, and micrograms rather than kilograms
- Confidence: read in full, by the lead session directly
- Why it matters: this is the first naked-siRNA drying evidence in the register — the existing drying source is a polyplex formulation. It separates the shear risk cleanly: a plasmid is damaged by atomisation, a short duplex is not.
- Proposed action: cite on the drying finding to retire atomisation shear as a governing risk and refocus R-003 entirely on temperature and the glass transition.

### F-016 — RETRACTED BY THIS SESSION: the site's diafiltration equation is correct, and the reconciliation note it already carries can now be closed
- Stream: C (membranes)
- Type: source-upgrade
- Affects: `docs/equations/index.md`, `EQ-DIAF` and `EQ-SIEVE`; Q-020
- **Correction, recorded openly because it is the exact failure mode this dive exists to prevent.** This
  entry was first written as a contradiction, on a research stream's report that the site states
  diafiltration clearance as an exponential in `N(1−σ)` with σ called the sieving coefficient. **I then
  opened `docs/equations/index.md` and that is not what it says.** The page states
  `C/C₀ = e^{−σN}` with σ defined as "sieving coefficient (0 fully retained … 1 freely permeable)",
  which is the correct pairing. It already carries the note: "the field-standard form uses
  \(e^{-\sigma N}\); an alternative \(e^{-N(1-\sigma)}\) appears with a retentate-basis σ —
  reconcile the σ definition before use." **There is no defect. No edit to the equation is required.**
  The finding was written against a paraphrase rather than the page, and it should never have been
  entered as a contradiction.
- Sources: SRC-NOURAFKAN-2024 and SRC-KELLY-OPRD-2025 (peer-reviewed primaries, both on nucleic acids), corroborated numerically by SRC-PALL-TFF
- Verbatim (the numeric check, from the vendor diavolume table): "1 63.2 50.0 / 2 86.5 75.0 / 3 95.0 87.5 / 4 98.2 93.8 / 5 99.3 96.9 / 6 99.8 98.4 / 7 99.9 99.2"
- Scale/system: generic ultrafiltration theory; two of the three sources apply the relation to a nucleic acid
- Confidence: read in full for all three sources, and the site page verified directly
- Why it still matters: the page's own caveat says "reconcile the σ definition before use", and it can now
  be closed. The continuous column of the vendor table reproduces the page's 5 and 7 diavolume figures
  exactly, which confirms the page's form and its numbers together. The complementary form **is** a live
  trap in the wider literature, so it is worth stating the relationship explicitly rather than only
  warning about it.
- Proposed action: keep `EQ-DIAF` as written. Replace the "reconcile before use" caveat with the closed
  statement, cite the two primaries, and cross-reference `EQ-SIEVE` so the complement relation is on the
  page next to the equation that depends on it. Do **not** change the formula or the symbol definition.

### F-017 — Primary sources now exist for all four governing equations, so the anonymous secondary can be retired
- Stream: C (membranes)
- Type: source-upgrade
- Affects: `docs/equations/index.md`, `EQ-DIAF`, `EQ-FLUX`, `EQ-AREA`; `docs/process/filtration.md`; SRC-BPT-TFF
- Sources: diafiltration clearance — SRC-NOURAFKAN-2024 and SRC-KELLY-OPRD-2025; gel-polarisation flux — SRC-SCHWARTZ-BPI-2003 with SRC-BIESHEUVEL-2024 as corroboration; area sizing — SRC-PALL-TFF; sieving and observed rejection — four consistent primaries
- Verbatim (the cut-off rule, which the site does not currently carry at all): "As a general rule, the molecular weight cut-off (MWCO) of a membrane should be a third to a sixth the molecular weight of the molecule to be retained. This is known as the 3–6 × Rule, which ensures complete retention."
- Scale/system: general membrane theory; two of the four sources apply the equations to a nucleic acid
- Confidence: read in full
- Why it matters: the site's four governing equations currently lean on an anonymous, organisation-attributed website with no named author whose domain was registered six months ago. That is now unnecessary for every one of them.
- Proposed action: re-cite all four equations to the primaries and demote SRC-BPT-TFF to a "see also". **Do not** re-cite the gel-polarisation source for process time: it prints "Process Time = Filtrate Flow Rate × Volume", which is litres per hour times litres, and is not a time. Two further traps recorded during this dive: an open-access review prints the film-theory equation without its logarithm, and the complementary sieving/rejection form is a live trap in the literature, though the site itself states the equation correctly (see F-016, which was retracted after checking the page).

### F-018 — The spray-dryer step yield is not a constant and the registered value is indefensible
- Stream: H (scale-up)
- Type: contradiction / new-number
- Affects: `data/parameters.csv` P-YLD-DRY; Q-012; `docs/balance/index.md`; `docs/process/spray-drying.md`
- Source: SRC-KAPIL-2025
- Verbatim: "Optimized yields of 61%–89% for a sticky product were achieved for 5–400 g with suitable dryness (1%–5% residual solvent)."
- Verbatim: "The optimized Procept 100 g scale conditions were transferred to FluidAir (30–400 g) and initial conditions yielded low recovery (8.6%)."
- Verbatim: "After optimized yield of 87% was observed at 5 g scale, the conditions were tested at 100 g scale and demonstrated comparable yield (87%)."
- Scale/system: three dryers, 5 g to 400 g, a sticky small-molecule product — **not a nucleic acid**. The yield *behaviour* transfers; the material does not.
- Confidence: read in full
- Why it matters: a flat 90% assumption sits at the top of the achievable band and nowhere near the unoptimised state a first campaign will actually see.
- Proposed action: replace the point value with a 60–90% band plus a sensitivity case, and state explicitly that optimised conditions transfer between scales while unoptimised ones do not.

### F-019 — Filtration yield loss is an equation, not a "<10%" rule of thumb
- Stream: H (scale-up), with C (membranes)
- Type: contradiction / new-number
- Affects: `data/parameters.csv` P-YLD-UFDF; `docs/equations/index.md`; Q-012; R-011
- Sources: SRC-MILLIPORE-TFF (the relation), SRC-NOURAFKAN-2024 (the measured hold-up penalty)
- Verbatim (the worked example): "consider a process where the goals are to perform a 20-fold volume concentration factor (VCF), a 7 diavolume buffer exchange, and lose less than 7% of the product to the filtrate. For this example, the natural log (ln) of the VCF is 3 and N is 7, so the value of the term (ln VCF+N) is 10."
- Verbatim (the measured hold-up loss on a real nucleic acid): "a considerable amount of mRNA loss (between 30% and 40%) … due to mRNA remaining inside both TFF tubes and filters."
- Verbatim (the discipline): "In order to understand where the product is going during a process, it is important to calculate not only yield, but also mass balance. Determine the total protein in each of the retentate, the filtrate, and the unrecoverable holdup volume."
- Scale/system: the relation is general; the adsorption figures are protein-specific; the hold-up figure is messenger RNA at 20–80 mL scale
- Confidence: read in full. Note honestly that the equation itself sits in a graphic that did not extract and was **not** reconstructed from the figure.
- Why it matters: at 0.99 retention the loss is 9.5% and at 0.999 it is 1.0% — a tenfold swing from a membrane choice. And the dominant loss at small batch size is not membrane passage at all: it is hold-up in tubing and filters, which the site's yield model does not contain a term for, and which gets worse rather than better at plant scale.
- Proposed action: turn P-YLD-UFDF into an equation with retention, concentration factor and diavolumes as named parameters, add an explicit hold-up term, and add the mass-balance requirement to the development page.

### F-020 — The "oligonucleotides are intrinsically low-bioburden" argument does not apply to this process
- Stream: F (microbial)
- Type: new-risk
- Affects: `docs/process/microbial.md`; Q-031; R-009; R-012
- Source: SRC-PMC7415879
- Verbatim: "Oligonucleotides are manufactured via solid-supported synthesis followed by chromatographic purification steps that use organic solvents and only the last step is in aqueous solutions. On the contrary, biologics are manufactured by using conditions that highly favor microbial growth such as aqueous solutions, nutrients, and neutral pH."
- Scale/system: conventional phosphoramidite manufacture with organic-solvent purification
- Confidence: read in full
- Why it matters: the published rationale for treating an oligonucleotide process as low-risk has exactly two legs, and this process has neither. It is fully aqueous with no synthesis solvents, and it has an enzyme and its buffer in the stream. That does not vindicate the mammalian ladder, but it does mean the project must justify its microbial control from its own process and cannot inherit the modality's argument.
- Proposed action: state this explicitly on the microbial page as the reason a contamination control strategy is needed rather than assumed, and register it as a new risk.

### F-021 — Four commonly cited standards are at superseded editions
- Stream: H (scale-up)
- Type: source-upgrade
- Affects: `docs/facility/index.md`; `docs/techtransfer/index.md`
- Source: SRC-STANDARDS-CURRENT, each verified against the issuing body's own catalogue page
- Scale/system: engineering and quality standards for a greenfield drug-substance facility
- Confidence: read in full, except the two cleanroom-classification standards whose content is record-only because both the issuer and the national reseller refused this environment
- Why it matters: citing a superseded standard dates a package on sight in front of an engineering firm. The bioprocessing-equipment standard, the commissioning-and-qualification practice, the combustible-dust standard and the explosive-atmospheres classification standard have all moved.
- Proposed action: update the facility and technology-transfer pages to the current editions, and add the combustible-dust standard to the facility page, noting that the explosion parameters of the actual powder are a testing deliverable rather than a literature value. Also record the two scope answers this settles: the sterile annex does not apply to a non-sterile drug substance except where the manufacturer chooses to adopt principles and documents which, and the validation annex is optional supplementary guidance for an active substance, so its three-batch expectation is a default to justify rather than a rule.

### F-022 — The drug-substance purity criterion is indexed to your own toxicology batches, which reshapes the whole filtration argument
- Stream: G (regulatory), with B (blocks)
- Type: closes-gap
- Affects: `docs/findings/filtration.md` §6 point 3 and §7; Q-033; `docs/process/blocks.md`
- Sources: SRC-FDA-OXLUMO-CHEMR, corroborated by SRC-FDA-INCLISIRAN-CHEMR and SRC-PATISIRAN-EPAR
- Verbatim: "Per Agency recommendation, the Applicant has revised drug substance specified impurity limits to not exceed the maximum levels observed in the nonclinical batches."
- Verbatim: "In compliance with the Agency recommendations, the Applicant agreed to tighten the specified and total impurity limits based on the non-clinical and clinical data for the drug substance."
- Scale/system: two approved commercial siRNA drug substances, United States; corroborated in the European assessment report for a third
- Confidence: read in full, numerically redacted throughout
- Why it matters: the filtration finding says the drug-substance specification is "the single input that decides whether the filtration-only case closes", and treats it as an unknown number to be discovered. There is no such number and there is not meant to be one. The limit is set from the applicant's own toxicology batches and ratchets downward as commercial batches accumulate. A route whose purity floor is structurally capped does not fail against a published threshold; it sets its own specification at its own capability, and then has to qualify every impurity above threshold toxicologically rather than purify it away.
- Proposed action: rewrite §6 point 3 of the filtration finding around this, and restate Q-033 from "what is the number" to "what capability does the route demonstrate, and can the toxicology programme qualify what it leaves behind". This is the largest single change to the site's reasoning that this dive produced.

### F-023 — The "30 kDa upper limit" for membrane cut-off is refuted, and what replaces it points the opposite way
- Stream: C (membranes)
- Type: contradiction / closes-gap
- Affects: Q-035; `docs/process/filtration.md`; `docs/balance/index.md`; `data/equipment.csv` membrane selection
- Sources: SRC-GRONKE-2023 (the rule), SRC-ZYDNEY-2025 (what the siRNA work actually used), SRC-SCHWARTZ-BPI-2003 and SRC-PALL-TFF (the vendor rule)
- Verbatim: "In general, the oligonucleotide should be at least twice the reported membrane molecular weight cutoff for robust retention."
- Verbatim: "Experiments were performed with surface modified composite regenerated cellulose membranes having a molecular weight cutoff (MWCO) of 10 kDa."
- Verbatim: "A good general rule is to select a membrane with a MWCO that is 3 to 6 times lower than the MW of the molecules to be retained."
- Scale/system: the first is single-strand antisense at process-development scale, read from the abstract only; the second is bench siRNA; the third is a vendor rule for proteins
- Confidence: abstract only for the first two; read in full for the vendor rule
- Why it matters: the previously asserted enumeration and its "30 kDa upper limit" could not be found in any openable source, and a plausible-looking search summary matching it was deliberately not registered. Three independent sources point the other way, to cut-offs well below the product mass. For a 17 kDa duplex the rules give an upper bound of about 8 kDa (the twice rule) or 3 to 6 kDa (the vendor rule).
- Proposed action: strike the 30 kDa figure wherever it survives, replace it with the twice rule and the three-to-six-times rule, and record that the underlying siRNA study's own cut-off enumeration is still unavailable. Q-035 stays open on that specific point.

### F-024 — Approved siRNA products contain essentially no excipient, which reframes the formulation question
- Stream: G (regulatory)
- Type: closes-gap
- Affects: Q-021; `docs/process/spray-drying.md`; `data/buffers.csv` BUF-FINAL; P-EXCIPIENT-RATIO
- Source: SRC-SIRNA-LABELS
- Verbatim (Givlaari): "containing 189 mg givosiran in a single-dose, 2-mL Type 1 glass vial… GIVLAARI is formulated in Water for Injection. Sodium hydroxide and/or phosphoric acid may have been added for pH adjustment during product manufacturing."
- Verbatim (Amvuttra): "Each 0.5 mL of solution contains 25 mg of vutrisiran (equivalent to 26.5 mg vutrisiran sodium), 0.2 mg sodium phosphate monobasic dihydrate, 0.7 mg sodium phosphate dibasic dihydrate, 3.2 mg sodium chloride"
- Scale/system: seven approved siRNA drug **products**, all liquid aqueous injectables. **No spray-dried and no lyophilised siRNA drug product has ever been approved**, so these ratios are not transferable targets for a dried matrix.
- Confidence: read in full
- Why it matters: four of the seven carry no weighed excipient at all, at 160 to 200 mg/mL in essentially pure water. The active substance therefore needs no stabilising excipient in the liquid state. Any excipient in a dried matrix exists for the drying and powder properties, not for chemical stability of the molecule.
- Proposed action: restate Q-021 from "what ratio does the molecule need" to "what ratio does the dryer need", and record on the drying page that the excipient is a process aid, not a stabiliser, with the liquid-product evidence behind it.

### F-025 — The endotoxin half of the microbial question is not closable the way the site frames it
- Stream: F (microbial)
- Type: contradiction / new-question
- Affects: `docs/process/microbial.md`; Q-037; R-007; R-012
- Sources: SRC-PMC7415879 (silent on endotoxin numbers), SRC-PHEUR-0169 (what the water figures actually are), SRC-DEVRIES-2018 (the adsorber evidence)
- Verbatim (water, and note it is not a limit): "Under normal conditions, an appropriate action level is a microbial count of 10 CFU per 100 mL when determined by filtration through a membrane with a nominal pore size not greater than 0.45 µm, using R2A agar, using at least 200 mL of water for injections in bulk and incubating at 30-35 °C for not less than 5 days."
- Verbatim (this one *is* a limit): "Bacterial endotoxins (2.6.14): less than 0.25 IU/mL."
- Verbatim (what an adsorber alone achieves against a competing polyanion): "A control using only membrane adsorbers without prior sodium hydroxide treatment showed an endotoxin concentration of 641 (±139) EU mg −1 ."
- Scale/system: pharmacopoeial water; and a bacterial polyanion on an anion-exchange membrane adsorber at laboratory to pilot scale
- Confidence: read in full; the pharmacopoeial texts were read from third-party reproductions of the printed monographs, with edition caveats recorded in the register
- Why it matters: three things at once. There is **no compendial endotoxin ladder** — the limit is calculated from dose, so it is a quantity per milligram of substance rather than per millilitre of a process stream, and the site's ladder is the wrong kind of quantity. The water figures the project carries have different status from each other and one of them is an action level, not a limit, with its method conditions forming part of the number. And the adsorber strategy behind R-007 has now been tested against a competing polyanion, where it fell two orders of magnitude short on its own.
- Proposed action: remove the endotoxin ladder entirely rather than replacing it, and derive an endotoxin limit from the intended dose instead. Restate the two water figures with their true status, the action level distinguished from the limit, and carry the method conditions with the count because a number stated without them has not stated the requirement. Keep R-007 open and add the polyanion adsorber evidence to it: the registered buffer-matrix study had nothing competing for the ligand, which is precisely the condition R-007 says will not hold for our stream.

### F-026 — Water grade per process step is answered, and a spray-dried substance shifts the burden onto its own specification
- Stream: F (microbial)
- Type: closes-gap
- Affects: `data/utilities.csv`; `docs/facility/index.md`; `docs/process/microbial.md`; Q-037
- Source: SRC-EMA-WATER-2018
- Verbatim (Table 3, the row for a solution active substance): "AS is in solution, not sterile, and intended for parenteral use. | Any step excluding final isolation and purification. | Purified Water" and "Final isolation and purification | WFI"
- Verbatim (the row that applies to an isolated powder): "AS is not in solution, not sterile, and intended for use in a parenteral product. | Final isolation and purification | Purified Water***"
- Verbatim (the footnote that carries the cost): "*** Appropriate specifications have to be set for endotoxins and microbiological quality of the active substance as per the relevant Ph. Eur. chapters."
- Scale/system: active substance manufacture, non-sterile, intended for a parenteral product. Exactly this project's situation.
- Confidence: read in full
- Why it matters: this is the cleanest available answer to "water for injection or purified water, at which step", and for a spray-dried drug substance the default is purified water at final isolation, not water for injection. That is a real capital and utility saving. But the footnote shifts the burden: a process using purified water and carrying no endotoxin specification on the substance would be indefensible.
- Proposed action: set the water grade per step in `data/utilities.csv` from Table 3, state the guideline's risk-based framing rather than presenting it as a rule, and tie the choice explicitly to the requirement for an endotoxin specification on the drug substance.

### F-027 — Nuclease control: the protective claim is half evidenced and must be weakened where it is asserted
- Stream: F (microbial)
- Type: closes-gap (partially) / new-question
- Affects: Q-031; `docs/process/microbial.md`; R-009
- Sources: SRC-LAYZER-2004, SRC-CZAUDERNA-2003
- Verbatim: "Greater than 50% of the 2′-OH siRNA was degraded within the first minute of exposure to plasma and it was virtually all degraded by 4 h. By contrast, more than 50% of the 2′-F siRNA molecules remained full length after 24 h."
- Verbatim: "We further demonstrate that synthetic siRNA molecules with internal 2′-O-methyl modification, but not molecules with terminal modifications, are protected against serum-derived nucleases."
- Scale/system: picomole-scale gel assays; human plasma and fetal bovine serum at 37 °C; partially modified duplexes, not fully modified therapeutic siRNA
- Confidence: read in full
- Why it matters: Q-031 asks whether chemical modification makes aggressive nuclease control unnecessary, and the site currently asserts that it does. The evidence supports a roughly thousandfold gain in plasma half-life and shows that protection is **positional** — internal modification protects, terminal caps do not. It does not address nuclease carried by process bioburden in a buffer hold vessel, which is the actual question. No such measurement exists for any modality.
- Proposed action: weaken the assertion on the microbial page to what is evidenced, state the positional dependence, and keep Q-031 open explicitly on the manufacturing-hold half with the search that failed to close it recorded.

### F-028 — Purity multiplies only within a single analytical dimension
- Stream: G (regulatory)
- Type: new-question
- Affects: `EQ-PURITY`; `gen/balance.py` `purity_floor`; `docs/findings/filtration.md` §3; Q-011
- Source: SRC-FDA-OXLUMO-CHEMR for the method architecture; the observation itself arises from a disclosed contract specification pairing a single-strand purity above 85% by denaturing anion exchange with a duplex purity above 90% by non-denaturing size exclusion
- Verbatim (how duplex purity is actually measured): "ion pairing reversed phase chromatography HPLC (IPRP-HPLC) with ultraviolet (UV) detection is utilized under non-denaturing conditions to confirm that drug substance is in its native duplex form, and to determine the purity of the duplex structure relative to unhybridized single strands and related impurities."
- Scale/system: approved commercial siRNA drug substance; the numeric pair is a research-scale contract specification, not a GMP release criterion, and is flagged as such
- Confidence: read in full for the method architecture; the numeric pair is a secondary observation and is **not** proposed as a design input
- Why it matters: duplex purity measured under non-denaturing conditions can read **higher** than either single-strand purity measured under denaturing conditions, because the two methods measure different things. The site's purity-floor equation multiplies block full-length fractions, which is sound within one analytical dimension, but it must not be used to predict a non-denaturing duplex purity from denaturing single-strand purities. Nothing on the site currently says this.
- Proposed action: add the caveat to the equations page and to the filtration finding, and register a new question on which analytical dimension the drug-substance specification will actually be written in, because that decides which purity the floor has to clear.
