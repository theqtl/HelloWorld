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
| 2 — the vocabulary, the fields, the visibility | **done** | `25c831b` |
| 3 — the corrections the audits forced | **done** | `55c75d2` |
| 4 — buffers | **done** | (this commit) |
| 5 — sizing, and the citable cleaning criteria | **next** | — |

**Baseline is now 215 tests, not 147.** Phase 0 took it to 155, phase 1 to 163, phase 2 to 202, phase 3 to 205,
phase 4 to 215.

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

### Phase 3 — verified state, 2026-09-27

**Baseline is 202 tests** (phase 2 took it from 163). Next free question id is **Q-071**; there are
52 question rows.

**`Q-059` and `Q-064` already exist and already carry long notes. EDIT them, do not raise new
questions for the same ground.**

**Do not conflate two different contradictions.** `Q-059`'s notes already record one - inside
`SRC-CN119265174`, where Example 7 heat-kills an immobilised enzyme at 80 °C/5 min, Example 12 at
85 °C/15 min, and Examples 3, 5, 6 and 8 remove it centrifugally at 3000 rpm for 2 min with no
thermal step at all. That is about **enzyme inactivation**. The contradiction phase 3 must register
is a **different one**: Almac's paper says phosphorylation at **5 mM** while its own SI says **2 mM**
for the same telescoped experiment (same one-pot phosphorylation of 1.2/1.3, same ligation of 1.4
then 1.1, same Figure S5). Keep them apart or the register will read as if one document had both
problems.

**The Almac solids rejection is genuinely unregistered - checked.** Every existing `centrifug*`
mention in `data/` (C-014, ENV-005, U02-CF, IMP-LIGASE, IN-017, P-LIG-INACT-T, Q-059) is about
`SRC-CN119265174` removing an **immobilised enzyme**. None is about Almac's *"heat treated at 75 °C
for 10 min (initial reactions) or 30 min (crude reactions), then centrifuged to pellet any
precipitated material and supernatant used for ligations"*, which sits **between kinase and
ligation** and is a solids-rejection step the flowsheet does not have. `docs/sources/ligation-evidence.md`
contains **zero** mentions of centrifugation.

**The evidence page is hand-written and IS swept for uncited numbers.**
`test_numeric_claims_in_prose_carry_a_citation` exempts only `/registers/`, `balance/results.md` and
`process/streams.md` - **not `docs/sources/`**. So every quantity added there (75 °C, 10 min, 30 min,
2 mM, 5 mM, 0.55 mM, 1.5 mM) needs a `SRC-`/`P-`/`Q-`/`EQ-`/`R-` token within ±3 lines. Phase 2 may
have widened `_CITATION`; check what it accepts now before assuming.

**The basis-crossing correction for `P-LIG-SEG-CONC` and `Q-064`, with the arithmetic:** the 1.5 mM
low endpoint is **per segment across three segments** (4.5 mM) **plus 0.55 mM of tri-template hub**,
so ≈**5.05 mM total oligonucleotide** - which makes the "6.7× void" ≈**2.0×** on a total basis. The
hub is a ~24 kDa covalently-supported construct with **no counterpart in our route**, and the
register has never mentioned it. The high end (*"blockmer concentrations as high as 10 mM"*) does not
state whether it is per blockmer or total, so the void's width is basis-dependent at both ends.

**A retrieval trap for any re-verification:** the Almac SI uses **U+2019**, not a prime (U+2032), so
a quote written with a prime will not string-match.

### Phase 3 — what landed, and the verified state phase 4 inherits

**205 tests** (phase 2 left it at 202). **Next free question id is Q-074**; there are **55 question
rows**, ids running Q-001..Q-073 with eighteen never issued. `gen/dataio.py`'s `QUESTION_STATUS`
comment carries that arithmetic and was updated with it — keep them in step.

**Three questions raised, and none of them is ground phase 4 should re-raise.** `Q-071` the 2 mM vs
5 mM published contradiction; `Q-072` the phosphorylation-to-ligation solids rejection; `Q-073` the
retracted 89–96% block-purity band still live in nine sites. **`Q-059`, `Q-064`, `Q-016`,
`P-LIG-SEG-CONC`, `ENV-006` and `IN-005` were EDITED**, plus six source rows
(`SRC-ALMAC-2023`, `SRC-USPTO-10640812`, `SRC-PBCV1-2014`, `SRC-NEB-WO2023173098`,
`SRC-WO2025262452`, `SRC-DEVRIES-2018`), each carrying the verbatim quote behind its correction.

