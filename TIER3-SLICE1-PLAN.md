# Tier-3 slice 1 — implementation plan (approved, not yet applied)

**Created 2026-09-21.** This file is deliberately outside `docs/` so it is not a site page and
cannot affect the strict build — the same reason `RESEARCH-QUEUE.md` sits here.

**Nothing in this plan has been applied.** No `data/*.csv`, no `gen/` module and no page under
`docs/` has been changed for it. The repo is at Tier 2 (`ef256a8`, 51 tests) and this file is the
only addition.

It was written and then audited three times; 24 findings were raised, 1 withdrawn, 23 standing, and
all are folded into the body below rather than listed as history. Three of those findings were
regressions introduced by the revisions themselves, so prefer this document over re-deriving its
reasoning. The **Verified facts** section at the end records what has already been checked against
the repo — do not re-derive those, and note the single item flagged unverified.

---


## Context

Tier 2 merged as `ef256a8` and is deployed; the suite is 51 tests. Registers, the balance, the impurity
overlay and the flowsheet all generate from `data/*.csv`.

One part of the argument is still held only as prose. `docs/techtransfer/index.md:52-60` ends with
"Control strategy anchor points (from the findings)" — three bullets that *are* the CPP→CQA argument:
purity is set at the block stage and the ligation reaction rather than downstream; duplex integrity is
bounded first by the moisture-shifted glass transition and then, more loosely, by dryer outlet
temperature below Tm; enzyme clearance depends on enzyme form. Prose cannot be checked, so nothing in
the repo can catch a control claimed for a quantity nobody can measure — and the repo contains exactly
that case. Q-042's notes say verbatim that in-line UV saturates on a 21-mer at process concentration
and that the deployed answer "is variable-pathlength slope spectroscopy, which is **at-line, not
in-line**." Meanwhile `docs/techtransfer/index.md:25-26` still advertises "in-line UV/conductivity on
UF/DF" as PAT.

The same page lists "**No side-by-side comparison** of premises, equipment, instruments, materials,
procedures and methods" as a WHO TRS 1044 gap (line 48), and **there is no instrument data anywhere in
the repo** — the only two matches for "instrument" are a figurative note in `sources.csv` and a comment
at `gen/test_balance.py:524`. A control strategy with no instrument to enforce it is half a document,
so both land together.

Outcome: a CPP→CQA matrix and an instrument register, generated and guarded, with every gap registered
rather than filled.

## Decisions taken

1. Soluble-enzyme clearance = thermal/pH denaturation, then depth filtration.
2. **Enzyme identity is undecided** → a registered question with blank-valued dependents. This makes
   decision 1 *conditional*, because denature-then-filter presumes a soluble enzyme while the register
   currently presumes an immobilised one. Clearance is therefore modelled as **two branches, neither
   asserted as chosen**.
3. Full instrument register, including monitoring-only instrumentation.
4. Keep the three prose bullets as narrative, with a pointer to the generated matrix.

## Discipline

Edit `data/*.csv` and `gen/`, never generated pages. Every value flagged fact / inference / assumption.
Never invent, round or extrapolate; a gap stays blank and is registered. Carry scale and system with
every transferred number. **Never weaken a test**; never tune a value so a test passes (`P-DRYGAS-RATIO`
was deleted for that). Prefer invariants that hold by construction. **Do not resolve Q-002.** Do not
relitigate enzymatic ligation, filtration-led purification, evaporation, spray drying, low-bioburden
microbial control; no lyophilisation.

---

## A. New parameters

None of these exist today and §B's rows need them. Convention: **carry the cited value only where the
quantity actually transfers; otherwise leave it blank and register it.** All `assumption`, all
`used_by=docs`, all with a `Q-` in `notes`. A `BAND:` note requires `range_low`+`range_high`; a blank
point value alongside a band is an established pattern (`P-EVAP-MIN-WETRATE`). The precedent for a
deliberately blank, registered-gap parameter is **`P-HBEL-DS`** — blank value, `used_by=docs`, tied to
Q-047, and protected by `test_hbel_stays_a_registered_gap` so nobody later fills it in. Model
`P-LIG-ENZ-LOAD` and `P-ENZ-CLEARANCE-LRV` on it, and consider an equivalent guard for each.

