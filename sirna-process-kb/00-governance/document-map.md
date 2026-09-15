# Document map: knowledge base to formal deliverables

The knowledge base is the source. Formal documents are rendered from it and cite it.
Nothing below should restate a value that lives in a register.

| Formal deliverable | Standard or driver | Sourced from |
|---|---|---|
| Process Design Basis / Basis of Design | EPC front-end engineering | `03-process/`, `04-materials/`, mass balance |
| User Requirements Specification, per system | ASTM E2500, GAMP 5, EU GMP Annex 15 | `05-equipment/`, `03-process/` UO sections 4 and 6 |
| Process Flow Diagram and P&ID basis | Engineering | `03-process/process-overview.md` |
| Process Description / Manufacturing Process Description | ICH Q7, Module 3.2.S.2.2 | `03-process/downstream/` UO sections 1 to 6 |
| Quality Target Product Profile | ICH Q8 | `01-product/qtpp.md` |
| CQA justification | ICH Q8, Q11 | `01-product/cqa-register.md` |
| Control Strategy | ICH Q10, Q11 | `08-quality-regulatory/control-strategy.md`, UO sections 6, 7, 9 |
| Quality Risk Management file | ICH Q9 | `09-risk/` |
| Development Report | ICH Q11 | `02-knowledge/`, `10-decisions/` |
| Validation Master Plan | EU GMP Annex 15 | `08-quality-regulatory/validation-approach.md` |
| Analytical Procedure lifecycle docs | ICH Q14, Q2(R2) | `06-pat-analytics/analytical-method-register.csv` |
| Facility concept and layout basis | ISPE Baseline Guides | `07-facility/` |
| Containment and EHS basis | Occupational hygiene, local codes | UO section 11, `07-facility/` |

## The rendering rule

When a formal document is issued, it captures a **snapshot** of the knowledge base at a
stated commit. Record the commit hash in the document header. Subsequent knowledge base
changes do not silently alter an issued document, but the delta is always computable.