**The quench picture phase 4 must build its row on, because it is not what the plan says.** The plan
claims four registered sources name a chemical stop. **It is three, and only ONE is on a ligation:**

- **`SRC-PBCV1-2014`** — the only ligation. *"reactions halted at 15, 30, 60, 120, 240 and 480 min by
  addition of 25 µl stop solution"*, the solution being *"50 mM EDTA and 10 mM Tris–HCl at pH 7.5"*,
  1:1 by volume so 25 mM EDTA final, **no thermal step**. But 2.5 nM unmodified DNA probes on an mRNA
  splint — an analytical time course.
- **`SRC-NEB-WO2023173098`** — *"2x Quench Solution (20 mM EDTA, 2% SDS)"* is exact, and there is a
  second recipe, *"quenched by adding 2 µl of 30 mM EDTA and heating at 75 °C for 5 min"* — EDTA **and**
  heat, the only retrieved instance of the shape `Q-059` argues for. **Every quench in that patent is on
  a capping or poly(A) tailing reaction, never a ligation.**
- **`SRC-ALMAC-2023`** — methanol, `100% v/v` in the PNK screen and `1 volume` in the RNAL screen: **one
  recipe in two units on two different screens**, not two data points on quench strength. Both feed UPLC.
- **`SRC-WO2025262452` is NOT a fourth.** Re-retrieved: *"The reactions were quenched by heating to
  95 °C for 20 min to inactivate the enzyme. The inactivated reactions were subsequently diluted
  400-fold in 10 mM EDTA pH 7.0 and analyzed via HPLC."* The document calls the **heat kill** the
  quench; the EDTA is HPLC sample prep on an already-dead reaction. The register was right and the
  proposed correction was wrong.

So a quench row is supportable **only with the analytical-scale caveat the plan already demands**, and
nothing retrieved terminates a modified-siRNA ligation at process scale. `Q-060` stays blank.

**The Almac numbers, re-verified character by character with two independent PDF extractors** (SI
integrity checked against the md5 figshare publishes):

- `5 mM` appears **once** in the main text and **never** in the SI; `2 mM` **three times** in the SI and
  never in the main text, and all three SI hits are the ATP row of Tables S1/S2, not the telescoping
  sentence. The two figures never co-occur and no erratum reconciles them.
- **Exactly ONE `%` in the whole main text**, in `100% v/v methanol` — the `P-CONC-LIG` / `Q-016` count
  re-confirmed. (The SI has three, all in the Table S3 gradient.)
- **Tables S1 and S2 are identical on every buffer component including pH** — 1 mM DTT, 2 mM ATP,
  100 mM KCl, 10 mM MgCl2, 50 mM Tris-HCl pH 7.5 — and differ only in enzyme identity and blockmer
  concentration (0.1 vs 0.5 mM). Phase 4's "do not add a PNK composition row" still holds, now verified
  rather than reported.
- **TWO retrieval hazards, not one.** The main text writes `5′OH` with a **prime (U+2032)** and no
  hyphen; the SI writes `5’-OH` with a **right single quotation mark (U+2019)** and a hyphen. The plan
  warns about the SI only. Also `SRC-PBCV1-2014` prints `Tris–HCl` with an **en dash**, and **PubMed
  Central served a reCAPTCHA page to every route tried** — that paper came through the Europe PMC REST
  service instead.

**The 6.7× void is now ≈2× to ≈6×, basis unknown — do not re-simplify it.** `SRC-USPTO-10640812`
Example 13 charges 1.5 mM of **each of three** segments **plus** *"750 μl 0.00387M Hub (Template)
(0.55 mM final)"*, so 5.05 mM total oligonucleotide. The hub is *"approximately 24 kDa"*, covalently
attached, and has **no counterpart in our route** — proved rather than assumed: the word "template"
occurs **exactly once** in Almac's whole main text and it is the product's own overhang. Almac's high
end states no basis at all. The plan's "~2.0× on a total basis" is one of four readings.

