# siRNA Process Knowledge Base

A single, version-controlled home for everything that feeds the design of an siRNA
drug substance process and the greenfield cGMP facility that will run it:
literature, document reviews, blockmer preparation, enzymatic ligation, downstream
unit operations, buffers, reagents, process conditions, equipment and system
requirements, PAT options, risks, decisions, and open questions.

---

## What is this kind of thing called?

There is no single industry term, which is why it is hard to name. What is being
described here is really **three established artifacts that overlap**, plus the
working library that feeds all three.

| Layer | Industry name | What it is | Where it lives here |
|---|---|---|---|
| The library | **Process Knowledge Repository** / Process Knowledge Management (PKM) system | The ICH Q10 "knowledge management" enabler. Durable, searchable, cited process understanding that outlives any one project or person. | `02-knowledge/`, `03-process/` |
| The engineering output | **Basis of Design (BoD)** and **User Requirements Specification (URS)** | The front-end deliverables that a greenfield capital project is designed and built against. | `05-equipment/`, `07-facility/` |
| The regulatory output | **Control Strategy** (ICH Q11) inside a **Development Report** | The CMC narrative linking QTPP to CQAs to CPPs to controls, filed in Module 3. | `01-product/`, `08-quality-regulatory/` |

Informally, people call the whole bundle a **"process book"**, a **"tech package"**,
or a **"technology transfer package"**. In engineering-procurement-construction work
the front end is the **Process Design Basis**. None of those names covers the whole
thing on their own.

### Recommended name for this repository

Call it the **siRNA Process Knowledge Base**, and treat the formal documents as
*outputs rendered from it* rather than as separate parallel documents. The mapping
from knowledge base entries to formal deliverables is defined in
[`00-governance/document-map.md`](00-governance/document-map.md).

The key discipline: **write once, here, and cite it everywhere else.** A URS that
restates a process parameter instead of referencing it will drift out of date the
moment the parameter changes.

---

## How it is organised

| Folder | Contents |
|---|---|
| `00-governance/` | Scope, charter, how KB entries roll up into formal documents |
| `01-product/` | QTPP, CQA register, siRNA modality notes |
| `02-knowledge/` | Literature notes and topic reviews, one note per source |
| `03-process/` | Process overview, blockmer prep, ligation, one file per downstream unit operation |
| `04-materials/` | Buffer and reagent registers, raw material strategy |
| `05-equipment/` | Equipment register, URS templates, utilities and systems |
| `06-pat-analytics/` | PAT options by unit operation, analytical method register |
| `07-facility/` | Greenfield design basis, area classification, personnel and material flows |
| `08-quality-regulatory/` | Regulatory landscape, control strategy, validation approach |
| `09-risk/` | Risk register and risk assessment method |
| `10-decisions/` | Decision log, decision record template, assumptions register |
| `11-open-questions/` | Open questions with owners and blocking status |
| `templates/` | The unit operation template and other reusable forms |
| `conventions/` | How to use, contribute to, and cite this knowledge base |

## Start here

1. Read [`conventions/how-to-use.md`](conventions/how-to-use.md).
2. Read [`03-process/process-overview.md`](03-process/process-overview.md) for the block flow.
3. Pick a unit operation in `03-process/downstream/` and work it against the template.

## Status

This is a **seeded scaffold**. Content marked `[SEED]` is generic domain knowledge
placed to show the shape of a complete entry. It has not been verified against
primary literature or against any specific molecule, and **must not be used as a
process basis until reviewed and cited**. Content marked `[TBD]` is an explicit gap.
