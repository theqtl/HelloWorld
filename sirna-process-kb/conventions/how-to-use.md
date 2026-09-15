# How to use this knowledge base

## Principles

1. **One fact, one home.** Every parameter, material, and requirement has exactly one
   authoritative entry. Everything else links to it. Never restate a value.
2. **Every claim is cited or flagged.** A statement is either backed by a reference in
   `02-knowledge/literature/`, backed by internal data, or tagged `[SEED]` / `[ASSUMED]`
   / `[TBD]`. Untagged, uncited assertions are the thing this repository exists to prevent.
3. **Questions are first-class.** An unanswered question goes in
   `11-open-questions/open-questions.csv` with an owner. Questions are not comments
   buried in prose.
4. **Decisions are recorded, not remembered.** Any choice that closes off an option gets
   a decision record in `10-decisions/`. Include the options rejected and why.
5. **Registers are machine-readable.** Equipment, buffers, parameters, risks, questions,
   and assumptions live in CSV so they can be sorted, diffed, and exported into formal
   documents.

## Confidence tags

Use these inline, in bold, at the point of the claim.

| Tag | Meaning |
|---|---|
| `[SEED]` | Generic domain knowledge placed to show structure. Unverified. Do not design against. |
| `[ASSUMED]` | A working assumption. Must also appear in `10-decisions/assumptions-register.csv`. |
| `[TBD]` | A known gap. Must also appear in `11-open-questions/open-questions.csv`. |
| `[LIT]` | Supported by literature. Must carry a citation key. |
| `[INT]` | Supported by internal data. Must carry a study or report reference. |
| `[VEN]` | Vendor claim. Treat as marketing until independently confirmed. |

## Citation keys

Literature notes are named `AuthorYear-shortslug.md`, for example
`Hull2021-ip-rp-oligo-purification.md`. Cite in text as `[LIT: Hull2021]`.

## Adding a unit operation

Copy `templates/TEMPLATE-unit-operation.md` into `03-process/downstream/` as
`UO-NN-shortname.md`. Fill every section. If a section does not apply, write
"Not applicable" and why. Do not delete sections, because the uniform shape is what
makes the set comparable and exportable.

## Adding literature

Copy `02-knowledge/literature/TEMPLATE-lit-note.md`. The note captures what the source
actually demonstrates and, critically, **at what scale and on what molecule**. A result
from a 10 nmol bench reaction on unmodified RNA does not transfer to a kilogram of fully
modified phosphorothioate siRNA, and the note must make that visible.

## Review cadence

Suggested, adjust to the project. **[ASSUMED]**

- Open questions and risk register: reviewed weekly during design.
- Unit operation entries: reviewed at each stage gate.
- Control strategy: reviewed at each regulatory milestone.
