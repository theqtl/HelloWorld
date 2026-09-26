# Plan: let this repo carry engineering judgement, labelled and guarded

`theqtl/HelloWorld`. Branch `claude/sirna-evidence-research-k8btv0`, restarted from `origin/main`
(`git fetch origin main && git checkout -B claude/sirna-evidence-research-k8btv0 origin/main`).
**Never push to `main`** — the site deploys from it. Plan first; do not start editing.

## The ask, in one sentence

This register currently refuses any number that is not in a retrieved document. Make it able to
carry **educated engineering estimates** — values from general process/chemistry knowledge rather
than a citation — in a way that is **unmistakable on sight** and **impossible to confuse with a
sourced fact or with an illustrative placeholder**. Then use it to fill the gaps worth filling:
the **buffer register first** (three rows, one of them real, behind a six-instrument buffer-prep
suite and a four-instrument CIP system with no registered cleaning solution), then the ligation
parameter gaps.

The user's words: *"It would be clear what is inferred when I look but it would be nice to make
some educated assumptions."*

Two follow-up exchanges shaped this, both recorded below rather than summarised away: the user
chose the fourth-provenance-value option over reusing `assumption` or building a separate register,
and then asked *"Do you think there is only one type of buffer that use ever used or?"* — which is
what surfaced the buffer register as the real hole.

## Two decisions already taken — do not re-open them

1. **A fourth `provenance` value, plus a mandatory guarded basis field.** Not "reuse `assumption`",
   not "a separate estimates register". The reason is in the numbers below: `assumption` already
   covers two unlike things across 35 rows, and adding to it makes that worse.
2. **Scope: `buffers.csv` first, then the ligation parameter gaps.** Not a retro-fit audit of all 35
   `assumption` rows (that is a later slice, and worth registering as a question), not "just do it
   ad hoc". The scope was originally stated as the ligation parameter gaps alone; it was widened
   after the buffer register was measured — see **The buffer register is the real hole** below. The
   buffers are the *better* first test of the new provenance value, because a T4 PNK reaction buffer
   and a caustic CIP recipe are among the most standardised solutions in the industry, so a labelled
   estimate with a stated basis is genuinely strong there. `P-HBEL-DS` by contrast needs compound
   tox data that recall cannot supply.

## Why this is a schema change and not just permission

`provenance` has three values. Across the 47 parameter rows: **6 `fact`, 6 `inference`, 35
`assumption`**. That one word currently covers two things with different reliability and different
consequences if wrong:

| Row | What it actually is |
|---|---|
| `P-EVAP-T-BOIL` = 50 °C, band 40–60 | an **illustrative placeholder** — the balance needs a number to run; no claim it is right |
| `P-EPS-260` = blank, band 20–25 mL/mg/cm | an **educated estimate** — bracketed from standard A260 conversions plus duplex hypochromicity, `range_kind=argued`, no source at either end |

Same label, same amber colour, same guard. `P-EPS-260` is the **working template** for what the
user wants and it already passes all 147 guards — so the capability exists; what is missing is the
label that distinguishes it, and the discipline that makes it safe.

## The rules this deliberately relaxes, and how far

The original slice prompt said, verbatim: *"Retrieve documents; do not recall them"*, *"Never
invent, round or extrapolate"*, *"A gap stays blank and becomes a registered question."* Those were
applied absolutely, which is why the ligation slice produced Q-057…Q-070 instead of estimates.

The relaxation is **narrow and conditional**, and every condition is a guard:

- a recalled value must be labelled with the new provenance value — never `fact`, never `inference`
  (which means *our arithmetic on sourced numbers*), never `assumption`;
- it must carry its **basis** — the reasoning, in a dedicated field, guarded non-blank. An estimate
  with no stated basis is indistinguishable from an invented number, and the thing that makes
  `P-EPS-260` trustworthy is that you can *attack* its stated reasoning;
- it must **still reference its open question**. An estimate does not close a gap. This is the
  single most important property: `Q-0xx` stays `open` and the row points at it, so filling the
  number never quietly retires the need for real data;
- prefer a **range over a point**. A range shows the uncertainty a point value hides. Where a point
  is given, the basis must say why the variable's spread does not matter;
- *"Never invent, round or extrapolate"* still holds for anything presented as sourced. And the ISA
  prohibition is untouched: no ISA clause text, letter tables or symbol tables, nothing
  reconstructed from memory; `SRC-ISA-5-1-2024` and `SRC-ISA-TR5-1-02-2024` stay `not-retrieved`
  and Q-053 stays open.

## Why the caution is not theatre — this repo is its own evidence

Read `docs/sources/ligation-evidence.md` first. Its four **withdrawn** claims were all
recall-shaped and all *looked right*:

- the 45–75 °C inactivation bracket, whose lower endpoint was a recalled figure that one pass
  called a melting temperature and another an activity midpoint, with no retrievable document to
  settle it;
- a 2.7-log endotoxin comparison that silently merged two different proteins from two different
  tables and converted a host-strain difference into a purified-vs-crude one;
- a yield claim that **inverted its source's polarity** (71% of yield lost vs. ~3% gained);
- a block-count "sign error" that was not one.

None was caught by reading it. All were caught by re-retrieval. **Recalled numbers fail quietly.**
That is an argument for labelling them loudly, not for refusing them.

## Verified state of the tree (measured, 2026-09-26 — do not re-derive, but do re-confirm before editing)

- Head `2ab632c`, working tree clean, `python -m pytest gen -q` → **147 passed**.
- `PROVENANCE_VOCAB = {"fact", "inference", "assumption"}` at `gen/test_balance.py:1249`, consumed
  at `:1342` and `:1350` (the referential-integrity sweep over `controls` and `instruments`).
- **`test_no_value_without_provenance` (`gen/test_balance.py:~36`) re-lists the three values inline**
  instead of importing the constant. That is the anti-pattern this repo names explicitly; fix it as
  part of the change, or the fourth value will be legal in one guard and illegal in another.
- `test_assumption_params_reference_a_question` (`:~26`) requires `"Q-" in notes` for every
  `assumption`. The new value needs the same requirement — see the honesty rule above.
- `parameters.csv`: 13 columns, header ends `...,range_low,range_high,range_kind`, **CRLF**, 47 rows.
  A 14th field appends cleanly: `csv.writer(quoting=QUOTE_MINIMAL, lineterminator='\r\n')`
  round-trips it so every data line becomes exactly `<old line>,` — verified byte-wise. Ten CSVs are
  CRLF; `streams.csv` and `scenarios.csv` are LF. Quoting differs per file.
- **Twelve CSVs carry a `provenance` column**: buffers, controls, couplings, envelopes, equipment,
  impurities, infoneeds, instruments, parameters, scenarios, utilities, verdicts. Decide and state
  whether the new value is legal in all of them or only in `parameters` — the sweep at `:1342`
  currently polices `controls` and `instruments` against the same constant.
- `range_kind` counts: 10 `evidence`, 1 `argued` (`P-EPS-260`), 1 `design_intent`
  (`P-EVAP-T-BOIL`), 35 blank. `proven_acceptable_range` and `design_space` are deliberately empty
  ICH terms with a guard that no row claims them.
- **CSS**: `docs/stylesheets/extra.css:13-15` defines `.prov-fact` `#2e7d32`, `.prov-inference`
  `#1565c0`, `.prov-assumption` `#b26a00`. **There is no dark-mode block in the file at all** — check
  the chosen colour against both Material themes rather than assuming.
- **Two legends list the three values and will go stale**: the generated parameters-register intro
  in `gen/build.py` (the `("parameters", "registers/parameters.md", ...)` spec) and the
  hand-written **"Provenance discipline"** section of `docs/index.md`, which uses the
  `<span class="prov-…">` chips.
- **Copy the pattern that already exists for exactly this problem**:
  `test_the_access_legend_covers_the_whole_vocabulary` checks the reading-list legend against
  `ACCESS_VOCAB` **both ways** — every vocabulary value appears, and the legend explains nothing
  outside the vocabulary — never against a re-typed list. Do the same for provenance, and for both
  legends, or this change ships its own staleness.

## The buffer register is the real hole (measured 2026-09-26)

This was missed when the scope was first written. `data/buffers.csv` has **three rows, and one of
them is real**:

| Row | State |
|---|---|
| `BUF-LIG` | genuine - `provenance=fact`, pH 7.5, four components quoted verbatim from `SRC-ALMAC-2023` |
| `BUF-DF` | *"Exchange from reaction salts toward final matrix - composition TBD"*, **pH blank**, `assumption` |
| `BUF-FINAL` | *"Glass-forming excipient (trehalose/sucrose?) + minimal/volatile buffer - TBD"*, **pH blank**, `assumption` |

Meanwhile `equipment.csv` carries **`U00-BUF` "Buffer preparation & hold suite"** with **six
instruments** on it, sized on *"Total buffer volume/campaign (DF diavolumes dominate)"* - a whole
unit operation devoted to preparing three buffers, two of which have no composition. And
**`U06-CIP` "CIP/SIP system"** carries four instruments with **no registered cleaning solution at
all**: `NaOH`/`sodium hydroxide` appears only in `impurities.csv`, `risks.csv` and `sources.csv`,
never as a buffer row with a concentration, a temperature and a contact time. `P-HBEL-DS`, the
cleaning *acceptance limit*, is also blank - so neither the agent nor the criterion is registered.

### Solutions the repo's own content implies, with no row at all