**The `_QUANTITY` percentage hole phase 2 deferred here is FIXED**, with `%` moved onto its own branch
outside the trailing `\b`. Three mutation cases guard it, and one was **proved to fail against the old
regex** before being kept. The seven lines it newly caught were across **three** pages, not four as
phase 2 recorded. One of them was a real defect: `docs/findings/filtration.md` cubed an 89–96% block
purity that `Q-011` retracted on 2026-09-25, publishing a ~70–88% internal-limited purity floor where
`P-BLOCK-PUR` supports **~82–87%**. Fixed there; the other nine sites are `Q-073` and are **deliberately
not swept**, because 89–96% is also a still-valid first-principles band (`ENV-002`) and each site has to
be read to decide which of the two it meant.

**Deliberately NOT done in phase 3**, so phase 4 does not assume otherwise: no unit operation for the
solids rejection (`pfd.UNITS` derives from `equipment.csv`, so it would force an SVG re-baseline on a
96-well-plate observation); no quench row (phase 4 owns it); no value written for `P-LIG-SEG-CONC`; no
sweep of `Q-073`'s nine sites.

### Phase 4 — verified state, 2026-09-27

**Baseline 205 tests.** Phase 4 is the FIRST phase that writes an actual estimate: `judgement` is in
the vocabulary and **zero rows anywhere use it**. Phases 0–3 built the machinery, the guards and the
corrections; nothing has exercised them yet.

**Recommendation before starting: open a PR for phases 0–3 first.** Eight commits and well over a
thousand lines sit unreviewed on the branch, and phases 0–3 are exactly the reviewable unit the plan
designed — the machinery plus the corrections, with **no estimate resting on any of it**. Phase 4 is
the first phase whose content is a judgement call rather than a mechanical invariant, so if review
changes the machinery, phase 4's data would have to be rewritten. Land 0–3, then start 4 on a clean
base.

**The guards phase 4 must satisfy** (`estimate_offenders()` in `gen/envelope.py:161`, guarded by
`test_an_educated_estimate_carries_its_obligations` at `test_balance.py:2382`):

1. The number goes in **`est_value`** and the row's own quantity columns stay **blank**. For
   `buffers` those columns are **`components` and `ph`** — `ESTIMATE_REGISTERS` is
   `{"parameters": ("value",), "buffers": ("components", "ph"), "scenarios": (...)}`. So an
   estimated CIP recipe does **not** go in `components`. The converse is guarded too: `est_value`
   on a non-estimate row fails.
2. **`basis` must resolve every `SRC-`/`P-`/`EQ-`/`Q-` token**, no cited source may be graded
   `abstract-only`, `record-only` or `not-retrieved`, and **at least one `Q-` token is required** —
   a row naming no open question is claiming to have settled something.
3. **The cited question must be `open`.** A `partially_resolved` or `resolved` one is a contradiction.
4. `judgement` is **refused outside `ESTIMATE_REGISTERS`**.

Four more guards exist and must stay green: `test_no_numeric_reader_consumes_an_estimate`,
`test_an_estimate_is_marked_in_the_cell_where_the_number_is_read`,
`test_the_marker_transform_is_wired_into_every_estimate_register`,
`test_every_estimate_reaches_the_census`, and
`test_an_estimated_quantity_in_prose_names_the_parameter_it_estimates`.

**Phase 4 starts with source registration, not with buffer rows.** Of 106 source rows, the only
cleaning-adjacent one is `SRC-MILLIPORE-TFF`, and it is registered for **TFF yield loss**, not
cleaning. Nothing is registered for Cytiva (two handbooks, exact doc codes `CY28744-18Jul22-HB` and
`CY14739-24Feb21-HB`), the Millipore *Pellicon 3 IUG* (`AN1065EN00 Rev C, 01/2009`, reachable only
via a third-party mirror so its access grade must be **downgraded off `full-text-read`**),
Wiencek/ISPE 2006, PIC/S PI 006-3 (**docview 3447**, not 3436), WHO TRS 1019 Annex 3, Alfa Laval, or
the brewery CIP paper. Since `basis` must resolve its `SRC-` tokens and they must be READ grades,
**no estimate can be written until its sources exist**.

**The plan's phase-4 content, with the audit corrections already applied** — do not re-derive these:
`BUF-MEMBRANE-CLEAN` is `one_source_both_ends` at convention level, **not** two independent
endpoints; drop its **pH 10–11** figure as a typo beside 0.1–0.5 N NaOH (which is pH 13); carry the
**100-hour cumulative exposure budget** and Millipore's own *"better membrane life has been observed
at lower concentrations"*. `BUF-CIP` is the genuine `judgement` case. A **quench** row is now
supportable from four documents, with the caveat that every chemical stop is at an **analytical
sampling point**, not process scale. **Do not** add a PNK composition row (it would duplicate
`BUF-LIG`) or IMAC buffers (conditional on `Q-050`). Two CIP rows minimum — TFF chemistry differs
from every other unit operation.