| new id | value | basis |
|---|---|---|
| `P-LIG-ATP` | 2 mM | `SRC-ALMAC-2023` SI, 1 L, cell-free extract; note the Q-040 tension |
| `P-LIG-T` | 25 °C | same source and caveat; Q-050 may move the optimum |
| `P-LIG-TIME` | blank, BAND 1–20 h | cited band; Q-050 |
| `P-LIG-ENZ-LOAD` | **blank** | 1 mg/mL is a *cell-free-extract* loading (R-017); form undecided (Q-050) |
| `P-DS-TM` | blank, BAND 58.1–64.1 °C | `SRC-MALEK-2019`; do not extrapolate across all 21 positions (Q-030) |
| `P-DS-TG` | blank, BAND 38–53 °C | `SRC-KEIL-2021`, trehalose, bench — their matrix, not ours (Q-039) |
| `P-DS-RESID-MOISTURE` | blank, BAND 3.8–4.6 %w/w | same source and caveat (Q-039) |
| `P-ENZ-CLEARANCE-LRV` | **blank** | no ppm or log figure exists publicly (Q-032) |

Unit style follows the repo (`degC`, `percent_w_w`, `dimensionless`); `mM` and `h` are new.

## B. `data/controls.csv` and the generated matrix

Columns: `control_id, cpp, cqa, unit_op, param_ref, equation_ref, risk_ref, instrument_ref,
control_type, acceptance_basis, gap_ref, provenance, source_key, notes`.

`control_type` is a controlled vocabulary in `gen/controls.py`, mirroring `CLEARANCE_MODELS`
(`gen/impurity.py:24`):

- `set_at_supply` — fixed by incoming block spec, not adjustable in-facility
- `in_reaction` — adjusted at the reaction
- `thermal_limit` — an upper bound on temperature
- `matrix` — set by the final formulation
- `downstream_removal` — achieved by a separation step
- `not_measurable` — **no instrument can measure it at process conditions**; renders as a registered
  gap. The Q-042 case, and the row type that makes generating the matrix worth doing.
- `gap` — no control defined yet

Rows, from the three anchor bullets: block purity (`set_at_supply`, `P-BLOCK-PUR`, `EQ-PURITY`, Q-011);
ligation conversion (`in_reaction`, `P-LIG-CONV`, `EQ-LIG`, Q-010); ATP, temperature and time
(`in_reaction`, the new parameters, Q-040/Q-050); enzyme loading and form (`in_reaction`,
`P-LIG-ENZ-LOAD`, **R-017** — a cell-free extract makes the protein burden a whole proteome plus
endotoxin, not one ligase, so this control sizes the clearance problem in §D); AppN suppression
(`in_reaction`, gap → Q-040, R-010);
Tg at achieved moisture (`thermal_limit`, `P-DS-TG` + `P-DS-RESID-MOISTURE`, `EQ-TG`, Q-039) as the
**binding** limit; dryer outlet below Tm (`thermal_limit`, `P-DRY-T-OUT` / `P-DS-TM`, Q-030) as the
**looser** one; final matrix (`matrix`, `P-EXCIPIENT-RATIO`, Q-021, R-005); the two enzyme branches
(§D); in-line concentration (`not_measurable`, gap → Q-042).

**Three generated pages, on the streams precedent** — `gen_registers()` emits `registers/streams.md`
while `gen_streams_on_process()` emits a curated `process/streams.md`:

- `docs/registers/controls.md` and `docs/registers/instruments.md` — raw tables, one new spec tuple
  each in `gen_registers()` (`gen/build.py:32`). Under `docs/registers/` they inherit the filter and
  sort JS and are exempt from the prose-citation lint.
- `docs/process/controls.md` — the CPP→CQA matrix grouped by CQA, from a new `gen/controls.py` wired
  into `gen/build.py` `main()`. Not exempt from the lint, but every row carries a `P-`/`Q-`/`R-`/`EQ-`
  token on its own line, so it passes by construction — **provided the renderer emits the id columns**,
  which §E guards. Intro prose must carry its own citations.

Reuse `md_table` (`gen/tables.py`) and `load_rows` / `param_value` (`gen/dataio.py`). Follow
`gen/impurity.py`: lenient on blanks (`param_value` → `None`, render `gap (...)`), strict on vocabulary
(it raises at `:44-47`).

