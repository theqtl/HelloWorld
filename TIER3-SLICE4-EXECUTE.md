# Tier-3 slice 4 — execution brief

Read `TIER3-SLICE4-PLAN.md` first. It is the audited plan and it is the authority; this file is only
the working order and the paste-able prompt.

## The prompt

```
Read TIER3-SLICE4-PLAN.md and TIER3-SLICE4-EXECUTE.md at the repo root, then implement the plan
phase by phase.

Branch: claude/sirna-evidence-research-k8btv0, restart from origin/main
(git fetch origin main && git checkout -B claude/sirna-evidence-research-k8btv0 origin/main).
Never push to main — the site deploys from it.

Work one phase at a time. After each phase run all three gates and stop to report before starting
the next. Do not open a PR until I ask.

The plan's decisions are settled — do not re-litigate them. Its FINDINGS are a different matter:
re-verify any finding you are about to rely on, by execution or by retrieving the document, before
it shapes code. Three audit rounds already overturned findings in this plan, including one of my
own corrections, so treat every number in it as a claim with a name on it rather than as fact.

Report at the end of each phase what you verified by execution versus what you took from the plan.
```

## Progress — read this before starting

| Phase | State | Commit |
| --- | --- | --- |
| 0 — separate the two axes | **done** | `bd9b91e` |
| 1 — refuse a fabricated value; resolve buffer references | **done** | `35ec908` |
| 2 — the vocabulary, the fields, the visibility | **done** | — |
| 3 — the corrections the audits forced | **next** | — |
| 4 — buffers | open | — |
| 5 — sizing, and the citable cleaning criteria | open | — |

**Baseline is now 202 tests, not 147.** Phase 0 took it to 155, phase 1 to 163, phase 2 to 202.

**What phase 0 delivered**, so phase 2 does not redo it: `envelopes.provenance` renamed to
`endpoint_sourcing` with its own `ENDPOINT_SOURCING` constant kept deliberately separate from
`PROVENANCE_VOCAB`; `PROVENANCE_VOCAB` moved into `gen/dataio.py`; `provenance_offenders()` there
now validates **every** register carrying the column via `PROVENANCE_REGISTERS`, which **already
includes `buffers`** — one of the three buffer holes phase 1 was scoped to close was closed here;
`BRACKET_VERDICTS`, `DISPOSITIONS` and `RISK_UNIT_OPS` relocated out of the renderer and the test
file; the four inline re-listings replaced with imports.

**What phase 1 delivered.** `value_written_where_refused()` in `gen/envelope.py`, guarded by
`test_a_refused_bracket_is_not_written_as_a_value_either`. The rule is **not** "a `not_a_range` row
may carry no value" — that would contradict the policy its sibling states, which allows "a blank or
a clearly-labelled single point". A value is legitimate as `fact`/`inference` **with a source**; an
`assumption` value is refused. **Keyed on `not_a_range` alone**, never `single_point`. Plus a
bidirectional buffer-reference sweep, `buffers` added to the source-key sweep, and the first buffer
mutation coverage in the harness's history.

**A deviation from the plan, made deliberately.** The plan called for a structured `buffer_ref`
column. Phase 1 swept prose instead, for two reasons: three of the eighteen mentions
(`infoneeds.satisfied_by`) are **already** structured and **already** resolved by
`satisfied_universe()`, so a column would have carried the same reference twice — which is how two
registers start disagreeing — and prose sweeping is the idiom this repo already uses for the same
problem (`Q-\d{3}`). The structured column is still worth having for rendering links; it is a
feature, not an integrity fix, and it is **not** done.

**What phase 2 delivered.** `judgement` as the fourth `PROVENANCE_VOCAB` value, with three
obligations enforced rather than described. `est_value`/`basis`/`falsifier` on the three registers
named by `ESTIMATE_REGISTERS` (`parameters`, `buffers`, `scenarios`), and `judgement` **refused by
guard** on the other eight. `estimate_offenders()` in `gen/envelope.py`, called from `validate()` so
it raises at build time: an estimate may not write its register's quantity column, must state a basis
whose `SRC-`/`P-`/`EQ-`/`Q-` tokens resolve, may not rest on a source graded `abstract-only`,
`record-only` or `not-retrieved`, must name a question, and that question's status must be `open`.
`QUESTION_STATUS` added as a vocabulary (all 52 rows already passed it). `_with_provenance_markers`
beside `_with_bracket_verdicts`, guarded over the transform's return value. Census page at
`docs/registers/estimates.md`. **No row carries the new provenance** — the machinery landed before
any number rested on it, which is why nine of the thirty-nine new tests are mutation cases that
supply the row.

**Where phase 2 chose differently from the plan, and why.**

- **The scope of `est_value`/`basis`/`falsifier` is three registers, not eleven and not two.** The
  plan said "every register where it is legal" without saying which. The line is drawn on a property
  of the register — *does a row carry a quantity of its own that cannot be referenced out to
  `parameters.csv`* — and `ESTIMATE_REGISTERS` records the reason for each of the three. `judgement`
  is refused on the other eight **by guard**, so the line is enforced rather than assumed.
  `equipment.turndown` looks like a fourth case and is not: all seven rows state a basis in prose
  with the numeric ratio explicitly pending, verified row by row.
