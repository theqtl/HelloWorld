# Research kickoff prompt

Paste the block below into a new Claude Code session on this repository.
The repository is intentionally empty. The session designs everything.

---

```text
Enter plan mode. Propose a plan and wait for my approval before writing any files.

## 0. Situation

This repository is empty by design. There is no inherited structure, no template set, and
no prior content to conform to. You are building the whole thing from scratch.

A previous attempt used markdown files and CSV registers in a folder tree. It was rejected
as not user friendly, specifically for process flow diagrams and equations, which markdown
renders badly or not at all. Do not rebuild that. The presentation layer is a first-class
design problem here, not an afterthought.

## 1. What I am designing

An siRNA drug substance process, and the greenfield cGMP facility to manufacture it.

### Decisions already made. These are fixed. Do not relitigate them.

- **Strand assembly:** chemically synthesised blocks joined by ENZYMATIC LIGATION.
- **Purification:** FILTRATION-LED. Chromatography only where you can demonstrate that
  filtration cannot do the job.
- **Concentration: EVAPORATION WILL BE USED.** Driven by throughput demand. The TYPE is
  open, so evaluate falling film, wiped film, thin film, forced circulation, mechanical
  vapour recompression, and flash, and recommend one. That evaporation happens is settled.
- **Drying: SPRAY DRYING WILL BE USED.** Driven by throughput demand. Lyophilisation cannot
  meet the required throughput. That spray drying happens is settled.
- **Microbial control** across the entire train.

Your job on the fixed items is **how to make them work**, not whether to do them. There are
real technical concerns here, in particular whether a duplex survives atomisation and
drying, and whether thermal exposure in an evaporator degrades product. Treat those as
design constraints to engineer around: what configuration, what conditions, what excipients,
what alternative sequencing. Surface every risk you find and put it in the risk register,
but do not come back recommending lyophilisation. If a constraint looks genuinely
prohibitive, say so precisely and propose the engineering route through it.

### The one open question that decides the architecture

Filtration separates by size, charge, and binding. It does not separate by a
single-nucleotide length difference. An n-1 impurity differs from product by one nucleotide
out of roughly twenty. So a filtration-led train only closes if the impurity profile is
CONTROLLED WHERE IT IS CREATED rather than RESOLVED AT THE END.

Answer this with evidence, not assertion, in either direction:
- What each filtration mode can and cannot clear from this stream, quantitatively.
- Whether block-stage purity control plus high ligation conversion holds final purity
  without a polishing separation.
- What purity specification would have to move, or what upstream control tighten, for the
  filtration-only case to close.
- If chromatography cannot be avoided, where the minimum necessary chromatography sits, and
  what filtration still buys around it.

This is the finding I most want.

### Throughput is the design driver

Everything above follows from throughput demand. Treat capacity as the organising
constraint throughout: mass flow per unit operation, evaporation duty, dryer capacity,
campaign structure, and what becomes the bottleneck. Where I have not given you a number,
carry explicit scenarios rather than inventing one, and make every sizing result a visible
function of the scenario so it can be re-run when the real number arrives.

## 2. Deliverable 1, and do this first: the information architecture

Before researching content, design how this body of knowledge will be presented and
retrieved. Propose it in your plan. I will approve it before you build.

Requirements it must satisfy:

- **Process flow diagrams that are real diagrams.** Vector graphics, legible, with stream
  numbers that tie to the mass balance. Not ASCII art. Block flow, process flow, and enough
  structure to hand to an engineering firm later.
- **Equations that render as equations.** Properly typeset mathematics, with every term
  defined, assumptions stated, and validity range given.
- **Fast retrieval.** I need to find one parameter, one equation, or one unit operation
  without reading anything else. Search matters.
- **Tabular data stays queryable.** Equipment, streams, parameters, risks, questions.
  Sortable and filterable, not buried in prose.
- **Usable by people who do not use git.** Engineers, quality, and a capital project team
  will need to read and ideally contribute.
- **Cross-linked.** A parameter on a flowsheet should reach its unit operation, its
  equation, its risk, and its instrument.

Weigh at least these options, and say why you rejected the others:
- A static documentation site with math and diagram rendering, published from this repo.
- An interactive HTML application published as an artifact, with embedded vector flowsheets.
- A notebook-based or computational-document approach where the mass balance actually
  executes and the numbers in the document are live.
- A spreadsheet workbook for the quantitative layer, paired with something else for prose.
- A hybrid: structured source data plus a generated presentation layer.

I have a mild preference for the presentation layer being generated from structured source
data, so that a number lives in one place and appears everywhere it is needed. Argue me out
of it if you disagree. Note that this repository has GitHub Pages available.

Recommend one. Justify it against the requirements above. Then build it.

## 3. Research scope

Run these as parallel teams with their own context. Refine the decomposition in your plan.
Streams that synthesise others' output sequence after them.

A. **Enzymatic ligation.** Enzymes and end-chemistry requirements, junction design and
   modification tolerance, splint versus splint-free chemistry, conditions, kinetics,
   conversion, the adenylylated dead-end species and other side reactions, solid-phase and
   immobilised variants, scale-up behaviour, GMP enzyme sourcing.

B. **Block preparation.** Synthesis, deprotection, block-stage purification, 5' phosphate
   installation, block specifications, and how block purity propagates into final purity.

C. **Filtration-led purification.** Every applicable mode: tangential flow ultrafiltration,
   diafiltration, nanofiltration, membrane adsorbers, depth and sterilising filtration, and
   any charge or affinity based membrane process. What each clears, achievable separation
   from each impurity class, cascade and staging configurations, flux, fouling, yield,
   scale-up rules.

D. **UF/DF in depth.** Membrane selection for a species of roughly seven kilodaltons,
   real retention versus nominal rating, diafiltration design, flux and polarisation models,
   shear, hold-up and recovery, single-use versus reusable, cleaning and reuse validation.

E. **Evaporation.** Technology selection across the options listed above. Thermal exposure
   and residence time versus product stability, duplex integrity, vacuum and boiling point
   elevation, achievable concentration, viscosity and fouling limits, foaming, materials of
   construction, heat transfer and duty calculation, cleaning and sanitisation, scale-down
   representation.

F. **Spray drying.** Whether the duplex is dried as a duplex or the strands dried separately
   and annealed after, with a recommendation. Atomiser selection, inlet and outlet
   temperature design, droplet drying kinetics, glass transition and amorphous stability,
   excipient and carrier selection, particle engineering, residual moisture, cyclone and
   wall losses, yield at scale, containment, dryer sanitisation, low-bioburden operation.

G. **Microbial control and contamination control strategy.** Across an aqueous,
   enzyme-containing process. Bioburden and endotoxin, hold times, water quality per step,
   nuclease control proportionate to a modified duplex, sanitisation of evaporator and
   dryer, filter validation, and where the sterile or low-bioburden boundary sits.

H. **Greenfield capital design.** Facility concept for this specific train. Area
   classification, hazardous-area footprint given this route's actual solvent duty,
   utilities and loads including the evaporator and dryer duties, layout and flows,
   expansion strategy, and what drives capital cost.

I. **Process development, benchtop to scale.** Stage-appropriate approach, scale-down models
   and their qualification, design of experiments strategy, what must be characterised, and
   what breaks first on scale-up for each unit operation. Be specific about evaporation and
   spray drying, where small-scale results are notoriously unrepresentative.

J. **Tech transfer and engineering package.** Document set, mass and energy balances,
   governing equations, equipment specification and sizing basis, instrumentation, process
   analytical technology per unit operation, control strategy, and the ICH and engineering
   standards that bind.

K. **Risks and open questions.** Synthesised from every other stream.

## 4. Quantitative content required

- **A mass balance** across the whole train, with stream numbers tying to the flowsheet, and
  yield propagation per step. Make it executable if your architecture allows.
- **An energy balance** for the thermal operations. Evaporation and spray drying both have
  real duty, and it feeds utility sizing and facility cost.
- **Governing equations**, with terms defined, assumptions stated, validity range given, and
  the data needed to use them. At minimum: tangential flow flux with polarisation and gel
  models, diafiltration clearance versus diavolumes, sieving and rejection coefficients,
  membrane cascade staging, evaporator heat transfer and overall coefficient, boiling point
  elevation, spray dryer mass and energy balance, droplet drying kinetics, Peclet number and
  particle morphology, glass transition and moisture relationships, ligation kinetics and
  conversion.
- **Say which equations are well founded for this application** and which are borrowed from
  another industry and may not transfer. Spray drying and evaporation correlations largely
  come from food and fine chemicals. Be explicit about that.

## 5. Quality bar

- **Never invent a number.** If a value is not in a source you actually read, do not state
  it. Mark it as a gap and register it. A plausible fabricated range is worse than a blank,
  because it will be designed against and nobody will remember where it came from.
- **Record scale and system for every literature result.** A bench result on unmodified RNA
  does not transfer to kilograms of modified phosphorothioate siRNA. Make that visible.
- **Cite everything** resolvably. Where you reached only an abstract, say so.
- **Separate established fact from your own inference.** Label your reasoning as reasoning.
- **Report negative findings prominently.** If something does not work, that is the most
  valuable thing you can tell me.

## 6. Practical constraints

- **Test network access early** and report what you can and cannot reach. Web search and
  page fetching are gated separately in this environment. Record unreachable sources as
  gaps rather than guessing around them.
- Paywalled publisher content will not be reachable. Produce a prioritised reading list of
  what I should pull manually, ranked by what it would unblock.
- Validate before finishing: any structured data parses, links resolve, the site or
  application builds, and no identifier is referenced without being defined.
- Commit to this session's designated branch and push. No pull request unless I ask.

## 7. Present your plan

Cover: the information architecture you recommend and why, the team decomposition, what each
team produces, sequencing and dependencies, how you will attack the filtration question in
section 1, how you will handle the duplex-survival question for spray drying, and the shape
of the final output. Then wait for my approval.
```