Add all three pages to **`.gitignore`**, which lists every generated Markdown file explicitly. Add nav
entries — two under `Registers:`, one under `Process:` — in `mkdocs.yml` (`strict: true`).

## C. `data/instruments.csv` — full register

Columns: `instrument_id, tag, unit_op, stream_ref, measured_variable, measurement_mode, purpose,
provenance, source_key, gap_ref, notes`. ISA-style tags (TI/TIC/PI/FI/AI/QI/MI/LI/DPI) keyed to unit
ops and, where applicable, to `stream_id`; `data/streams.csv` already carries the topology.

**`measurement_mode` is required**, vocabulary `{in_line, on_line, at_line, off_line}`. Without it the
slice's centrepiece cannot be expressed as data, because the `not_measurable` control row rests
entirely on the in-line/at-line distinction Q-042 draws.

**No `control_loop` column.** `controls.instrument_ref` is the single authoritative link; carrying the
relation on both sides lets them disagree with nothing to detect it. A monitoring-only instrument is
simply one that no control references.

Control-enforcing rows: dryer inlet/outlet temperature and product residual moisture (U05-SD);
evaporator boiling temperature and vacuum (U04-EVAP); UF/DF TMP, conductivity and UV (U03-UFDF);
reaction temperature and ATP (U01-LIG). Monitoring-only rows: vessel levels, differential pressure
across depth and 0.2 µm filters, dryer gas flows, CIP conductivity returns, bioburden and endotoxin
sample points. Expect 35–50 rows, each `assumption` unless a source supports it.

The UF/DF UV row is the one that must be right: `measured_variable=uv_absorbance`,
`measurement_mode=at_line`, `gap_ref=Q-042`.

## D. The enzyme fork, modelled as a fork

- **New `Q-050`** — which ligase, and in which form. Owner `process`. Record both candidates with their
  evidence and their gap: the T4-mutant CC31 lineage (`SRC-USPTO-10640812` — relative peak area only,
  and it drags Q-040 with it, because wild-type T4 "gave exclusively AppDNA on RNA-splinted substrate"
  per `SRC-PBCV1-2014`, and for siRNA the splint *is* the complementary product strand) and PBCV-1
  (`SRC-PBCV1-2014` — DNA-RNA hybrid helices, not fully modified siRNA).
- **Two `downstream_removal` rows**, both with blank acceptance and a live `gap_ref`. The *soluble*
  branch: denature (85 °C/15 min, `SRC-CN119265174`) then depth filtration — provenance **inference**,
  because that cited route follows denaturation with an ion column, not filtration alone, which is why
  R-002's note says it "does not by itself deliver a chromatography-free train." The *immobilised*
  branch: the existing path, Q-032 and R-002.
- **Reframe `Q-032`**, whose text presupposes the answer ("…with immobilised enzyme"). Make it
  form-agnostic and cross-reference Q-050.
- **New `R-021`** — an 85 °C denature hold sits above any plausible duplex Tm, and Tm is unknown
  (Q-030), so the soluble branch trades an enzyme-clearance gap for a product-integrity risk that is
  registered nowhere. `category=product`, `unit_op=Filtration`.
- **Update `U02-CF`** in `data/equipment.csv`: its `sizing_basis` and `notes` currently assume the
  immobilised route ("or centrifuge if immobilised enzyme"). Make both branch-aware. It is CRLF —
  preserve that.
- **The soluble branch implies equipment that does not exist.** An 85 °C hold needs a heated vessel or
  exchanger; `U02-CF`'s `moc_candidate` is "Single-use depth media" and cannot denature anything.
  Either add the denature unit to `data/equipment.csv` or register its absence against Q-050. Do not
  route the control row through `U02-CF` as though the filter performed the thermal step.

## E. Guards

- **Controlled vocabularies** — `control_type`, `measured_variable`, `measurement_mode`. Copy
  `test_impurity_clearance_models_are_a_controlled_vocabulary` (`:875`): constant in the generator, test
  imports it.
- **Referential integrity, the guard that earns this slice.** `risk_ref` resolves to a real `risk_id`;
  `equation_ref` to a heading parsed from `docs/equations/index.md`; `instrument_ref` to a real
  `instrument_id`; `stream_ref` to a real `stream_id`; `unit_op` to an `equip_id` or a member of
  `flowsheet.SENTINELS` (`gen/flowsheet.py:20`).