- **The cell marker is Markdown, not the CSS chip.** `test_md_table_emits_markdown_only` locks the
  register tables to pipe tables, and the precedent the plan itself points at
  (`_with_bracket_verdicts`) injects `**no audit**`. So the cell reads `**estimate only**` /
  `<n> **judgement**`, and `prov-judgement` is for hand-written prose, where there is no column.
- **`_CITATION` is unchanged; the rule is a second guard keyed on the QUANTITY.** `prov-judgement` is
  deliberately absent from `_CITATION`, so a quantity near the chip still needs a real reference, and
  `test_an_estimated_quantity_in_prose_names_the_parameter_it_estimates` adds the other half. Keyed
  on the chip it immediately failed on `docs/index.md`'s own legend — which labels no number and must
  not name a parameter, since none carries an estimate yet.
- **Most of the "stale three-value enumerations" were not enumerations.** Only three sites enumerate
  the vocabulary as closed: `docs/index.md`, `README.md:42-44` and `gen/build.py:43-45`. Those are now
  four-valued. `gen/__init__.py:2`, `gen/impurity.py:85`, `docs/balance/index.md:10`,
  `docs/techtransfer/index.md:24` and `README.md:67` say "assumption-flagged inputs", which is
  **still true** and stays true by construction — so each was strengthened to say *why* an estimate
  cannot be among them, rather than edited to look updated. The plan's `gen/build.py:219` is
  `return scn["label"], rows`; its build.py line numbers drifted in phases 0-1.

**Two defects found while building phase 2, both by the guards rather than by reading.**

1. **`.gitignore` enumerates the generated pages one by one, and nothing related that list to
   `_generated_pages()`.** The census page was generated, navigated, linked — and tracked by git, so
   every build would have shown it as a diff. Fixed, and `test_every_generated_page_is_gitignored`
   now closes the class.
2. **`test_numeric_claims_in_prose_carry_a_citation` has never policed a percentage.** `_QUANTITY`
   ends its unit alternation with `\b`, and a word boundary after `%` needs a WORD character next —
   so `0.5%`, `0.5 %.` and `0.5% of` all fail to match. Measured, not reasoned: **7 prose lines
   across 4 pages** are quantities under a corrected regex, carry no citation within the ±3-line
   window, and pass today (`docs/equations/index.md:77`, `docs/findings/filtration.md:54/152/156`,
   `docs/sources/ligation-evidence.md:61/62/63`). **NOT fixed here** — it changes an existing guard's
   semantics and each of the 7 needs judging, which is phase 3's kind of work. Registered here so it
   is not lost.

**Still true and unfixed, verified at `35ec908`, and now superseded by phase 2:** the stale
three-value enumerations were in `docs/index.md`, `README.md` (3 places), `gen/build.py` (4),
`gen/__init__.py` and `gen/impurity.py` — see phase 2's note above for which of those were really
enumerations. The `prov-*` chips existed only in hand-written prose; `prov-judgement` now exists in
the CSS and the legend is guarded against the vocabulary. The marker precedent phase 2 needed was
`_with_bracket_verdicts` at `gen/build.py:152`, which injects `**no audit**` into a cell at `:174`.

## Working order

Each phase leaves all three gates green and is independently landable. Phases 0–2 are the machinery;
3 is corrections owed regardless; 4–5 are the content.

| # | Phase | Why this order |
| --- | --- | --- |
| 0 | Rename `envelopes.provenance` → `endpoint_sourcing` | 11 rows contradict `parameters.csv` today. Every later phase reads provenance, so the axis has to be separated before a fourth value lands in it. |
| 1 | Make the deliberate-blank refusal real | A fabricated value walks into `P-LIG-SEG-CONC` through 147 green tests **right now**. This closes a live hole and must precede the feature that widens it. |
| 2 | The vocabulary, `est_value`/`basis`/`falsifier`, the cell marker, the census page | The feature. Lands with no estimate resting on it yet, so it is reviewable on its own. |
| 3 | The corrections the audits forced | Owed whether or not the feature ships. Independent of 0–2. |
| 4 | Buffers | Needs 1 (the refusal) and 2 (the fields) in place. |
| 5 | Sizing, and the citable cleaning criteria | Needs 2. The only phase that moves a computed number. |

Stopping after 3 is a defensible landing: the machinery plus the corrections, with the estimates
explicitly not yet made. Stopping after 4 but before 5 publishes estimates with no sizing consequence
shown — do not stop there.

## Do not do these — they were tried and refuted

- **Do not add a phosphorylation/PNK buffer composition row.** SI Tables S1 and S2 are identical
  component-for-component including pH; it would duplicate `BUF-LIG`.
