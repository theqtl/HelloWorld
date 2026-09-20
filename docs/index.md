# siRNA drug substance: process & greenfield cGMP facility

A knowledge base for an siRNA drug-substance (DS) process built on **enzymatic ligation** of
chemically synthesised blocks, purified by a **filtration-led** train, concentrated by
**evaporation**, and dried by **spray drying**, with **microbial control** across the whole
process. It is the source for the process concept, the mass and energy balance, the governing
equations, the equipment and risk registers, and the facility concept to be handed to an
engineering firm.

## How this site is built

The presentation layer is **generated from a single structured data layer**. Every parameter,
stream, piece of equipment, buffer, risk, question, and citation lives once in `data/*.csv`.
A small Python layer (`gen/`) computes the mass and energy balance and emits the register and
balance pages. A number lives in one place and appears everywhere it is used.

- **Fast retrieval.** Use the search box for any parameter, equation, or unit operation.
- **Queryable tables.** Register tables are click-to-sort and searchable.
- **Typeset equations.** See [Equations](equations/index.md).
- **Vector flowsheet.** See [Diagrams](diagrams/index.md).

## Provenance discipline

Every numeric value carries a provenance flag, and nothing is invented:

- <span class="prov-fact">fact</span> — from a cited source (see the [source](registers/sources.md) and its scale/system).
- <span class="prov-inference">inference</span> — our reasoning or arithmetic, labelled as such.
- <span class="prov-assumption">assumption</span> — an illustrative placeholder, registered as an [open question](registers/questions.md).

A value we could not source is left **blank** and recorded as a gap, never filled with a
plausible-looking number.

## Fixed design decisions

Strand assembly by enzymatic ligation; filtration-led purification (chromatography only where
filtration provably cannot do the job); evaporation for concentration; spray drying (lyophilisation
cannot meet throughput); microbial control throughout. **The process is fully aqueous — no organic
solvents.** The boundary starts at received, purified, 5'-phosphorylated blocks; block synthesis
(solvent-intensive) is a supplier operation.

## Start here

- **[Does the filtration-led train close?](findings/filtration.md)** — the central purification finding.
- **[Does the duplex survive spray drying?](findings/spray-drying.md)** — the central drying finding.
- **[Mass & energy balance](balance/index.md)** — executable, scenario-driven.
- **[Open questions](registers/questions.md)** — Q-001 (annealing / product form) and Q-002 (real annual demand) drive everything.

!!! note "Scope of this release (Tier 2)"
    Tier 1 established the architecture, the data model and build, the two headline findings, the
    executable mass balance across illustrative throughput scenarios, and seeded registers. Tier 2
    added the full energy balance, species-resolved impurity fate, the contamination-control
    strategy with CIP/SIP, filterable registers, a generated flowsheet, and equipment sizing basis
    and turndown. The facility capital concept, process flow diagrams with instrument tags, and the
    control strategy are Tier 3 and are marked as stubs or registered gaps where not yet built.
