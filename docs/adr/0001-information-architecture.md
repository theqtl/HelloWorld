# ADR 0001 — Information architecture

**Status:** accepted · **Date:** 2026-09-17 · **Supersedes:** nothing

## Context

The brief asked for the presentation layer to be designed before any content was written, for five
candidate architectures to be weighed, and for the rejects to be justified. That justification was
never written down. The brief also recorded that an earlier attempt using "markdown files and CSV
registers in a folder tree" had been rejected as not user friendly, specifically for process flow
diagrams and equations — and what was built is, on its face, close to that. This record settles the
question rather than leaving it implicit in the repository layout.

The six requirements the architecture has to satisfy: real vector flow diagrams whose stream numbers
tie to the mass balance; properly typeset equations with terms, assumptions and validity; fast
retrieval of a single parameter, equation or unit operation; tabular data that stays sortable **and
filterable**; usability by people who do not use git, who must be able to read and ideally
contribute; and cross-linking from a parameter to its unit operation, equation, risk and instrument.

## Decision

**Keep the current architecture: structured CSV source data, a standard-library Python generation
layer, and an MkDocs Material site. Migrate nothing.**

The rejected-attempt concern is answered on its own terms. The objections were diagrams and
equations. Diagrams are now vector SVG with stream numbers checked against `data/streams.csv` by an
automated test, and equations are typeset through MathJax with every term, assumption and validity
range stated. A folder of Markdown and CSV is the *source*, not the presentation layer.

## Options considered

**A static documentation site published from the repository — chosen, in combination with E.**
Gives search, navigation, cross-linking and a publishing path for free, and keeps the whole package
reviewable as a diff.

**A hybrid of structured source data and a generated presentation layer — chosen, in combination
with A.** This is the property worth most here: a number lives in one place. The mass balance is
executable, every register page is generated from a CSV, and a figure cannot be edited into
inconsistency in one page while staying stale in another.

**An interactive HTML application published as an artifact — rejected as the primary surface.** No
search index, no deep links, no reviewable diff, no hand-off path to an engineering firm. Its one
real virtue, click-a-stream interactivity, can be added inside the site later if anyone asks for it.

**A notebook or computational document — rejected as a format, adopted in spirit.** Notebooks diff
badly, store outputs, and quality and capital-project readers will not open one. But its core virtue,
live numbers, is real: it is delivered here by the generation layer instead, and the remaining
hand-typed numbers in prose are a known weakness worth closing with templating.

**A spreadsheet workbook for the quantitative layer — rejected as the published layer, recommended
as the editing surface.** No version control of formulas, no review gate, no cross-links. But it is
the strongest available answer to the contribution requirement, and it is worth revisiting as an
*input* path that generates the CSVs through a pull request.

**Quarto, the serious challenger — rejected for now, recommended downstream.** It buys live inline
numbers, numbered cross-referenceable equations and figures, and web, PDF and Word output from one
source. That third item matters more than the brief realised: a capital team handing a package to an
engineering firm eventually wants an issued, page-numbered, revision-controlled document. It loses
because each advantage has a cheaper answer inside the current stack, and because Quarto optimises
for a document you issue once while this is a knowledge base with sixteen open questions that people
will browse for months. Adopt it, or pandoc, as an exporter — never as the authoring layer.

Sphinx and Docusaurus were also considered. Sphinx's custom domains would solve cross-referencing
properly but at a steep authoring cost that lands hardest on the non-git contributors this project
is already worried about. Docusaurus has the best browsing experience and real versioning, but its
MDX parser treats `{` and `<` as syntax, and this content is saturated with `2'-OMe`, `<1 kDa` and
`>95%` arriving from CSV cells that domain experts are meant to edit freely.

## Consequences

At the time of this decision two requirements were **not** met, and both were orthogonal to the
choice of site generator, which is the decisive argument against migrating to fix them. The dated
update below records what has since closed and what has not:

- **Filterable tables.** The register tables sort but do not filter. This is survivable at today's
  sizes and will not be at Tier 2 sizes. The fix is to emit semantic HTML from `gen/tables.py` and
  bind a filtering component over it.
- **Contribution without git.** There is no edit affordance at all, and a non-git reader who finds a
  generated register page on GitHub and edits it would be editing a git-ignored artifact that the
  build overwrites. The fix is an edit action plus structured issue forms mirroring the CSV columns,
  and ultimately a controlled workbook that opens a pull request.

A third weakness is structural: the flowsheet is drawn by hand while `data/streams.csv` already
holds the topology as an edge list. It is the one artifact that escaped the single-source discipline,
and it silently lost its product-outlet arrow as a result. A drift test now guards it; generating it
from the data is the real fix.

### Update — Tier 2, 2026-09-20

Two of the three are closed, and neither needed a different site generator, which is the prediction
above holding.

- **Filterable tables — met, by a different route than the one proposed.** The fix above assumed
  `gen/tables.py` would emit semantic HTML. It does not, deliberately: it still emits Markdown pipe
  tables, and a test asserts the generator emits no HTML tags, which keeps its output diffable and
  keeps the registers readable on GitHub. The filter is instead progressive enhancement over the
  rendered table (`docs/javascripts/tablefilter.js`), bound to Material's `document$` so it survives
  instant navigation, and anchored outside Material's horizontal scroll wrapper — inside it, the
  control scrolled out of view on exactly the widest registers. Register pages always get a filter;
  elsewhere only tables large enough to need one, because a row count alone does not make a table a
  register.
- **Hand-drawn flowsheet — closed as proposed.** `gen/flowsheet.py` now derives
  `docs/diagrams/bfd.svg` from the `data/streams.csv` edge list and the equipment register, so the
  last artifact outside the single-source discipline is inside it. The drift test now guards a
  generated file rather than a hand-maintained one.
- **Contribution without git — still open.** Unchanged. There is no edit affordance, and a non-git
  reader who edits a generated register page is editing a git-ignored build artifact that the next
  build overwrites. The fix remains an edit action plus structured issue forms mirroring the CSV
  columns, and ultimately a controlled workbook that opens a pull request.

### Update — Tier 3 slice 1, 2026-09-21

The control strategy moved from prose into `data/controls.csv` and `data/instruments.csv`, and the
CPP → CQA matrix became a generated page like the registers and the balance. This is the decision
above being used for what it was chosen for rather than extended: no new mechanism, one more
generator module, three more generated pages.

It did surface one thing the ADR did not anticipate. The argument this repository most needed to
make checkable was a **negative** one — that a control claimed in prose could not be enforced,
because no instrument can measure the quantity at process conditions. A knowledge base built on
"every value lives once, flagged" has no natural place for an assertion about something that does
*not* exist. The answer was to give absence its own vocabulary — a `not_measurable` control type
and a required `measurement_mode` on every instrument — so that the gap is a row rather than a
silence. That generalises: the data layer earns its keep most when it can represent what the
package is missing, not only what it has.

## What would reverse this decision

- An issued, revision-controlled document becomes the primary deliverable rather than a browsable
  site — then the authoring layer should follow the deliverable, and Quarto wins.
- Formal numbered citations in a regulatory style become a requirement — Quarto and pandoc do this
  natively and MkDocs has no good answer.
- Genuine what-if interactivity is asked for repeatedly — a slider that redraws the flowsheet and
  rebalances the train cannot be done in a static site.
- The identifier vocabulary grows past roughly a thousand entities, at which point regex-based
  auto-linking starts producing false positives and Sphinx's semantic domains become the principled
  answer.

Needing versioned documentation does **not** reverse it; that is available for MkDocs directly.
