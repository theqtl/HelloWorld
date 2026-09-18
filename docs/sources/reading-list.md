# Reading list — an expert curriculum

Read this top to bottom and you will be able to hold your own with a contract manufacturer and an
engineering firm on an enzymatic-ligation siRNA drug substance: ask the right questions, recognise a
wrong number when you hear one, and know precisely which facts are established, which are inferred,
and which are still open.

Full citations, reachability and the scale each source applies to are in the
[source register](../registers/sources.md). This page is the order to read them in.

## How to read the access labels

Every entry states what was **actually read**, using the controlled `access` vocabulary from the
source register. The two things are different and the difference is the whole point:

| Label | Meaning |
|---|---|
| **full text read** | the complete article or document was read |
| **web page read** | a web page, blog, vendor note, standard or patent read in full |
| **abstract only** | only the abstract, or an abstract-equivalent record summary, was seen |
| **record only** | only bibliographic metadata was confirmed; no abstract was read |
| **redacted** | obtainable and read, but the numbers we need are withheld in it |
| **not retrieved** | could not be obtained at all |

A source marked *abstract only* or *record only* has not been read. Nothing should rest on it.
The census in [What we have not actually read](#what-we-have-not-actually-read) lists every one.

---

## Tier 0 — orientation

Five open-access items, about three hours in total. They give the vocabulary and the shape of the
field. Start here even if you are in a hurry.

**1. Virta, P. From liquid-phase synthesis to chemical ligation.** *Nucleic Acids Research* 2025.
[SRC-NAR-2025] · open access at PubMed Central · **full text read** · ~60 min · unblocks Q-011, Q-010.
The single best orientation piece: it covers liquid-phase synthesis, chemical ligation and
ligase-assisted assembly in one review, and it quotes the real fragment and assembly numbers from the
kilogram-scale industrial work that is otherwise behind a paywall.

**2. Muslehiddinoglu, J. et al. Technical Considerations for Use of Oligonucleotide Solution API.**
*Nucleic Acid Therapeutics* 2020. [SRC-PMC7415879] · open access at PubMed Central ·
**full text read** · ~40 min · unblocks Q-017, Q-018, Q-036, Q-037.
The most useful single document in this register. Written by a thirteen-author industry group, it
covers ultrafiltration, thin-film evaporation, viscosity, bioburden and storage for an oligonucleotide
drug substance in one place. Read it before anything else on the downstream train.

**3. Andrews, B.I. et al. Sustainability Challenges and Opportunities in Oligonucleotide
Manufacturing.** *Journal of Organic Chemistry* 2021. [SRC-IQ-SUSTAIN-2021] · open access at PubMed
Central · **full text read** · ~45 min · unblocks Q-011, Q-012.
Cross-company consensus on what the conventional route actually achieves, and therefore what a new
route has to beat. It also explains why capping exists, which turns out to matter a great deal.

**4. Vehring, R. Pharmaceutical particle engineering via spray drying.** *Pharmaceutical Research*
2008. [SRC-VEHRING-2008] · open access at PubMed Central · **full text read** · ~50 min · unblocks
Q-019, Q-021.
The origin of the Péclet framework the drying pages use. Derive the dimensions by hand as you read:
automated extraction of this paper's central equation has produced dimensionally impossible forms.

**5. Keil, T.W.M. et al. Spray drying of siRNA.** *Advanced Therapeutics* 2021. [SRC-KEIL-2021] ·
open access at PubMed Central · **full text read** · ~35 min · unblocks Q-030, Q-039, R-003.
The measured glass transitions and residual moistures that set the real thermal window. This is the
paper whose misreading produced the worst number this project ever carried.

---

## Tier 1 — the load-bearing sources

The site's conclusions rest on these eleven. If you challenge a conclusion, challenge one of these.

**6. Hongene Biotech. Chemoenzymatic ligation brochure, August 2025.**
[SRC-HONGENE-BROCHURE-2025] · open PDF on the vendor's site · **full text read** · ~15 min ·
unblocks Q-010, Q-012, Q-034; bears on R-002.
The most consequential single document for the filtration thesis, and it cuts against it. It names a
kilogram-scale GMP siRNA campaign, publishes overall yields of 19% to 43% against per-ligation
conversions above 90%, and its table footnote states that **both** of its routes end in HPLC
purification of the siRNA itself. Read the footnotes, not the headline.

**7. Gronke, R.S. et al. Use of ultrafiltration/diafiltration for the processing of antisense
oligonucleotides.** *Biotechnology Progress* 2023. [SRC-GRONKE-2023] · free publisher PDF exists
(bronze open access) but was blocked here; abstract read verbatim from two publisher records ·
**abstract only** · ~10 min for the abstract · unblocks Q-017, Q-020, Q-035, Q-036.
Three answers in one abstract: an oligonucleotide should be at least twice the membrane cut-off for
robust retention; 200 mg/mL is reachable at 95% yield and under 15 centipoise on a 3 kDa membrane;
and a polyanion will not diafilter out cationic impurities, magnesium included. **Pull the full text.**

**8. Banik, I. et al. Effect of ligand density and properties on membrane charge for enhancing
ultrafiltration of siRNA.** *Separation and Purification Technology* 2025. [SRC-ZYDNEY-2025] ·
open-access mirror at Penn State ScholarSphere, record readable, deposited file behind a Cloudflare
challenge · **abstract only** · ~10 min · unblocks Q-017, Q-035.
The real home of the ~193 g/L siRNA concentration figure, which is now confirmed and quotable, and the
only membrane cut-off quotable from this group's siRNA work: 10 kDa.

**9. Banik, I. et al. Development of charged membranes for the ultrafiltration of siRNA.**
*Journal of Membrane Science* 2025. [SRC-ZYDNEY-2024] · abstract open at the Penn State research
portal; full text behind a Cloudflare challenge, not a paywall · **abstract only** · ~10 min ·
unblocks Q-035.
Charged membranes raise the achievable siRNA concentration from 52 to over 180 mg/mL. The paper's
cut-off range is still not enumerated anywhere reachable, so Q-035 stays open on that point.

**10. Zhou, X. et al. Development of Kilogram-Scale Convergent Liquid-Phase Synthesis of
Oligonucleotides.** *Journal of Organic Chemistry* 2022, pages 2087 to 2110. [SRC-ZHOU-2022] ·
genuinely closed, verified across five independent indexes · **abstract only** · ~10 min for the
abstract · unblocks Q-011.
Read the abstract carefully: it says purities suitable for clinical use are achieved *after* the
standard full-length-product purification, and calls eliminating that chromatography a demonstrated
*potential*. Its fragment numbers are independently corroborated by item 1, so you do not need the
full text for those.

**11. Ajinomoto and Biogen. Convergent liquid phase syntheses of oligonucleotides (WO2020227618A2).**
[SRC-WO2020227618] · free full text at Google Patents · **full text read** · ~90 min · unblocks
Q-011, R-001.
The free way into the same programme: seven of the nine authors of item 10 are inventors here, and it
gives the measured, chromatography-free block purities at hectogram scale, plus what one preparative
chromatography step adds. The most quantitatively useful patent in this register.

**12. Paul, S. et al. Convergent Biocatalytic Mediated Synthesis of siRNA.** *ACS Chemical Biology*
2023. [SRC-ALMAC-2023] · the typeset article is served openly by the corresponding author's
organisation · **full text read** · ~30 min · unblocks Q-010, Q-016, Q-034, R-010.
The only peer-reviewed enzymatic ligation of a genuinely modified siRNA. It gives the working titre,
the vessel scale, the concentration at which the reaction stops working, and an adenylylated dead-end
by-product observed in this exact chemistry.

**13. Tianjin Kailaiying (Asymchem). Immobilized enzyme for catalyzing RNA ligation (CN119265174B).**
[SRC-CN119265174] · free at Google Patents; numeric tables are image-only and unreadable ·
**web page read** · ~60 min · unblocks Q-010, R-002.
The strongest evidence that an immobilised ligase holds duty on fully modified siRNA. Also the
clearest evidence that it does not, by itself, deliver a chromatography-free train.

**14. US FDA. Chemistry review, NDA 214103 (Oxlumo, lumasiran).** [SRC-FDA-OXLUMO-CHEMR] ·
open at accessdata.fda.gov · **redacted** · ~40 min · unblocks Q-033.
The document that reframes the purity question. It states the principle by which siRNA impurity limits
are actually set, and it is not a fixed threshold.

**15. European Medicines Agency. Onpattro (patisiran) assessment report, EMA/554262/2018.**
[SRC-PATISIRAN-EPAR] · open at ema.europa.eu · **redacted** · ~60 min for the quality sections ·
unblocks Q-033, R-001.
What a real siRNA drug-substance specification contains: thirteen named tests, no published acceptance
criteria, and the regulator's own written statement that some impurities can only be controlled at the
single-strand stage.

**16. Kelly, R., Parga, C., Ferguson, S. Scalable Membrane Enabled One-Pot Liquid-Phase
Oligonucleotide Synthesis.** *Organic Process Research and Development* 2025.
[SRC-KELLY-OPRD-2025] · open access, CC-BY, at PubMed Central · **full text read** · ~50 min ·
unblocks Q-011, R-001, and the diafiltration equation.
Does two jobs: the only measured crude purity for short 2'-O-methyl phosphorothioate oligomers, and
membrane selectivity data showing that purpose-built oligonucleotide membranes do not achieve a clean
cut even at a sixfold mass ratio. That is the empirical backbone of R-001.

---

## Tier 2 — depth by unit operation

### Ligation

**17. Novartis. Nucleic acid ligation method (WO2025262452A1).** [SRC-WO2025262452] · free at Google
Patents · **web page read** · ~45 min · unblocks Q-016, Q-034, R-010.
Pins the ATP stoichiometry a four-ligation assembly must pay for, and shows that regeneration from
AMP has a hard equilibrium ceiling.

**18. Lohman, G.J.S. et al. Efficient DNA ligation in DNA-RNA hybrid helices by Chlorella virus DNA
ligase.** *Nucleic Acids Research* 2014. [SRC-PBCV1-2014] · open access at PubMed Central ·
**full text read** · ~50 min · unblocks R-010.
The mechanism and the quantitative ATP threshold for suppressing the adenylylated dead end. **Read the
correction too** — this is the one source in the register with a known erratum, and it is worth
knowing that the erratum touches only a figure caption.

**19. Codexis. Four ligation patent families.** [SRC-CODEXIS-PATENTS] · free at Google Patents ·
**full text read** · ~90 min if you skim all four · unblocks Q-032.
Read these to learn what is *not* there. No absolute conversion, no titre, no residual-protein
clearance anywhere in the estate of the technology's most vocal proponent.

**20. New England Biolabs. Immobilized enzyme compositions and methods (WO2023173098A1).**
[SRC-NEB-WO2023173098] · free at Google Patents · **full text read** · ~30 min · unblocks Q-032.
How the leading supplier actually characterises enzyme leaching: a functional gel assay, reported
qualitatively. There is no mass-based leaching specification in the public record.

**21. Shieh, Y., Swartz, A.R., Rustandi, R.R. Detection of residual T7 RNA polymerase.**
*Electrophoresis* 2024. [SRC-T7RNAP-2024] · CC-BY, served openly by the German National Library
deposit mirror — **not** paywalled despite what the indexes suggest · **full text read** · ~25 min ·
unblocks Q-032.
The nearest thing to an enzyme-clearance benchmark. Learn the shape of the argument, not the number:
the size ratio is inverted for our case.

### Blocks and purity

**22. Hybridon. Extremely high purity oligonucleotides using dimer blocks (US6087491A).**
[SRC-US6087491] · free at Google Patents · **web page read** · ~40 min · unblocks Q-011, R-001.
The per-cycle failure rate that underlies the whole purity-floor argument, and the patentee's own
statement that n-1 is the hardest species to chromatograph.

**23. Avecia. Process for the preparation of phosphorothioate oligonucleotides (US7227017B2).**
[SRC-US7227017] · free at Google Patents · **web page read** · ~25 min · unblocks Q-011.
Measured phosphodiester impurity in a fully phosphorothioate strand, and the demonstration that it
roughly doubles from one wash-and-dry decision.

**24. Tutiš, L. et al. Ion-Pairing Hydrophilic Interaction Chromatography for Impurity Profiling.**
*Analytical Chemistry* 2025. [SRC-TUTIS-2025] · open access at PubMed Central · **full text read** ·
~45 min · unblocks Q-011.
How separable n-1 actually is, how fragile that separation is, and why mass spectrometry cannot
substitute for chromatography on the hardest impurity.

### Filtration

**25. Schwartz, L. Diafiltration for Desalting or Buffer Exchange.** *BioProcess International*,
May 2003. [SRC-SCHWARTZ-BPI-2003] · open PDF on the vendor content network · **full text read** ·
~30 min · unblocks Q-020, EQ-DIAF, EQ-FLUX.
A named author with a reference list, replacing the anonymous aggregator the equations used to lean
on. Gives the gel-polarisation law, the three-to-six-times cut-off rule and the diavolume tables.
**It also contains a dimensionally impossible equation for process time** — see
[Claims to not repeat](#claims-to-not-repeat).

**26. Pall Corporation. Introduction to Tangential Flow Filtration, report 20-0410.**
[SRC-PALL-TFF] · open PDF · **full text read** · ~30 min · unblocks Q-020, EQ-AREA.
Membrane area sizing with worked examples that reproduce by hand, and the diavolume table that
confirms the site's removal percentages. Tag as a vendor claim wherever used.

**27. Nourafkan, E. et al. Tangential Flow Filtration Performance for mRNA Drug Substance
Purification.** *Biotechnology Journal* 2024. [SRC-NOURAFKAN-2024] · CC-BY, deposited at the White
Rose institutional repository · **full text read** · ~50 min · unblocks Q-036, R-011.
A peer-reviewed primary source for the diafiltration clearance equation applied to a nucleic acid, and
the most transferable yield lesson in this register: hold-up volume in tubing and filters, not membrane
passage, dominates loss at small batch size.

**28. Imbrogno, A. et al. Molecular weight cut off determination in ultra- and nanofiltration.**
*Separation and Purification Technology* 2025. [SRC-MWCO-REVIEW-2024] · CC-BY, full text at the
Karlsruhe Institute of Technology repository · **full text read** · ~60 min · unblocks Q-035.
Was abstract-only while carrying a load-bearing claim on the site's most important page. Now read:
the cut-off definition, why real membranes blur it, and the finding that charged solutes behave very
differently from the uncharged tracers cut-offs are measured with.

**29. Guillen-Cuevas, K. et al. Purifying circular RNA by ultrafiltration.** *Separation and
Purification Technology* 2025. [SRC-HUSSON-CIRCRNA-2025] · CC-BY at PubMed Central ·
**full text read** · ~45 min · unblocks Q-020, Q-035.
The one nucleic-acid ultrafiltration paper found with an enumerated cut-off ladder, a stated diavolume
count and measured sieving coefficients. Read it for the methodology, not the numbers.

**30. Zydney, A.L. and van Reis, R. Highly selective membrane systems (US7497950).**
[SRC-US7497950] · open at the USPTO · **web page read** · ~20 min · unblocks R-001.
The lower bound on what ultrafiltration can resolve, from the people who set it.

### Evaporation

**31. Hughes, D.T. The effect of turbulence on the minimum thickness of a liquid film flowing down a
vertical tube.** *Chemical Engineering Research and Design* 2024. [SRC-HUGHES-2024] · green open
access at arXiv · **full text read** · ~45 min · unblocks Q-018, R-004.
The minimum wetting rate, which is the constraint that decides whether a small-batch evaporator can
run single-pass at all. Reports the primary measurements with attribution, which matters because the
primary is genuinely closed [SRC-MORISON-2006].

**32. Medina, C., Scholl, S., Raedle, M. Film thickness and glycerol concentration mapping of falling
films.** *Micromachines* 2022. [SRC-MEDINA-2022] · open access at PubMed Central ·
**full text read** · ~30 min · unblocks Q-018.
The real source of the film-thickness range the site uses.

**33. Tetra Pak. Dairy Processing Handbook, Evaporators.** [SRC-TETRAPAK-DPH] · open ·
**web page read** · ~25 min · unblocks the evaporator energy basis.
The transfer judgement is yours to make and the handbook is explicit about its own scale and system.
Read it alongside [SRC-EFSAN-MVR] and note that the two disagree by a factor of two, because they are
at different temperature lifts.

### Drying

**34. Okuda, T. et al. Stability of Naked Nucleic Acids under Physical Treatment and Powder
Formation.** *Pharmaceutics* 2023. [SRC-NAKED-NA-2023] · open access at PubMed Central ·
**full text read** · ~40 min · unblocks R-003.
The evidence that retires atomisation shear as a governing risk for a short duplex, and shows why the
same worry is entirely justified for plasmid DNA.

**35. Malek-Adamian, E. et al. Effect of Sugar 2',4'-Modifications on Gene Silencing Activity of
siRNA Duplexes.** *Nucleic Acid Therapeutics* 2019. [SRC-MALEK-2019] · open access at PubMed
Central · **full text read** · ~35 min · unblocks Q-030, R-003.
Measured melting temperatures for a 21-nucleotide siRNA duplex, with the per-modification increment
and the buffer conditions. Read the conditions: a melting temperature without its salt concentration
is not a number.

**36. Gelman Constantin, J., Schneider, M., Corti, H.R. Glass Transition Temperature of Saccharide
Aqueous Solutions.** *Journal of Physical Chemistry B* 2016. [SRC-GELMAN-2016] · green open access
in the CONICET repository · **full text read** · ~45 min · unblocks Q-039, EQ-TG.
The Gordon-Taylor constants the site's glass-transition equation needs, and the discovery that the
anhydrous trehalose figure everyone quotes is one of at least two competing primary values.

**37. Alhajj, N. and O'Reilly, N.J. Interplay of solute crystallization and drying potential.**
*International Journal of Pharmaceutics* 2026. [SRC-SD-MORPH] · **CC BY 4.0 open access** — the
earlier "paywalled" record was wrong; blocked here only by a bot challenge · **abstract only** ·
~10 min for the abstract · unblocks Q-019.
**Pull this one.** It qualifies the Péclet reading on the drying finding, and its abstract contains no
numbers at all, so nothing quantitative should rest on it until somebody opens it.

**38. Nearest Neighbor Database, Turner 2004 Watson-Crick helices.** [SRC-NNDB-TURNER] · open ·
**web page read** · ~30 min · unblocks Q-030.
The openly published parameters for calculating an RNA duplex melting temperature. Learn what they
cover and, more importantly, what they do not: there is no openly citable parameter set for
2'-O-methyl, 2'-fluoro or phosphorothioate duplexes.

### Microbial control

**39. Layzer, J.M. et al. In vivo activity of nuclease-resistant siRNAs.** *RNA* 2004.
[SRC-LAYZER-2004] · open access at PubMed Central · **full text read** · ~30 min · unblocks Q-031.
The strongest quantitative evidence that modification is protective, and a clear view of its limits:
this is serum challenge, not a manufacturing hold.

**40. Czauderna, F. et al. Structural variations and stabilising modifications of synthetic siRNAs.**
*Nucleic Acids Research* 2003. [SRC-CZAUDERNA-2003] · open access at PubMed Central ·
**full text read** · ~40 min · unblocks Q-031.
Protection depends on where the modifications sit, not merely that they exist. End caps do not work.

**41. de Vries, I. et al. Single-use membrane adsorbers for endotoxin removal and purification of
endogenous polysialic acid.** *Biotechnology Reports* 2018. [SRC-DEVRIES-2018] · open access at
PubMed Central · **full text read** · ~35 min · unblocks R-007.
The closest analogue to our endotoxin problem: a polyanionic product competing with endotoxin for the
same charged sites. The adsorber alone was two orders of magnitude short.

**42. Muralidharan et al. Microbial-control hold-time assessments.** *BioProcess International* 2025.
[SRC-BPI-HOLDTIME-2025] · open · **full text read** · ~30 min · unblocks R-012.
Read this to know exactly what the site's old microbial ladder was, and that it describes mammalian
cell culture. It is on this list as a cautionary source, not as a design input.

### Scale-up, yields and process development

**42a. Kapil, A. et al. Model-aided process development for scalable spray drying of sticky
substances.** *Frontiers in Chemical Engineering* 2025. [SRC-KAPIL-2025] · fully open access ·
**full text read** · ~45 min · unblocks Q-012.
The number that kills a flat 90% dryer yield. Measured recoveries ran from 8.6% to 22% before
optimisation and 61% to 89% after, from 5 g to 400 g. Optimised conditions did transfer between
scales; unoptimised ones did not.

**42b. Millipore. Protein Concentration and Diafiltration by Tangential Flow Filtration.**
[SRC-MILLIPORE-TFF] · open technical brief · **full text read** · ~30 min · unblocks Q-012, R-011.
Turns "less than 10% filtration loss" from an assumption into an equation. Loss is exponential in
product retention and in the combined concentration-and-diavolume term, with membrane adsorption as a
second additive term. Also states the mass-balance discipline the site does not yet apply: account for
retentate, filtrate **and** unrecoverable hold-up.

**42c. World Health Organization. Technology transfer in pharmaceutical manufacturing, Technical
Report Series 1044, Annex 4 (2022).** [SRC-WHO-TRS1044] · free on the WHO content network ·
**full text read** · ~60 min · unblocks the technology-transfer page.
It explicitly covers active pharmaceutical ingredients, and its Appendix 1 is the itemised list a
contract manufacturer will work from. Read it as a gap analysis against what this project currently
holds.

---

## Tier 3 — regulatory and standards

You must be able to cite these by name, and to say what each one *is*.

**43. ICH Q3A(R2), Impurities in New Drug Substances — Preamble; and the ICH Q6(R1) Final Concept
Paper, 25 June 2024.** [SRC-ICH-Q3A-SCOPE] · open at the ICH database · **full text read** · ~20 min
for the relevant sections · unblocks Q-033.
Read the Preamble. Oligonucleotides are explicitly excluded from ICH Q3A, and from Q6A. Any sentence
beginning "ICH requires" followed by a percentage for siRNA is unsupportable.

**44. EMA. Draft Guideline on the Development and Manufacture of Oligonucleotides,
EMA/CHMP/CVMP/QWP/262313/2024.** [SRC-EMA-OLIGO-2024] · open at ema.europa.eu ·
**full text read** · ~75 min · unblocks Q-033.
**Still a draft.** Consultation closed in January 2025 and no overview of comments has been published.
It requires three separate impurity specifications for a duplex, and it is the only regulatory
document in which the phrase "full length" appears — as an impurity group label, not a purity
attribute.

**45. PMDA review report, Onpattro (patisiran), and its quality overall summary.**
[SRC-PMDA-ONPATTRO] · open at pmda.go.jp, Japanese language · **full text read** · ~90 min ·
unblocks Q-033, R-001.
**Japan is where to go for any siRNA specification question.** PMDA publishes the complete
drug-substance specification item list with the method for each item and its own reasoning. No other
regulator does. It still masks every acceptance criterion.

**46. US FDA. Chemistry review, NDA 214012 (Leqvio, inclisiran).** [SRC-FDA-INCLISIRAN-CHEMR] ·
open at accessdata.fda.gov · **redacted** · ~40 min · unblocks Q-033.
Confirms independently of the EMA that the purity criterion is derived from demonstrated batch
capability. Every limit is withheld under exemption (b)(4).

**47. Approved siRNA product labelling, composition sections.** [SRC-SIRNA-LABELS] · open via
DailyMed · **full text read** · ~30 min for all seven · unblocks Q-021.
Four of the seven approved siRNA products contain no weighed excipient at all. Read this before
anybody tells you what excipient ratio the molecule "needs".

**48. European Pharmacopoeia 5.1.4 and monograph 0169 (Water for injections).**
[SRC-PHEUR-5-1-4], [SRC-PHEUR-0169] · read from third-party reproductions of the printed text;
edition caveats recorded in the register · **full text read** · ~40 min · unblocks Q-037.
Learn the difference between an interpretation rule, an acceptance criterion and an action level.
Three of the numbers most often quoted in this area are not the kind of thing people think they are.

**49. EMA. Guideline on the quality of water for pharmaceutical use,
EMA/CHMP/CVMP/QWP/496873/2018.** [SRC-EMA-WATER-2018] · open at ema.europa.eu ·
**full text read** · ~30 min · unblocks Q-037.
Table 3 answers "which water at which step" directly, and the answer for an isolated solid drug
substance is not the one most people assume.

**50. ICH Q7, Good Manufacturing Practice Guide for Active Pharmaceutical Ingredients.**
Open at the ICH database · **full text read** · ~90 min · unblocks R-009, R-012.
Section 4.34 is exactly this project's situation. Read it to learn that it supplies no numbers at all,
and why that is the regulator's deliberate choice.

**50a. Engineering and quality standards, current editions.** [SRC-STANDARDS-CURRENT] ·
each verified against the issuing body's own catalogue page · **web page read** · ~40 min ·
unblocks the facility and technology-transfer pages.
Four editions commonly cited in packages of this kind are stale, and citing a superseded standard
dates a document on sight. This entry also answers two questions people ask constantly: whether the
sterile-manufacturing annex applies to a non-sterile drug substance, and whether the validation annex
binds an active substance. Both answers are "not by default, and if you adopt them you must say so".
Note that a spray-dried powder brings the combustible-dust standard into scope, and that the
explosion parameters of the actual powder are a testing deliverable rather than something you look up.

---

## What we have not actually read

This is a census, not a pull list: it covers every source in the register whose `access` is
*abstract only*, *record only* or *not retrieved*, whether or not it merits a place in the curriculum
above. If you want to know what this site is resting on that nobody has opened, this table is the
answer.

| Source | Access | What it is used to support | Where it is used |
|---|---|---|---|
| [SRC-ZHOU-2022] | abstract only | Block purity and yield at kilogram scale; the purity floor | Filtration finding §3, equations, blocks page |
| [SRC-ZYDNEY-2024] | abstract only | Membrane cut-off selection and the charged-membrane concentration ceiling | Filtration process page, equations, balance |
| [SRC-ZYDNEY-2025] | abstract only | The ~193 g/L concentration ceiling | Filtration process page |
| [SRC-SD-MORPH] | abstract only | Qualifying the Péclet reading of particle morphology | Spray-drying finding §4, spray-drying process page, equations |
| [SRC-GRONKE-2023] | abstract only | Cut-off rule, achievable concentration, diafiltration salt requirement | Not yet cited on the site; queued |
| [SRC-OPRD-2025] | record only | Nothing any more — both figures previously attributed to it have been traced to other sources | Microbial process page |
| [SRC-MORISON-2006] | record only | Nothing directly; its numbers reach us through [SRC-HUGHES-2024], which was read | Provenance chain only |
| [SRC-XIA-1998] | record only | Nothing directly; its parameters reach us through [SRC-NNDB-TURNER], which was read | Provenance chain only |

**How to read this table.** Five of these eight are genuinely load-bearing and unread. Two are
provenance-chain entries whose numbers reach us through an open source that *was* read in full, so
nothing rests on the unread document. One, the microbiological control paper, no longer supports
anything at all, because both numbers once attributed to it turned out to belong elsewhere.

**Three of them are not paywalled.** The 2026 morphology paper is CC BY 4.0, the antisense
ultrafiltration paper is bronze open access, and both Penn State membrane papers are deposited in an
open repository. All are blocked by automated bot challenges, not by subscription. **A human with an
ordinary browser can open every one of them in a few minutes.** That is the single highest-value
manual task outstanding.

---

## What you must be able to say

Twenty statements. Each is sourced. Together they are what fluency in this process sounds like.

1. **Filtration does not separate by one nucleotide, and nothing changes that.** A deletion differs
   from full-length by about 5% of the strand mass, and the published threshold for clean
   ultrafiltration fractionation is a molecular-weight ratio of about five. [SRC-US7497950]
2. **The purity floor is set at the blocks and multiplies.** Measured, chromatography-free block
   purity for 4- and 5-nucleotide modified blocks is 89% to 96% at hectogram scale.
   [SRC-WO2020227618]
3. **That multiplicative model has been validated against a real assembly.** An 18-mer built from
   four blocks came out at 80% purity at 200 g without chromatography, which implies an effective
   per-block fraction of about 94.6%. [SRC-NAR-2025]
4. **One preparative chromatography step lifts a block from about 81% to about 99%, at 90% to 98%
   recovery.** That is the selectivity a filtration-only train forgoes. [SRC-WO2020227618]
5. **There is no published numeric purity specification for any approved siRNA drug substance, in
   any jurisdiction.** Japan discloses the test list and the methods; the United States discloses the
   attribute names; nobody discloses the criteria. [SRC-PMDA-ONPATTRO], [SRC-FDA-INCLISIRAN-CHEMR]
6. **The criterion is not a fixed threshold — it is indexed to your own toxicology batches.** The
   FDA's stated position is that specified impurity limits must not exceed the maximum levels
   observed in the nonclinical batches. [SRC-FDA-OXLUMO-CHEMR]
7. **Oligonucleotides are explicitly outside the scope of ICH Q3A and Q6A.** There is no ICH impurity
   threshold to cite for siRNA, and ICH has only now started work to change that.
   [SRC-ICH-Q3A-SCOPE]
8. **A regulator has stated in writing that some impurities can only be controlled at the
   single-strand stage.** That is the regulatory articulation of the purity-floor argument.
   [SRC-PATISIRAN-EPAR]
9. **Demonstrated enzymatic ligation titre for a modified siRNA is about 1 mM in a 1 L vessel, and
   10 mM was tried and failed to go to completion.** [SRC-ALMAC-2023]
10. **An immobilised ligase has held above 92% conversion on fully modified siRNA blocks in
    continuous flow for over 100 hours.** That part of the immobilisation risk is answered.
    [SRC-CN119265174]
11. **Ligase clearance is not.** No ppm figure, no log reduction, no immunoassay and no total-protein
    result for a ligation stream exists anywhere in the public record. [SRC-CODEXIS-PATENTS],
    [SRC-NEB-WO2023173098]
12. **Per-ligation conversion and overall yield are different quantities, an order of magnitude
    apart.** Published overall yields for ligation-built siRNA are 19% to 43%.
    [SRC-HONGENE-BROCHURE-2025]
13. **Every named commercial ligation route still ends in HPLC purification of the siRNA itself.**
    Filtration replaces fragment chromatography, not final-product chromatography.
    [SRC-HONGENE-BROCHURE-2025]
14. **An oligonucleotide should be at least twice the membrane cut-off for robust retention**, and
    200 mg/mL at 95% yield and under 15 centipoise has been achieved on a 3 kDa membrane.
    [SRC-GRONKE-2023]
15. **A polyanion will not diafilter out cationic impurities, magnesium and calcium included** — and
    the ligation buffer contains magnesium. [SRC-GRONKE-2023]
16. **Hold-up volume, not membrane passage, is what costs yield at small scale.** Thirty to forty
    percent of a nucleic acid can remain in tubing and filters. [SRC-NOURAFKAN-2024]
17. **Thin-film evaporation of an oligonucleotide drug substance is established practice**, with a
    reported maximum of 160 mg per gram of solution achieved in manufacture. [SRC-PMC7415879]
18. **The glass transition binds before the melting temperature.** A 21-nucleotide siRNA duplex melts
    at 58 °C to 64 °C; the spray-dried trehalose powder's glass transition was measured at 38 °C to
    53 °C. [SRC-MALEK-2019], [SRC-KEIL-2021]
19. **Atomisation shear is a plasmid problem, not a short-duplex problem.** Naked siRNA retained over
    80% integrity and full activity through sonication, vortexing, atomisation and freeze-drying.
    [SRC-NAKED-NA-2023]
20. **The one oligonucleotide-specific bioburden figure is under 1 colony-forming unit per millilitre
    at drug substance**, and it is a statement of practice with a case-by-case escape, not a
    pharmacopoeial limit. [SRC-PMC7415879]

---

## Claims to not repeat

Numbers and rules that circulate in this field, that this project has carried or nearly carried, and
that are wrong, mis-scoped or misattributed. Being able to correct a confident wrong number in a
meeting is worth more than knowing ten right ones.

| The claim | What is actually true |
|---|---|
| "Spray-dried trehalose siRNA has a glass transition near 117 °C." | The paper it was cited to measured 38 °C to 53 °C at 3.8% to 4.6% residual moisture. The 117 °C figure is for *anhydrous* trehalose, and even that is contested: 389 K and 380 K are both claimed by different primary sources. [SRC-KEIL-2021], [SRC-GELMAN-2016] |
| "Charged membranes take siRNA above 190 g/L" — cited to the 2024 *Journal of Membrane Science* paper. | That paper reports 52 to over 180 mg/mL. The ~193 g/L figure belongs to the 2025 companion paper by the same group, where it is real. [SRC-ZYDNEY-2024], [SRC-ZYDNEY-2025] |
| "Ultrafiltration resolution is governed by a rule in a microdialysis patent." | That patent is about microdialysis for mass spectrometry and says nothing on the subject. The real bound is in the Zydney and van Reis membrane patent. [SRC-US7497950] |
| "The European assessment report sets a purity criterion of 80% full-length." | It contains no numeric criteria at all. The 80% figure is an **FDA recommendation for guide RNA in genome editing**, not an siRNA specification. [SRC-AMVUTRA-EPAR], [SRC-FDA-CBER-2024] |
| "Full-length product is the purity attribute in the EMA oligonucleotide guideline." | The only place "full length" appears in that guideline is as an **impurity group label** for a phosphorothioate antisense oligonucleotide. Porting ">=80% full-length" to siRNA is a category error twice over. [SRC-EMA-OLIGO-2024] |
| "ICH requires X% purity for siRNA." | Oligonucleotides are explicitly excluded from the scope of ICH Q3A and Q6A. There is no such requirement. [SRC-ICH-Q3A-SCOPE] |
| "The FDA inclisiran chemistry review states purity exceeds 85% full-length by HPLC." | The 94-page review was read in full. No such sentence exists, and no unredacted purity number of any kind appears in it. [SRC-FDA-INCLISIRAN-CHEMR] |
| "Ligation-based siRNA manufacture achieves >95% conversion at up to 100 g/L with >98% purity." | Traceable only to a marketing blog. Absent from the company's own press release and from all four of its ligation patent families. [SRC-CODEXIS], [SRC-CODEXIS-PR-2024], [SRC-CODEXIS-PATENTS] |
| "Bioburden runs from 100 down to 10 colony-forming units per 10 mL toward drug substance, with endotoxin from 5 to 1 EU/mL." | Every one of those figures is verbatim from an article about **mammalian cell culture**, hedged there as a description of typical practice. [SRC-BPI-HOLDTIME-2025] |
| "200 colony-forming units per gram is the pharmacopoeial maximum for an oligonucleotide." | It is the Ph. Eur. **interpretation rule** for reading a 10² criterion, and it is the compendial floor for any non-sterile substance — three orders of magnitude looser than what the oligonucleotide literature recommends. [SRC-PHEUR-5-1-4] |
| "Water for injection must have fewer than 10 colony-forming units per 100 mL." | That is an **action level**, qualified twice in the monograph, and the method conditions are part of it. The endotoxin figure in the same monograph *is* a limit. [SRC-PHEUR-0169] |
| "The T4 DNA ligase patent shows it cannot ligate 2'-O-methyl segments." | The patent says T4 is "poor at" it, and it is not a negative-result patent at all: it is GlaxoSmithKline's **engineered-ligase** patent, and it identifies alternatives that work. [SRC-USPTO-10640812] |
| "The kilogram-scale convergent synthesis assembled the product without chromatography." | It assembled the *fragments* into the 18-mer without column chromatography. Clinical-grade purity still required the standard full-length-product purification, and eliminating that was described as a *potential*. [SRC-ZHOU-2022] |
| "Process time equals filtrate flow rate times volume." | Printed in a widely circulated article and dimensionally impossible: litres per hour times litres is not a time. [SRC-SCHWARTZ-BPI-2003] |
| "Diafiltration clearance is exp(−N(1−σ)) where σ is the sieving coefficient." | Correct only if σ is the **rejection** coefficient. With σ read as sieving, a freely permeating salt never washes out, which is plainly wrong. [SRC-NOURAFKAN-2024], [SRC-KELLY-OPRD-2025] Note this is a trap in the wider literature, **not** a defect on this site: `EQ-DIAF` states the field-standard form correctly and already flags the alternative. |
| "The 2026 morphology paper shows outlet temperature predicts particle morphology and inlet does not." | Its abstract says inlet temperature *alone* is insufficient. It does not say outlet temperature is sufficient or superior, and it contains no numbers at all. [SRC-SD-MORPH] |
| "Modification makes nuclease control unnecessary." | The evidence is serum challenge, not a manufacturing hold, and protection is positional: internal modification protects, terminal caps do not. Nobody has measured nuclease activity from process bioburden. [SRC-LAYZER-2004], [SRC-CZAUDERNA-2003] |
| "Oligonucleotide processes are intrinsically low-bioburden." | The published argument rests on two premises — the synthesis runs in solvents, and only the last step is aqueous. **Neither holds for a fully aqueous enzymatic route with an enzyme and its buffer in the stream.** [SRC-PMC7415879] |
| "A ~1-2 °C rise per modified nucleotide means a fully modified duplex melts near 100 °C." | That increment was measured over **three** modified positions. Extrapolating it across twenty-one is unsupported by the source. [SRC-MALEK-2019] |
| "An anion-exchange adsorber will clear endotoxin from our stream." | With a polyanionic product competing for the ligand, an adsorber alone left 641 EU per milligram and only reached specification with an orthogonal step, at 29% recovery. [SRC-DEVRIES-2018] |