- **`param_ref` is conditional, not "resolves if present".** A row whose `control_type` is not
  `gap`/`not_measurable` **must** carry a `param_ref` and it must resolve. A `not_measurable` row
  **must** leave it blank — you cannot name the parameter for a quantity nobody can measure — and must
  carry a resolving `gap_ref`. "Every non-blank `param_ref` resolves" is too weak: it permits a control
  row with no parameter at all, the exact defect this slice exists to expose.
- **No `in_line` claim for concentration or UV.** Any instrument with `measured_variable ∈
  {uv_absorbance, concentration}` and `measurement_mode = in_line` fails unless a source establishes it.
  Q-042 encoded as a guard rather than a note.
- **Gaps render as registered.** Copy `test_impurity_gaps_carry_a_registered_reference` (`:891`):
  `gap` and `not_measurable` rows match `[QR]-\d{3}` *and* that reference appears in the rendered page.
- **The matrix page renders its id columns.** Assert every row's id token appears in
  `gen/controls.render()` output — otherwise the "passes the lint by construction" claim quietly
  degrades into a coincidence.
- **Instrument coverage.** `in_reaction`, `thermal_limit` and `downstream_removal` rows must carry a
  non-blank `instrument_ref`. Blank is permitted only for `set_at_supply` (a supplier spec, no
  in-facility instrument), `matrix`, `gap` and `not_measurable`.
- **Determinism** — `controls.render() == controls.render()`, per
  `test_impurity_overlay_is_deterministic_and_scenario_free`.
