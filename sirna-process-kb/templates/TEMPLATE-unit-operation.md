# UO-NN — <Unit operation name>

> Status: Draft | In review | Baselined
> Owner:
> Last reviewed:

## 1. Purpose and position in the train

What this step achieves, and what would happen if it were removed. Upstream step and
downstream step by UO number.

## 2. Mechanism

The physical or chemical basis of separation, conversion, or conditioning. Enough that a
reader can predict how the step responds to a change in feed.

## 3. Stream definition

| | Description | Key attributes | Typical values |
|---|---|---|---|
| Feed | | | |
| Product out | | | |
| Waste out | | | |

## 4. Equipment

Reference rows in `05-equipment/equipment-register.csv` by ID. Include contact materials,
wetted surfaces, single-use versus stainless, and scale bracket.

## 5. Consumables, buffers and reagents

Reference rows in `04-materials/buffer-register.csv` and `reagent-register.csv` by ID.
Include grade, compendial status, and quantity per batch.

## 6. Process parameters

| ID | Parameter | Type | Target | Range | Basis | Impact |
|---|---|---|---|---|---|---|

Type is CPP, KPP, or GPP. Impact names the CQA affected. Basis is a citation, an internal
study, or a confidence tag.

## 7. In-process controls and PAT

What is measured, where, by what technique, and what decision it drives. Distinguish
in-line, on-line, at-line, and off-line. Cross-reference `06-pat-analytics/`.

## 8. Scale-up and scale-down

The scaling rule and the constraint that breaks first. State the scale-down model and
its qualification status.

## 9. Impurity fate

Which process-related and product-related impurities are cleared, which are formed, and
which pass through unchanged. This is the section that makes the control strategy writable.

## 10. Failure modes

Reference rows in `09-risk/risk-register.csv` by ID. Include the detection method and the
recovery action for each.

## 11. Cleaning, changeover and containment

Cleaning approach, hold times, campaign versus dedicated, carryover limits, operator
exposure controls.

## 12. Environmental and utility load

Solvent volumes, water, waste streams, energy, recovery options.

## 13. Open questions

Reference rows in `11-open-questions/open-questions.csv` by ID.

## 14. References

Citation keys into `02-knowledge/literature/`.