1. **The phosphorylation / kinase (PNK) solution.** The structural one. `SRC-ALMAC-2023` runs a
   kinase step with a 75 degC heat treatment between it and ligation; `S01`/`S02` already assert the
   blockmers arrive 5'-phosphorylated; `ENV-008` is a PNK envelope row and a PNK risk row exists.
   An entire enzymatic reaction step with **no solution registered and no unit operation**. Check
   whether adding a unit operation ripples into an eighth PFD SVG and a `flowsheet.UNIT_LABELS`
   entry before committing to it.
2. **The quench solution.** `Q-059` is open on what terminates the reaction. `BUF-LIG`'s own note
   already reasons that chelating its 10 mM Mg2+ at the quench would form net-negative Mg-EDTA and
   point it the *right* way through the membrane (`C-014`). The register contains reasoning *about* a
   quench solution and no row for one.
3. **CIP/SIP solutions** - see above. Caustic concentration, temperature, contact time, acid step if
   any, and the final rinse. Standardised enough to estimate; state the basis.
4. **UF/DF membrane flush and storage solutions.** Absent.
5. **IMAC equilibration / wash / elution buffers.** Absent, and **legitimately conditional on
   `Q-050`** - do not add these while the enzyme-form fork is open. Note that the nickel-leaching
   envelope bracket already carries the flag that both its endpoints are *elution* conditions while
   the process never elutes.

### Two structural defects, not just missing rows

- **No guard relates a unit operation to the solutions it runs in.** Plenty of guards check that a
  buffer row is *well formed*; nothing checks that a reaction step *names its solution*. This is the
  same shape as the reachability defect fixed in PR #8 - there the pair was *data reaches a page* vs
  *a page reaches a reader*; here it is *a buffer row is valid* vs *a unit operation has the
  solutions it needs*. `test_a_control_that_acts_names_the_instrument_that_enforces_it` is the
  idiom to follow. Decide the domain carefully: `equipment.csv` has seven unit operations
  (`U00-BUF`, `U01-LIG`, `U02-CF`, `U03-UFDF`, `U04-EVAP`, `U05-SD`, `U06-CIP`), and not all of them
  consume a solution, so an honest guard needs a declared set of *solution-consuming* operations
  rather than a blanket rule - and that set must be derived or defended, not hand-waved.
- **There is no `buffer_ref` column anywhere.** Buffer ids are mentioned **17 times** across
  `streams`, `controls`, `instruments`, `risks`, `questions`, `impurities`, `couplings`, `infoneeds`
  and `verdicts` - and every one of those mentions is **free text inside another field**, so none is
  referentially checked. The reference sweep at `gen/test_balance.py:~1335` resolves `unit_op`,
  `equation_ref`, `risk_ref`, `instrument_ref` and `gap_ref`; `buffer_ref` is not among them. A
  typo'd buffer id is invisible today. `buffers.csv` is **CRLF**, 3 data rows, 9 columns.

`buffers.csv` is the only register that never received a slice: parameters gained `range_kind` and
the envelope, controls gained a matrix, instruments gained per-unit PFDs, sources gained an access
vocabulary and a reading-list census. Buffers still has its seeded shape.

## The ligation parameter gaps, with what actually blocks each

The second half of the scope. Blank-valued and band-less today. **`BUF-LIG` is NOT on this list** — it was filled during the last
slice from a verified `SRC-ALMAC-2023` quote (50 mM Tris-HCl pH 7.5 / 100 mM KCl / 10 mM MgCl₂ /
1 mM DTT) and is `provenance=fact`. Do not re-open it.

| Parameter | Registered blocker | Honest prospect for an estimate |
|---|---|---|
| `P-LIG-SEG-CONC` | blockmer charge concentration; 1 mM works and 10 mM is "slow and failed to go to completion", with **no datapoint between 1.5 and 10 mM** (Q-064) | plausible — the *mechanism* of the 10 mM failure (substrate/product inhibition, duplex aggregation, viscosity limiting mixing and heat transfer) supports an argued ceiling. Endpoints will be soft; say so |
| `P-HBEL-DS` | health-based exposure limit for cleaning limits | plausible — the **framework** is standard and citable in outline (PDE via adjustment factors; the older 1/1000-dose and 10 ppm criteria; the default-of-last-resort band used when no compound tox data exists). State the framework, bracket the default, and **do not invent a NOAEL** |
| `P-LIG-ENZ-LOAD` | candidate loadings are in **mutually inconvertible units** and the bridging quantities are absent from every source read | partly — a mass-basis figure already exists in the register's own evidence (0.4 mg/mL in `SRC-CN119265174` Example 12). An estimate can bridge to a mass basis per branch; it cannot invent the U→mg conversion. **`test_enzyme_parameters_stay_registered_gaps` deliberately holds `value` blank and requires the Q-050 back-reference and that the envelope rows not collapse to one branch — read that guard before touching this row** |
| `P-ENZ-CLEARANCE-LRV` | no achieved clearance figure for **either** enzyme branch (Q-032) | weak — the answer depends on the unresolved soluble-vs-immobilised fork (Q-050) *and* on the fact that the ligase (~38 kDa) is **larger** than the product duplex (~14 kDa), so size-based clearance runs the wrong way. A branch-conditional estimate is possible; a single number is not. **Consider leaving this blank and saying why** — that is a legitimate planning outcome |