**The unit-op → solution guard has a prerequisite.** Three vocabularies resolve to each other
nowhere: `equip_id`, free-text `equipment.unit_op`, and `RISK_UNIT_OPS` where `Ligation` ≠
`Enzymatic ligation` and `Utilities` is absent entirely. Phase 0 relocated that constant but did not
reconcile it. Fix the key first, then guard on `equip_id`.

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
- Baseline **147 tests** as the slice opened; **205** after phase 3. Every new guard mutation-tested
  against a failing case in
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

### Phase 4 — what landed, and the verified state phase 5 inherits

**215 tests** (phase 3 left it at 205). **Next free question id is Q-076** (Q-074 and Q-075 raised);
**next free envelope id is ENV-019** — ENV-017 already existed, so the row phase 4 added is
**ENV-018**, and the "next free ids by `max`, not assumption" rule caught the collision on the first
append. Eight SVGs byte-unchanged; no line-ending flip; `risks.csv` changed in exactly one column
across nineteen rows and nothing else.

**Three rows now carry `judgement` — the machinery is exercised.** `BUF-CIP` (the caustic recipe),
`BUF-DF` and `BUF-FINAL` (the two compositions that were `assumption` + "TBD"). `estimate_offenders()`
ran against real rows for the first time, and two of the nine phase-2 mutation cases now have live
counterparts: `test_mutation_the_first_real_estimate_may_not_write_its_composition` and
`test_mutation_closing_the_question_under_a_live_estimate_is_caught`, the second of which mutates the
QUESTION rather than the estimate — the cross-register direction nothing covered.

**Six sources registered, all read, all re-retrieved for this phase:** `SRC-MILLIPORE-PELLICON3`,
`SRC-CYTIVA-HF`, `SRC-CYTIVA-CFF`, `SRC-ISPE-WIENCEK-2006`, `SRC-ATWELL-2017`, `SRC-EGLI-2023`.
**Alfa Laval and the PIC/S and WHO cleaning documents were deliberately NOT registered:** the first
is not needed by any phase-4 row, and the other two are phase 5's content (the carryover criteria).

**The unit-operation prerequisite: the plan's premise was wrong and the fix inverted.** The plan says
three vocabularies resolve to each other nowhere. Measured, **four** registers carry a unit-operation
reference, and two of them **already held `equip_id`**: `instruments.unit_op` is `U00-BUF`…`U06-CIP`,
and so are `streams.from_unit`/`to_unit` (plus the boundary nodes `SUPPLY`, `WASTE`, `DS-STORE`). So
`equip_id` was already the key for half the data layer and `risks.unit_op` was the outlier — which
means relabelling `risks` to the equipment LABEL, the obvious reading of "fix the key", would have
turned three spellings into two and left the key unreachable. `risks.unit_op` now holds `equip_id`;
`risk_unit_ops()` is **derived** from `equipment.csv` (so `Utilities` cannot go missing again) and is
a function, not an import-time frozenset, because the mutation harness monkeypatches `DATA_DIR`.
`equipment.unit_op` stays a display label on purpose. **Registered, not fixed:** `gen/pfd.py`'s
`render_svg(unit_op)` takes an `equip_id` under a parameter name that says otherwise — a large part of
why three vocabularies looked like one.

**`solution_offenders()` is the unit-op → solution guard**, in `gen/envelope.py`, called from
`validate()` so the build raises too. Forward: every `buffers.equip_ref` resolves to an `equip_id`,
and a blank one fails. Reverse, and this is the direction that found something: **five of the seven
unit operations had no registered solution at all** before this phase, which the two CIP rows close.
Four mutation cases, including one that renames an `equip_id` to prove the vocabulary follows
`equipment.csv` rather than a literal.

**What phase 4 refuted in its own plan** — all six corrections are written into the source rows
themselves, with the verbatim quote behind each, so they cannot be lost:

