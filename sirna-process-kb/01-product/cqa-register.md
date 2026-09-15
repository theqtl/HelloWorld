# Critical Quality Attribute register

> **[SEED]**. Criticality assignments must be justified by risk assessment per ICH Q9 and
> linked to clinical or non-clinical rationale before use.

| ID | Attribute | Category | Typical control | Criticality | Primary clearing step |
|---|---|---|---|---|---|
| CQA-01 | Identity, sequence of each strand | Identity | LC-MS, nuclease digestion mapping | Critical | Synthesis fidelity |
| CQA-02 | Full-length product content | Purity | IP-RP-UV, AEX, CGE | Critical | Purification chromatography |
| CQA-03 | n-1 and shortmer content | Purity | IP-RP, CGE | Critical | Purification chromatography |
| CQA-04 | n+1 and longmer content | Purity | IP-RP, CGE | Critical | Purification chromatography |
| CQA-05 | Phosphodiester impurities, missing sulfur | Purity | IP-RP-MS | Critical | Purification chromatography, sulfurisation control |
| CQA-06 | Depurination and abasic products | Purity | LC-MS | Critical | Detritylation control, purification |
| CQA-07 | Residual 2'-protecting group | Purity | LC-MS | Critical | Deprotection |
| CQA-08 | Duplex content, percent annealed | Product-related | UV melting, non-denaturing CGE or AEX, SEC | Critical | Annealing |
| CQA-09 | Strand ratio, sense to antisense | Product-related | Denaturing IP-RP or AEX | Critical | Annealing |
| CQA-10 | Oligonucleotide content, assay | Content | UV at 260 nm with extinction coefficient, qNMR | Critical | Final UF/DF |
| CQA-11 | Water content | General | Karl Fischer | Non-critical | Lyophilisation |
| CQA-12 | Counterion content, sodium | General | Ion chromatography, ICP | Non-critical | Counterion exchange UF/DF |
| CQA-13 | Residual solvents | Safety | GC headspace, ICH Q3C | Critical | UF/DF, lyophilisation |
| CQA-14 | Elemental impurities | Safety | ICP-MS, ICH Q3D | Non-critical | Raw material control |
| CQA-15 | Bioburden | Microbial | Compendial | Critical | Sterile filtration, hold time control |
| CQA-16 | Bacterial endotoxin | Microbial | LAL or recombinant factor C | Critical | Raw material and water control, UF/DF |
| CQA-17 | Residual splint oligonucleotide | Process-related | Hybridisation assay or qPCR | Critical, **ligation route only** | Nuclease digestion, chromatography |
| CQA-18 | Residual ligase protein | Process-related | ELISA or total protein | Critical, **ligation route only** | Chromatography, UF/DF |
| CQA-19 | Adenylylated species, AppRNA | Process-related | IP-RP-MS | Critical, **ligation route only** | Chromatography, deadenylase treatment |
| CQA-20 | Appearance, pH in solution | General | Visual, potentiometric | Non-critical | Final formulation |

## The hard ones

**CQA-02 through CQA-05 are the whole purification problem.** These impurities differ from
product by one nucleotide or by a single sulfur atom. They are not cleared by any
orthogonal mechanism, only by chromatographic resolution, and resolution degrades as
column load increases. The commercial process economics turn almost entirely on how much
load can be pushed while holding these specifications.

**CQA-17 through CQA-19 exist only if the chemoenzymatic route is chosen.** They add
protein and nucleic acid clearance obligations that the purely synthetic route does not
have. This is a material argument in the route decision and is captured in
`10-decisions/decision-log.md`.