- **Do not treat the membrane cleaning bracket as two independent endpoints.** One industry
  convention across two vendors and three polymers. And **do not carry its "pH 10–11"** — that is a
  typo beside 0.1–0.5 N NaOH, which is pH 13.
- **Do not claim caustic degrades the product's residue.** The zero-2′-OH mechanism is supported; the
  degradation inference is a non sequitur, because cleaning validation sets analytically measured
  removal limits, not degradation.
- **Do not merge `single_point` into the blank-value guard.** `ENV-007/008/009` are `single_point`
  with `provenance=fact`; merging them forbids phase 5's own estimate. Key on `not_a_range` alone.
- **Do not scope the blank-value guard to the new provenance.** `P-LIG-SEG-CONC` is `assumption`, so a
  new-value-only guard closes nothing. Make it provenance-independent.
- **Do not fill `P-LIG-SEG-CONC`, `P-HBEL-DS` or `P-ENZ-CLEARANCE-LRV`.** The plan says why for each.
- **Do not add a new unit operation for phosphorylation.** `pfd.UNITS` is derived from
  `equipment.csv`, so a PFD cannot be opted out of, and a product stream would also force the
  `VIEW_W` fix plus an SVG re-baseline.
- **Do not let the new chip alone satisfy `_CITATION`.** Require a `P-` id with it.

## The discipline this slice was built under

Three audit rounds ran before a line was written, and each overturned something:

1. Four role reviewers, launched together so none saw the others: **all four rejected.**
2. A red team on the planner's own four findings: **two refuted, one's reasoning refuted, one
   confirmed by reproduction.**
3. A second-order audit that re-retrieved the documents behind round 2 and the research beat:
   **refuted the plan's headline research result, and found a published contradiction underneath a
   withdrawal the planner had already made.**

The transferable rule: **a finding is a claim with a name on it until someone re-retrieves the
document.** Two of this plan's best corrections came from re-reading a source the register had already
read — once for its percent sign while the sentence beside it answered an open question.

Practical consequences when you work:

- `curl` beats WebFetch on long documents; WebFetch silently truncates and has produced a confident
  false "no data" here. Espacenet, WIPO, ACS, ScienceDirect, NEB and Merck's own hosts 403.
- If a file you expect is missing, `find / -name '<file>'` before concluding anything. A scratchpad
  path changed mid-session once and the wrong conclusion drawn was that a whole research phase had
  been fabricated.
- Retrieval hazards already found, in the plan's own section: a mis-filed FDA media ID, a wrong PIC/S
  docview ID, and U+2019-vs-prime in the Almac SI that breaks a string match.

## Conventions that silently corrupt a diff

- **Gates, judged by exit code, never piped through `tail`**, with generated pages deleted first
  because CI runs pytest **before** the build:
  `git clean -fXd docs ; python -m pytest gen -q ; python -m gen.build ; mkdocs build --strict`
- Baseline **147 tests**. Every new guard mutation-tested against a failing case in
  `gen/test_mutations.py` — tmp-copy `data/`, monkeypatch `gen.dataio.DATA_DIR`, anchor on a **row id**
  never a field value, assert the guard **raises**. Start with the red team's reproduction, which must
  now fail.
- A column addition touches the header **and every row** together, or the field-count guard fires on
  all of them. `parameters.csv` is CRLF and appending a field turns each data line into exactly
  `<old line>,` — verified byte-wise. `buffers.csv` is CRLF and writes **no `""` for empties**, unlike
  `streams.csv`, which always quotes `carries` and `notes`. `equipment.csv` always quotes `turndown`.
  Keep every row single-line or the CR/LF count guard trips.
- Vocabularies are module constants in `gen/dataio.py` with a runtime `raise` in the consumer **and** a
  guard that **imports the constant** rather than re-listing it. Four guards currently re-list
  provenance inline; that is what phase 0 fixes.
- Adding a CSV column needs **no** register-spec edit — `cols=None` and `md_table` derives columns
  from the header.
- Every generated page must be in the `mkdocs.yml` nav **and** linked from a hand-written page; both
  are guarded. A root-level `.md` like this file is outside both, verified.
- `mkdocs` prints a red "Warning from the Material for MkDocs team" line and still exits 0. Not a
  failure.
- The eight committed SVGs must be byte-unchanged unless stream data deliberately changed.
- `balance._require` raises on a blank, so a blank `value` is only safe for parameters no balance path
  reads — check `used_by`, matched by bare substring over the whole text of `gen/balance.py`.
- Next free ids by `max`, not assumption; `questions` is at **Q-070**. Buffer ids are semantic
  `BUF-<WORD>` with no format guard. **Renaming `BUF-LIG` breaks three `infoneeds` rows.**

## Definition of done

All three gates green with generated pages deleted first; test count above 147; every new guard
mutation-proved; no `data/*.csv` line-ending flip; eight SVGs byte-unchanged.

Then a report stating what was verified **by execution** versus reasoned about, and for every value
carried under the new provenance: its basis, its falsifier, the question it did **not** close, and why
a range was or was not given.
