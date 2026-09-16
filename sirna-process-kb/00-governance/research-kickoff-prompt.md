# Research kickoff prompt

Paste the block below into a new Claude Code session on this repository.
It starts in plan mode and runs a multi-team research programme.

---

```text
Enter plan mode. Propose a research plan and wait for my approval before writing any files.

## 1. Read first

This repository contains `sirna-process-kb/`, a process knowledge base for designing an
siRNA drug substance process and the greenfield cGMP facility to run it. Before planning,
read in this order:

- sirna-process-kb/README.md
- sirna-process-kb/conventions/how-to-use.md and conventions/file-naming.md
- sirna-process-kb/templates/TEMPLATE-unit-operation.md
- sirna-process-kb/00-governance/document-map.md
- sirna-process-kb/01-product/ (all three files)
- sirna-process-kb/03-process/ (all files, upstream and downstream)
- the CSV registers in 04-materials, 05-equipment, 06-pat-analytics, 09-risk,
  10-decisions, 11-open-questions

Everything currently in the knowledge base is a seeded scaffold. Every claim is tagged
[SEED], [ASSUMED], or [TBD] and none of it is verified against primary literature or a
real molecule. Treat it as a strawman to attack, not as fact. Where your research
contradicts it, correct it and say explicitly what changed and why.

## 2. The process concept to research

READ THIS CAREFULLY. It differs from the train seeded in the repository, which assumes
two orthogonal chromatography steps and lyophilisation. Do not drift back to that train.
Research the concept as stated here and assess it honestly, including the possibility
that it does not work.

- Product: siRNA drug substance, duplex, chemically modified.
- Strand assembly: chemically synthesised blocks joined by ENZYMATIC LIGATION.
- Purification: FILTRATION-LED. Evaluate every filtration mode that could contribute,
  including tangential flow ultrafiltration, diafiltration, nanofiltration, dia-nanofiltration,
  depth and sterilising filtration, membrane adsorbers, and any size, charge, or affinity
  based membrane process. Use CHROMATOGRAPHY ONLY where you can demonstrate that filtration
  cannot do the job.
- Concentration: FALLING FILM EVAPORATION.
- Drying: SPRAY DRYING.
- Microbial control across the entire train.

### The central question the research must answer head on

Filtration separates by size, charge, and binding. It does not separate by a
single-nucleotide length difference. An n-1 impurity differs from product by one
nucleotide out of roughly twenty. A chromatography-free process therefore only works if
the impurity profile is CONTROLLED WHERE IT IS CREATED rather than RESOLVED AT THE END.

Determine, with evidence:
- What filtration can and cannot clear from this stream, quantitatively.
- Whether block-stage purity control plus a high-conversion ligation can hold final purity
  without a final polishing separation.
- What purity specification would have to be relaxed, or what upstream control tightened,
  for the filtration-only case to close.
- If the honest answer is that chromatography cannot be avoided, say so plainly, state
  where the minimum necessary chromatography sits, and quantify what filtration still buys.

Do not resolve this by assertion in either direction. This is the finding I most want.

## 3. Workstreams

Run these as parallel research teams with their own context. Refine the decomposition in
your plan; this is a starting structure, not a constraint. Later streams that synthesise
others' output should be sequenced after them.

A. **Enzymatic ligation process.** Enzymes and their end-chemistry requirements, junction
   design and modification tolerance, splint design or splint-free chemistry, reaction
   conditions and kinetics, conversion, side reactions including the adenylylated dead-end
   species, solid-phase and immobilised ligation variants, scale-up behaviour, enzyme
   sourcing and GMP grade availability.

B. **Filtration-led purification.** Every applicable filtration mode, membrane chemistries
   and cutoffs, what each clears and what it cannot, achievable resolution between product
   and each impurity class, cascade and multi-stage configurations, yield and flux
   behaviour, fouling, scale-up rules.

C. **UF/DF in depth.** Membrane selection for a species of roughly seven kilodaltons,
   retention behaviour versus nominal rating, diafiltration design, flux models, shear,
   concentration polarisation, gel layer, hold-up and recovery, single-use versus reusable,
   cleaning and reuse validation.

D. **Falling film evaporation.** This is unusual for oligonucleotides, so establish first
   whether it is appropriate at all. Thermal exposure and residence time versus product
   stability, duplex integrity, vacuum and boiling point elevation, achievable concentration,
   viscosity limits, foaming with any crowding agent or surfactant present, fouling and
   cleaning, materials of construction, scale-down representation, heat transfer design.

E. **Spray drying.** Whether the duplex survives atomisation and drying, or whether single
   strands are dried and annealed later. Glass transition and amorphous stability, excipient
   and carrier selection, inlet and outlet temperature design, particle engineering, residual
   moisture, cyclone and wall losses, yield at small scale versus large, containment,
   sanitisation and microbial control of the dryer, aseptic or low-bioburden operation.

F. **Microbial control and contamination control strategy.** Bioburden and endotoxin across
   an aqueous, enzyme-containing process, hold times, water quality per step, nuclease
   control proportionate to a modified duplex, sanitisation of evaporator and dryer,
   filter validation, and where the sterile or low-bioburden boundary should sit.

G. **Greenfield capital design.** Facility concept for THIS train specifically. Area
   classification, the hazardous-area footprint given the actual solvent duty of this route,
   utilities and their loads, layout and flows, expansion strategy, what drives capital cost,
   and how this train's capital profile differs from a chromatography and lyophilisation train.

H. **Process development, benchtop to scale.** Stage-appropriate development approach,
   scale-down models and their qualification, design of experiments strategy, which
   parameters must be characterised, what breaks first on scale-up for each unit operation,
   and the specific scale-dependent failure modes for evaporation and spray drying.

I. **Tech transfer and engineering package.** The document set, mass and energy balances,
   governing equations, equipment specification and sizing basis, instrumentation,
   process analytical technology by unit operation, control strategy, and the ICH and
   engineering standards that bind.

J. **Risks and open questions.** Synthesise from all other streams. Every risk with cause,
   effect, affected quality attribute, detectability, and proposed mitigation. Every open
   question with why it matters and whether it blocks a decision.

K. **Information architecture.** See deliverable 4 below.

## 4. Equations and models expected

Where the engineering rests on a model, give the equation, define every term, state its
assumptions and its validity range, and say what data is needed to use it. At minimum
cover: tangential flow flux and the concentration polarisation and gel models,
diafiltration clearance as a function of diavolumes, sieving and rejection coefficients,
membrane cascade staging, evaporator heat transfer and overall coefficient, boiling point
elevation, spray dryer mass and energy balance, droplet drying kinetics, Peclet number and
its effect on particle morphology, glass transition and moisture relationships, ligation
reaction kinetics and conversion, and overall process mass balance with yield propagation.

State clearly which equations are well founded for this application and which are borrowed
from another industry and may not transfer.

## 5. Quality bar

- **Never invent a number.** If a value is not in a source you actually read, do not state
  it. Write [TBD] and add the gap to the open questions register. A plausible fabricated
  range is worse than an acknowledged blank, because it will be designed against.
- **Tag every claim** with the scheme in conventions/how-to-use.md.
- **Record scale and system for every literature result.** A bench result on unmodified RNA
  does not transfer to kilograms of modified phosphorothioate siRNA, and the note must make
  that visible. Use the literature note template.
- **Cite everything** with a resolvable reference. Where you could only reach an abstract,
  say so and mark the note as incomplete.
- **Separate what is established from what you inferred.** Your own reasoning is valuable
  but must be labelled as reasoning.
- **Disagree with the existing scaffold where warranted**, and with the process concept
  itself where the evidence warrants. An honest negative finding is the most useful output
  this exercise can produce.

## 6. Deliverables

1. Full process content for enzymatic ligation, filtration purification, UF/DF, falling
   film evaporation, and spray drying, as unit operation entries against the existing
   template, with microbial control integrated rather than bolted on.
2. Greenfield capital design considerations for this specific train.
3. Populated risk register and open questions register.
4. **An information architecture recommendation, then implement it.** Assess how this body
   of information should be portrayed so it can be retrieved when needed. Consider at least:
   markdown and CSV in the repository as now; a generated browsable index or dashboard
   published as an artifact; a spreadsheet workbook; a wiki. Weigh them on retrieval speed,
   maintainability, and whether non-git users can contribute. Recommend one, say why, and
   build it. Do not skip the recommendation and just pick.
5. Process development considerations from benchtop through scale-up.
6. Tech transfer package content: documents, factors, equations, mass and energy balances,
   equipment, instrumentation, and PAT.
7. Anything material you find that I did not ask for. Flag it prominently rather than
   burying it.

Put content in the existing files where it belongs, and in new files where that is more
digestible. Follow the existing naming conventions. Keep the registers as the controlled
artifacts and keep prose referencing register IDs rather than restating values.

## 7. Practical constraints

- **Test network access early** and tell me what you can and cannot reach. Web search and
  page fetching are separately gated in this environment. If you cannot reach a source,
  record it as a gap rather than working around it with guesses.
- Paywalled publisher content will not be reachable. Build a prioritised reading list of
  what I should pull manually.
- Validate before you finish: every CSV parses with consistent columns, every internal link
  resolves, every referenced identifier is defined in a register.
- Commit to this session's designated branch and push. Do not open a pull request unless
  I ask.

## 8. Start

Present your plan covering: the team decomposition, what each team will research and
produce, the sequencing and dependencies, how you will handle the central question in
section 2, your proposed information architecture options, and the expected shape of the
output. Then wait for my approval.
```