- **Extend the cross-CSV guards** — add `controls` and `instruments` to `test_data_files_present`
  (`:82`), `test_all_source_keys_resolve` (`:7`), `test_every_question_reference_exists_in_every_csv`
  (`:173`) and `test_md_table_emits_markdown_only` (`:731`, currently a hardcoded four-CSV list — the
  new files carry the repo's longest free-text `notes`, where `|` escaping matters most).
- **New: `risks.csv` `unit_op`/`category` vocabulary guard.** Neither is enforced today, so R-021 could
  ship an invalid value silently. Strengthening, therefore allowed.

## F. Prose

Keep the three bullets and add a pointer to the generated matrix — the move already used for the
generated results table (`docs/balance/index.md:99,113`). But **bullet 3 is falsified** by decisions 1
and 2: "Enzyme clearance depends on **immobilisation** performance" must become the open fork.
Reconcile `docs/techtransfer/index.md:25-26`, which still lists in-line UV on UF/DF as PAT against
Q-042. Update the WHO TRS 1044 list: the instrument half of "no side-by-side comparison" becomes partly
addressable; the other five gaps are untouched.

`test_numeric_claims_in_prose_carry_a_citation` (`:492`) needs a citation token within ±3 lines of any
number carrying `% percent g/L mg/mL kDa Da kJ/kg EU/mL CFU LMH mM °C kWh MJ` (`:478`). **`mM` and
`mg/mL` matter here** — ATP is 2 mM, the enzyme loading 1 mg/mL.

Also update **`README.md`**, which enumerates what "lives once in `data/*.csv`" and lists the generated
pages; two new registers and a matrix page make both stale. Consider a line in
`docs/adr/0001-information-architecture.md`.

## Sequence

**Write each guard from its invariant before or alongside its data.** Guards written last get shaped to
fit whatever rows already exist — the mirror of the `P-DRYGAS-RATIO` failure, where a value was tuned
until a test passed. Here the risk is a test relaxed until the rows pass.

1. **A** — new parameters. Existing guards on provenance, Q-refs and bands make this verifiable on arrival.
2. **C** — vocabulary guards first, then `data/instruments.csv`, the register spec, nav, `.gitignore`.
3. **B** — the conditional `param_ref` and referential-integrity guards first, then `data/controls.csv`,
   `gen/controls.py` and the pages.
4. **D** — Q-050, R-021, the Q-032 reframe, `U02-CF`, the denature-unit decision.
5. **F** — prose pointer, bullet 3, the PAT reconciliation, WHO TRS list, README.
6. The cross-CSV and `risks.csv` guards, which can only be written once the files exist.

## Verification

After each step: `python -m pytest gen -q`, `python -m gen.build`, `mkdocs build --strict` — judge by
**exit code**, not by output. Then:

- Break one `param_ref` and confirm the guard fails; restore. Same for an `equation_ref` and an
  `instrument_ref`.
- **Prove the conditional with its negative cases, which are the novel part**: a non-gap row with a
  *blank* `param_ref` must fail, and a `not_measurable` row with a *populated* one must fail. A green
  suite on well-formed data proves neither.
- Set the UF/DF UV row to `in_line` and confirm the Q-042 guard fails; restore to `at_line`.
- Confirm the Q-042 control row renders as a registered gap, not as a control.
- Confirm both enzyme branches render with blank acceptance and a live gap reference, and that neither
  reads as the chosen route.
- Confirm no new parameter name appears in `gen/balance.py`.
- `tr -cd '\r' < data/controls.csv | wc -c` equals its line count (CRLF, the majority convention); same
  for `instruments.csv`; `equipment.csv` still CR=8.
- `git status` — the three new generated pages must be ignored, not staged.

**Report what was verified by execution versus only reasoned about.** Tier 2's first pass was green on
all three gates and still unsound.

## Say this in the PR

Most acceptance bases land as `assumption` tied to existing questions, because the data behind Q-010,
Q-011, Q-030, Q-039 and now Q-050 does not exist. The deliverable is a **correct, checkable structure
with flagged placeholders**, not a control strategy a CMO could execute. State it plainly rather than
letting a green build imply otherwise.

## Not doing

- **The PFD** — it needs these tags to exist first or it gets drawn twice. Natural next slice, and cheap:
  `gen/flowsheet.py` already does longest-path layout, cycle detection and role-agnostic edge routing.
- **The facility capital concept** — `docs/facility/index.md` scopes it as a function of Q-002.
- **Choosing the ligase**, or filling any gap that needs data which does not exist.

## Branch and landing

PR #4 is merged, so that branch cannot carry new work:
`git fetch origin main && git checkout -B claude/sirna-evidence-research-k8btv0 origin/main`.
Land via a **new** PR. Never push to `main`.

---

## Verified facts, so they are not re-derived or re-litigated

- `test_parameter_usage_matches_the_code` (`:199`) reads **only** `gen/balance.py`. So `used_by=docs`
  parameters may be read freely by `gen/controls.py`; §A's convention is sound.
- `test_cross_molecule_parameters_declare_the_transfer` (`:675`) will **not** fire on any source this
  slice cites — `_FOREIGN_CLASS_TOKENS` (`:661`) matches nothing in the `scale_system` of
  `SRC-ALMAC-2023`, `SRC-KEIL-2021`, `SRC-MALEK-2019`, `SRC-USPTO-10640812`, `SRC-CN119265174` or
  `SRC-PBCV1-2014`. **That guard has a blind spot**: "DNA" is not a foreign-class token, so a
  PBCV-1-sourced parameter would pass unchallenged even though that source's own `scale_system` says
  "does NOT transfer". If a parameter cites PBCV-1, write the caveat by hand.
- `flowsheet.SENTINELS = {"SUPPLY","WASTE","DS-STORE"}` at `gen/flowsheet.py:20`, importable.
- All 15 equation ids match `EQ-[A-Z]+`, so they satisfy the citation regex unchanged.
- `risks.csv` vocabularies: `unit_op ∈ {All, Cleaning, Evaporation, Filtration, Ligation, Spray drying,
  UF/DF}`; `category ∈ {formulation, microbial, process, product, purity, quality}`.
- Next free ids: **Q-050**, **R-021**.
- Line endings are mixed — 8 of 10 CSVs are CRLF, `streams.csv` and `scenarios.csv` are LF.
- Generated Markdown is git-ignored and listed file-by-file in `.gitignore`; `docs/diagrams/bfd.svg` is
  generated *and* committed, with a byte-drift test. This slice touches no streams, so the SVG should
  not change — if it does, something is wrong.
- **Verified 2026-09-21**: `mkdocs build --strict` exits **0** while printing a red-coloured
  "Warning from the Material for MkDocs team" line. The red notice is benign and is *not* a failure, so
  judge this gate by exit code and never by the presence of coloured output. (`python -m gen.build`
  also exits 0, and the suite is 51 passed at `ef256a8` plus this file.)
