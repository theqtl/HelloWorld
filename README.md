# siRNA Drug Substance Process & Greenfield cGMP Facility

Knowledge base for an **enzymatic-ligation** siRNA drug-substance (DS) process and its greenfield
cGMP facility: filtration-led purification, evaporation, spray drying, microbial control — fully
aqueous, no solvents.

The presentation layer is **generated from a single structured data layer**. Every parameter,
stream, equipment item, buffer, risk, question, and citation lives once in `data/*.csv`. A Python
layer (`gen/`) computes the mass and energy balance and emits the Markdown pages; a
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) site publishes them to GitHub Pages.

## Layout

| Path | Contents |
|---|---|
| `data/*.csv` | Single source of truth: parameters, streams, equipment, buffers, utilities, risks, questions, sources, scenarios. |
| `gen/` | Generation + executable mass/energy balance (`balance.py`) and tests (`test_balance.py`). Standard library only. |
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

Generated Markdown (register pages, `balance/results.md`, `process/streams.md`) is git-ignored;
`python -m gen.build` recreates it. Edit the CSVs, never the generated pages.

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
equipment register. The facility capital concept, process flow diagrams with instrument tags, and
the control strategy remain Tier 3, marked as stubs or registered gaps.

The information-architecture decision is recorded in
[`docs/adr/0001-information-architecture.md`](docs/adr/0001-information-architecture.md), including
the options rejected and what would reverse the choice. Of the requirements it did not meet at the
time, one is still open — a contribution path for people who do not use git — and is documented
there, alongside a dated update recording what Tier 2 closed.
