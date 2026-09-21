# siRNA Drug Substance Process & Greenfield cGMP Facility

Knowledge base for an **enzymatic-ligation** siRNA drug-substance (DS) process and its greenfield
cGMP facility: filtration-led purification, evaporation, spray drying, microbial control — fully
aqueous, no solvents.

The presentation layer is **generated from a single structured data layer**. Every parameter,
stream, equipment item, buffer, risk, question, instrument, control and citation lives once in
`data/*.csv`. A Python layer (`gen/`) computes the mass and energy balance and emits the Markdown pages; a
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) site publishes them to GitHub Pages.

## Layout

| Path | Contents |
|---|---|
| `data/*.csv` | Single source of truth: parameters, streams, equipment, buffers, utilities, risks, questions, sources, scenarios, impurities, instruments, controls. |
| `gen/` | Generation + executable mass/energy balance (`balance.py`), the impurity-fate overlay (`impurity.py`), the flowsheet (`flowsheet.py`), the CPP→CQA control matrix (`controls.py`), and tests (`test_balance.py`). Standard library only. |
| `docs/` | Site sources: findings, process pages, equations, diagrams, facility, registers. |
| `mkdocs.yml` | Site configuration. |
| `.github/workflows/pages.yml` | CI: test, generate, build, deploy to Pages. |

## Build locally

```bash
pip install -r requirements.txt
python -m pytest gen -q      # data integrity + balance tests
python -m gen.build          # generate register + balance pages from data/
mkdocs serve                 # preview at http://127.0.0.1:8000
```

Generated Markdown (register pages, `balance/results.md`, `balance/impurities.md`, `process/streams.md`,
`process/controls.md`) and `diagrams/bfd.svg` are produced by `python -m gen.build`; the Markdown is
git-ignored, file by file, in `.gitignore`. Edit the CSVs, never the generated pages.

## Publishing to GitHub Pages

The workflow builds and deploys on push. Enable it once in **Settings → Pages → Build and
deployment → Source: GitHub Actions**. Until then the site is buildable and previewable locally
but not live.

## Provenance discipline

Every numeric value is flagged **fact** (cited), **inference** (our reasoning/arithmetic), or
**assumption** (illustrative placeholder, registered as an open question). Unsourced values are
left blank and recorded as gaps — never invented. The mass balance runs on flagged assumption
inputs and refuses to run on a blank, so a gap cannot become a fabricated result.

`data/sources.csv` carries a `verified` column recording who checked each source against the
claims made from it, and when. A citation audit on 2026-09-17 checked all twenty-five original
sources: every cited work existed, but several numbers were attached to real sources that do not
contain them. Those were corrected or blanked, and the test suite now lints prose citations,
so the same class of error fails the build rather than shipping.

## Status

Tier 1 established the architecture, the data model, the executable balance across illustrative
scenarios, the two headline findings (filtration closure; duplex survival in spray drying), and the
seeded registers. Tier 2 added the full energy balance (sensible heat, drying-gas heating and plant
losses), species-resolved impurity fate, the contamination-control strategy with CIP/SIP and a
health-based exposure limit, filterable register tables, a flowsheet generated from
`data/streams.csv`, and a per-item sizing basis, materials of construction and turndown basis in the
equipment register.

The first Tier-3 slice added the **control strategy as data**: an instrument register carrying every
instrument the concept implies with its measurement mode, and a generated CPP→CQA matrix in which
every control names the parameter it acts on, the instrument that enforces it and the question that
blocks it. Most acceptance bases in it are assumption-flagged placeholders — the deliverable is a
**checkable structure**, not a control strategy a contract manufacturer could execute. It also makes
two things representable that prose could not: a measurement that exists but cannot close a loop on
its own stream (`at_line_only`, Q-042), and an enzyme-clearance route carried as two branches with
neither chosen (Q-050). The facility capital concept and process flow diagrams with instrument tags
remain Tier 3, marked as stubs or registered gaps.

The slice also got something wrong and is worth reading for that. Its first version held that
variable-pathlength slope spectroscopy is inherently at-line, wrote that into a question, a control
row and a *guard*, and shipped green. The technique is in fact used in-line; what is true is narrower
and quantitative — at our own registered retentate concentration the pathlength the reading needs
falls below the published floor for an in-line cell. The control type is therefore `at_line_only`
rather than `not_measurable`, and the decision is now **computed** from two registered parameters so
it self-corrects if either moves. A guard is only as good as the claim it encodes, and a green suite
says nothing about whether that claim is true.

The information-architecture decision is recorded in
[`docs/adr/0001-information-architecture.md`](docs/adr/0001-information-architecture.md), including
the options rejected and what would reverse the choice. Of the requirements it did not meet at the
time, one is still open — a contribution path for people who do not use git — and is documented
there, alongside a dated update recording what Tier 2 closed.