**Say plainly in the plan which of these your knowledge cannot honestly fill.** A plan that promises
four estimates and delivers two vague ones is worse than one that promises two and names the other
two as genuinely not-knowable-by-recall. The four-way split in `data/infoneeds.csv`
(`bracketed_evidence` / `bracketed_argument` / `point_justified` / `not_knowable`) already exists —
use it, and check whether these rows need their `disposition` updated.

## House conventions that silently corrupt a diff

- **Gates, judged by exit code, never piped through `tail`** (the pipe reports `tail`'s status):
  `python -m pytest gen -q ; python -m gen.build ; mkdocs build --strict`. Run pytest with the
  generated pages deleted first (`git clean -fXd docs`) — CI runs pytest **before** the build, and a
  guard that reads a built page passed locally and failed CI once already.
- Baseline **147 tests**. Every new guard must be **mutation-tested against a failing case** in
  `gen/test_mutations.py`, which copies `data/` to a tmp dir and monkeypatches `gen.dataio.DATA_DIR`
  so the working tree is never written. Anchor every mutation on a **row id**, never a field value.
  Assert the guard **raises**.
- Controlled vocabularies are module constants with a runtime `raise` in the consumer **and** a guard
  that **imports the constant** rather than re-listing it.
- `mkdocs` prints a red "Warning from the Material for MkDocs team" line and still exits 0 — that is
  not a failure.
- `docs/diagrams/bfd.svg` and the seven PFD SVGs are generated **and committed** with byte-drift
  tests. They must be byte-unchanged unless stream data deliberately changed.
- `balance._require` raises on a blank, so a blank `value` is only safe for parameters no balance
  path reads — check `used_by` (matched by bare substring over the whole text of `gen/balance.py`,
  comments included).
- Every generated page must be in the `mkdocs.yml` nav **and** linked from a hand-written page —
  both are now guarded.
- Next free ids: check by `max` rather than assuming; `questions` is at **Q-070**. Ids append at the
  end, not in numeric order.

## What the plan must decide and state

1. The **name** of the fourth provenance value. It has to read unambiguously in a table cell next to
   `fact`/`inference`/`assumption`. Candidates: `judgement`, `estimate`, `engineering_estimate`,
   `recalled`. Argue the choice; the word is a permanent API.
2. The **name and semantics of the basis field**, and whether it is **exclusive** to the new value
   (recommended: a bidirectional guard, so `basis` non-blank ⟺ provenance is the new value, which
   stops it becoming a free-text dumping ground) — versus also allowed on `inference`.
3. Whether the new value is legal in all twelve provenance-carrying CSVs or only `parameters`.
4. The **colour**, checked in light and dark.
5. Whether the generated `ligation-envelope.md` page needs a section that lists the estimates
   together, so a reader sees every recalled number in one place rather than scattered through a
   47-row table.
6. Which of the four gaps get estimates, which stay blank, and the question id each keeps.
7. Whether to register a question for the **deferred** retro-fit of the 35 existing `assumption`
   rows into placeholder-vs-estimate.
8. Whether `buffers.csv` gains a `basis` column too, or whether the basis for a buffer lives in its
   `notes` - and if the former, whether the guard is shared with `parameters.csv` or duplicated.
9. Whether to add a **`buffer_ref` column** to the registers that already mention buffer ids in free
   text, and wire it into the reference sweep. This is worth doing independently of the estimates and
   may deserve to be its own phase, since it is a referential-integrity fix rather than a knowledge
   question.
10. Which solution-consuming unit operations the new guard covers, and how that set is defended.
11. Whether the phosphorylation step becomes a real unit operation (with its PFD/`UNIT_LABELS`/BFD
    ripple) or stays a supplier-side telescoped charge with a registered question.

## Deliverable

A phased plan where **each phase leaves all three gates green**, with the data-model phase landing
independently of any estimate — so the machinery is reviewable before any recalled number rests on
it. Land via a **new PR**; do not create one until asked. Report at the end what was verified **by
execution** versus only reasoned about.

One more lesson from this session, worth carrying: if a file you expect is missing, run
`find / -name '<file>'` before concluding anything. A scratchpad path changed mid-session and the
wrong conclusion drawn from its absence was that an entire research phase had been fabricated.