1. **The membrane non-differentiation is in the wrong table in the plan.** Millipore's *cleaning*
   chart gives Biomax a NaOH/**NaOCl** blend, not NaOH alone — so it does NOT show one bracket for
   both membranes. The one-row non-differentiation is in the **sanitization, depyrogenation and
   storage** tables, each of which covers "Ultracel / Biomax" with a single `NaOH 0.1 N` row while
   every acid and solvent agent in the same document differs between them. That is *stronger*
   evidence, and it needs no polymer names — which matters, because **the guide names no polymer for
   either membrane**, so "regenerated cellulose" and "polyethersulfone" are attributions from
   somewhere else. Cytiva's hollow-fibre handbook does name its own: polysulfone.
2. **The brewery study did not measure hot caustic.** `SRC-ATWELL-2017` ran every one of its 90 runs
   "under ambient temperature conditions consistent with industrial operation" and measured a
   concentration threshold: NaOH must be "at least 1% w/v" and above that "there is no additional
   cleaning benefit". The lower-temperature claim belongs to **Goode et al (2010)**, which Atwell
   only reports and which was **not retrieved** — so no temperature conclusion may rest on it. The
   paper is a better counterweight than the plan described, not a worse one, and it adds a third
   independent, *measured* pH ≈ 13 for caustic solutions.
3. **The bracket does not recur across "two vendors" without exception.** Millipore's cleaning chart
   and Cytiva's CFF handbook print the same four numbers (N versus M, cleaning versus
   sanitization/depyrogenation, pH 10–11 versus pH 13). `SRC-CYTIVA-HF` — third document, third
   polymer — reproduces **neither end**, circulating a 0.5 N point at 50 °C for an hour. The
   convention reading survives and is *better* argued from the migration between unit operations
   than from a vendor count.
4. **The Millipore copy is not "frozen 2016".** It is **Rev C, 01/2009**, on a reseller mirror
   uploaded 2015/03, and Merck's own host publishes a **newer Rev 7, 04/2021** that could not be
   transferred (three attempts, empty reply; the manuals.plus mirror 403s). So the currency problem
   is sharper than the plan states: a 12-year-old revision, with a current one known to exist.
5. **The access grade was downgraded, for the honest reason.** `partial-text-read`, because the
   cleaning, sanitization, depyrogenation and storage sections were read in full while the
   installation chapters were skimmed — and the mirror-and-currency problem is recorded in
   `reachability`, where it belongs. Grading a full read as partial to *signal* a currency doubt
   would put two questions in one column, which is the polysemy phase 0 exists to have removed.
6. **The ISPE 1% is not a numbered item in the Assumptions list.** The list is items 1–5; the
   sentence "Assume a nominal chemical concentration of 1% by volume for caustic and acid washes"
   follows the arithmetic as an inline sixth assumption. Its only job is to turn 720,000 L of water
   into 7,200 L of chemical.

**And one thing the plan asserted that is now quoted.** "Two CIP rows minimum — TFF chemistry differs
from every other unit operation" is `SRC-ISPE-WIENCEK-2006`, verbatim: *"TFF membranes usually require
cleaning chemistries and temperatures that are different than all other unit operations. Establishing
specifications for each unit operation may minimize the need to test multiple CIP chemistries at the
production scale."*

**The quench row, and what it does not claim.** `BUF-QUENCH` is `fact`, carrying the **one** chemical
stop on a **ligation** anywhere in the register — `SRC-PBCV1-2014`'s 50 mM EDTA / 10 mM Tris–HCl
pH 7.5 stop solution, re-retrieved via Europe PMC and confirmed 1:1 into a **25 µl** reaction at
**2.5 nM** probes, feeding qPCR. Its `use` says in terms that it is analytical sampling and not a
unit operation. Re-retrieving `SRC-NEB-WO2023173098` found a **third** quench recipe phase 3 did not
record ("10 µL 50 mM EDTA with 0.7 % Tween-20"), and it is on a poly(A) tailing reaction like the
other two — so the count is three recipes in that patent, none on a ligation. `Q-060` stays blank and
`Q-059` was edited to say that the analytical quench being registered is not an answer to it.

**Carried forward to phase 5, and still not done.** The plan's "Also register, do not fix here" items
are **not registered yet**: `gen/flowsheet.py` `VIEW_W = 1160` with 30 px of slack and no test
catching a clipped box, and the retro-fit audit of the 35 `assumption` rows. The line-ending guard's
docstring is also still wrong, and the real figures are now **measured**: **14 CRLF and 2 LF across
16 files**, not "ten of the twelve" — left alone because the plan says register rather than fix, and
recorded here with the numbers so the fix does not need re-measuring. Also still not done: the
structured `buffer_ref` column phase 1 deferred as a rendering feature.
