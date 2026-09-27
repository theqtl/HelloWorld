# Tier-3 slice 4 — engineering judgement as a labelled provenance

## Context

The register refuses any number not in a retrieved document. Good discipline, and it produced 47
parameters of which **35 are `assumption`** — one word covering two unlike things: an *illustrative
placeholder* the balance needs to run (`P-EVAP-T-BOIL` = 50 °C) and an *educated estimate*
(`P-EPS-260` = 20–25 mL/mg/cm, bracketed from A260 conversions plus hypochromicity, no source either
end).

The ask: carry educated estimates so it is **clear what is inferred when you look**, without letting
them pass as sourced facts.

**Three audit rounds ran before this was written.** Four role reviewers each returned **REJECT**, for
four different reasons. A red team attacked my four planning findings: two refuted, one's reasoning
refuted, one confirmed by reproduction. Then a second-order audit re-retrieved the documents behind
the red team's and the research beat's claims, and **refuted the plan's own headline research result**.
The corrections below are the most valuable content here.

## Decisions taken with the user

- A fourth `provenance` value **plus a mandatory guarded basis**, but **fix the polysemy first**.
- **Rename `envelopes.provenance`** (to `endpoint_sourcing` or similar) rather than reconciling data:
  the two columns answer different questions.
- **Marker in the cell + a generated census page**, not a CSS chip alone.
- **A falsifier field, guarded.**
- **Both** the buffer compositions *and* the sizing work.

## Audit round 1 — the red team on my claims

**REFUTED — "the only retrieved quench is thermal, so a chemical quench would invent a route."** Four
registered sources name a chemical stop, including the one my claim rested on. `SRC-WO2025262452`'s
register quote is **truncated one sentence early**: *"diluted 400-fold in **10 mM EDTA pH 7.0**"*.
`SRC-NEB-WO2023173098` names a *"2x Quench Solution (20 mM EDTA, 2% SDS)"*. `SRC-PBCV1-2014` a
*"stop solution containing 50 mM EDTA and 10 mM Tris–HCl at pH 7.5"*. And `SRC-ALMAC-2023` quenches
with **methanol** — a sentence the register already cites, **for its percent sign**, to support a claim
that the text contains exactly one `%`. It had the quench in hand and read it for punctuation. So
`Q-059`'s *"the only retrieved quench is thermal"* is false of the documents (true only of the CSVs),
and a quench row is **supportable**. Caveats that must travel: every chemical stop is at an
**analytical sampling point**, not a process unit operation; and the paper's two methanol quenches are
almost certainly **one operation described twice** (1 volume ≈ 100% v/v), not two data points.

**REASONING REFUTED, conclusion survives — "no separate phosphorylation buffer, because one-pot."**
"One-pot" means the two blockmers phosphorylated *together*, not kinase and ligase sharing a vessel.
The conclusion holds for a better reason: SI **Tables S1 and S2 are identical component-for-component
including pH** — verified independently with two PDF extractors to rule out a dropped row — so a PNK
composition row would duplicate `BUF-LIG`. But a real process step is missing from the register:
*"heat treated at 75 °C for 10 min (initial) or 30 min (crude), then **centrifuged to pellet any
precipitated material and supernatant used for ligations**"* — a thermal hold, a **solids rejection**
and a supernatant transfer. And `SRC-NEB-WO2023173098` names a **distinct** kinase buffer with its own
vessel change.

**CONFIRMED by reproduction — the deliberate-blank hole.** The red team set
`P-LIG-SEG-CONC.value = 5` keeping `provenance = assumption` in a throwaway copy: **147 passed**, and
`gen.build` published the fabricated value. I verified the cause statically —
`range_written_where_refused()` (`gen/envelope.py:352`) reads `range_low`, `range_high`, `range_kind`
and **`value` never appears in the function**. The only accidental tripwire is
`test_no_value_without_provenance` policing the vocabulary — **exactly what this slice removes.**

## Audit round 2 — the second-order audit, which refuted my headline

**The 5 mM withdrawal rested on a contested number.** I withdrew a planning claim because the SI says
*"Phosphorylation of the 5′-OH blockmers at **2 mM** concentration was telescoped into the ligation
reaction at **1 mM** concentration"*. That quote is exact. But the **main text describes the same
experiment** — same one-pot phosphorylation of 1.2/1.3, same ligation of 1.4 then 1.1, same Figure S5
reference — and says **5 mM**. The published record is **internally inconsistent**, and *"2 mM"* never
appears standalone in the main text. So neither the original claim nor my withdrawal is safe. What is
registrable is **the contradiction itself**, as a new question: a peer-reviewed paper and its own SI
give two different charge concentrations for one experiment. Standalone-token counts, measured: `5 mM`
appears once in the main text and never in the SI (the other hits are inside `0.5 mM`).

**REFUTED — "the membrane numbers are evidence with both ends independently sourced across two
vendors."** They are **one inherited industry convention**, not two measurements:

- The identical bracket — 0.1–0.5 N, 30–60 min, ~25/30–50 °C — recurs across **two vendors, three
  product lines and at least three polymers**, with unit drift (N / M / N) that is itself a tell of
  copied legacy text.
- **Millipore publishes one NaOH bracket for both Ultracel (regenerated cellulose) and Biomax
  (polyethersulfone)** — internal proof the numbers are not chemistry-specific measurements.
- **The ends conflict rather than corroborate.** Millipore permits 25 °C; Cytiva's HF handbook says
  20 °C is *"not recommended"* and prefers 50 °C; Cytiva's own CFF table then prescribes 20 °C for a
  hypochlorite/NaOH blend. Two Cytiva documents disagree.
- **Millipore's cited row is chemically self-contradictory**: 0.1–0.5 N NaOH is pH 13–13.7, not the
  *"pH 10–11"* printed beside it — that looks carried over from the adjacent hypochlorite row, and
  Cytiva independently says **pH 13**. Citing "0.1–0.5 N NaOH, pH 10–11" **propagates a typo**.
- Millipore also **discourages the very endpoint being cited**: *"There is an initial NWP decline …
  after initial exposure to 0.5N NaOH. Better membrane life has been observed at lower
  concentrations."* And it carries a **100-hour cumulative exposure budget** with no Cytiva
  counterpart, which merging the sources silently discards. Cytiva explicitly disclaims
  transferability.

So the membrane row is `one_source_both_ends` at convention level — **not** `two_independent` — its
access grade must be **downgraded off `full-text-read`** (the only reachable copy is a third-party
reseller mirror, frozen 2016, Merck's own hosts 403, currency unverifiable), the pH figure must be
dropped, and the 100-hour budget carried.

**PARTLY WRONG — the alkaline-resistance claim.** The mechanism half is supported and now better
evidenced: the product has **zero 2′-OH** (both strands tokenised from the SI — 21 and 23 residues, all
2′-OMe or 2′-F), and Egli & Manoharan (*NAR* 2023, open access) state *"Modification also affords
chemical stability in that it precludes 2′-OH-mediated strand cleavage."* But *"alkaline"* appears
**zero times** in that review, no primary source exposed a fully 2′-modified siRNA to caustic cleaning
conditions, and *"resists"* ≠ *"is inert"* — the backbone and the GalNAc amides remain. **The "so" is a
non sequitur**: cleaning validation nowhere requires the residue to be chemically degraded; Annex 15,
PIC/S, WHO and ICH Q7 all set **removal limits measured analytically**. Keep the mechanism, drop the
inference.

**PARTLY REFUTED, and this one is a gain — "the regulatory record has no numeric cleaning value at
all."** True for **caustic concentration, temperature and contact time** (genuinely absent from all
five documents). **False for residue-acceptance criteria**, which are citable and mandatory in phrasing:
PIC/S PI 006-3 §7.11.3 and WHO TRS 1019 Annex 3 §11.9–11.10 both give *"no more than 10 ppm"* and
*"no more than 0.1% of the normal therapeutic dose"*, WHO explicitly *"in rinse water as ppm"* (§11.6)
and *"the most stringent of three options should be used"* (§11.10). **This changes the `P-HBEL-DS`
decision** — see phase 5.

**CONFIRMED, and weaker than I framed it — the ISPE 1%.** The word *"Assume"* is there, and the figure
sits inside a list headed *"Assumptions"*, used only to convert 720,000 L of water into 7,200 L of
chemical in a waste-arithmetic example. It is a **bookkeeping placeholder, not a process parameter.**

## Audit round 3 — in-repo claims, verified by my own execution

- **The polysemy is 11 rows, not the 2 the panel found.** Every envelope row naming a parameter
  disagrees with `parameters.csv`, systematically and in one direction: `ENV-001/002/003/007/008/009/
  010/012/014/015/016` say `fact` (8) or `inference` (2) where `parameters` says `assumption`.
- `ENV-007/008/009` are `single_point`, `provenance=fact`, `low==high` (0.4, 1, 20) — so merging
  `single_point` into the blank-value guard **would have forbidden phase 5's own estimate**.
- **12 blank-value parameter rows**, provenance unpoliced, because `test_no_value_without_provenance`
  fires only when `value` is non-blank.
- Blank-value guards exist for `P-HBEL-DS` (`:843-846`), `P-LIG-ENZ-LOAD` and `P-ENZ-CLEARANCE-LRV`
  (`:1473`). **`P-LIG-SEG-CONC` has none.**
- `wfi = df_buffer + lig_vol` — **cleaning demand is zero litres** in the number sizing `U00-BUF` and
  `UT-WFI`.
- **The sizing numbers are exact**, re-run in memory via the `_excipient_sensitivity` deep-copy idiom:

  | `P-CONC-LIG` | Low | Mid | High |
  | --- | --- | --- | --- |
  | 5 g/L | 10,002 L | **33,340 L** | 40,008 L |
  | 15 g/L (registered) | 3,301 L | 11,002 L | 13,202 L |
  | 20 g/L | 2,469 L | **8,229 L** | 9,875 L |

  `P-DF-DIAVOL` 4 → 7 → 20 moves DF buffer 3,023 → 5,291 → 15,117 L and WFI 13,727 → 16,293 →
  27,527 L. **A finding in its own right: at the bottom of the concentration envelope the Mid scenario
  needs a 33,340 L ligation vessel, which is not a buildable single vessel.** The bracket decides
  whether the plant exists.

## The panel's four blockers

- **The feature is invisible where numbers are read.** `prov-*` chips exist **only in hand-written
  prose**. My line *"adding a value requires no rendering change"* was the defect stated as comfort.
  Fix precedent already exists: `_with_bracket_verdicts` (`gen/build.py:145`) **already injects
  `**no audit**` markup into a cell.**
- **Phase 2's guards covered `parameters.csv` only while the estimates land in `buffers.csv`** (nine
  fields, no `basis`). The rows the feature exists for escaped every guard.
- **No estimate reached a sizing number** — `param_value` reads `value` only.
- My own errors: *"`SRC-WHO-TRS1044` anchors the CIP requirement"* (naming a gap is not evidence for a
  concentration) and *"`BUF-FINAL` is closer to `evidence`"* (`evidence` is a `range_kind`, not a
  provenance — I conflated the two axes the slice exists to separate).

## Approach — six phases, each leaving all three gates green

### Phase 0 — separate the two axes
Rename `envelopes.provenance` → `endpoint_sourcing`, so the 11 disagreements stop being contradictions
and the new value lands in one column with one meaning. Move `PROVENANCE_VOCAB` from
`gen/test_balance.py:1249` to `gen/dataio.py` beside `RANGE_KINDS`, enforce it across **all twelve**
provenance-carrying CSVs, and replace the four inline re-listings with imports. Relocate
`BRACKET_VERDICTS`/`DISPOSITIONS` out of the renderer and `RISK_UNIT_OPS` out of the test file.

### Phase 1 — make the deliberate-blank refusal real
Extend the refusal from ranges to **values**, keyed on **`not_a_range` alone** (never `single_point`),
and **provenance-independently** — `P-LIG-SEG-CONC` is `assumption`, so a new-value-only guard closes
nothing. Mutation case = the red team's exact reproduction. Also close the `buffers.csv` holes:
`buffers` missing from `test_all_source_keys_resolve` (`:9`), no `buffers.provenance` validation, no
`buffer_ref` column (17 free-text mentions across nine registers), zero buffer mutation coverage.

### Phase 2 — the vocabulary, the fields, the visibility
Fourth value; **`est_value`, `basis`, `falsifier` on every register where it is legal**, not
`parameters` only. **An estimate never touches `value`** (guard), so the balance is *physically unable*
to consume one and "never closes its question" becomes structural. `basis` must resolve its
`SRC-`/`P-`/`EQ-`/`Q-` tokens and **must not rest on a source graded `abstract-only`, `record-only` or
`not-retrieved`**. Add `QUESTION_STATUS` as a vocabulary (free text today) and guard that an estimate's
question is **`open`**. Visibility: a `_with_provenance_markers(rows)` transform beside
`_with_bracket_verdicts`, guarded over the **transform's return value**, never the gitignored page.
`_CITATION` must require the chip **and** a `P-` id. Rewrite `docs/index.md:30-31`, plus the stale
enumerations at `gen/build.py:43-45` and `:219`, `gen/impurity.py:85`, `gen/__init__.py:2`,
`docs/balance/index.md:10`, `docs/techtransfer/index.md:24`, `README.md:43-44` and `:67`.

### Phase 3 — the corrections, owed regardless
Register the **2 mM vs 5 mM published contradiction** as a question; neither number is settled. Qualify
`P-LIG-SEG-CONC` and `Q-064`: the *"6.7× void"* is basis-dependent — the 1.5 mM low end is per-segment
across three segments plus **0.55 mM of tri-template hub** the register never mentions, ≈5.05 mM total,
making the void ~2.0× on a total basis. Correct `Q-059`. Register the **75 °C hold plus centrifugal
solids rejection**. Record in `docs/sources/ligation-evidence.md` that the register read Almac's
methanol-quench sentence for its percent sign.

### Phase 4 — buffers, with the audited split
`BUF-MEMBRANE-CLEAN` as a **convention-level `one_source_both_ends`** row, access downgraded, **pH
figure dropped**, 100-hour budget carried, Millipore's own "lower concentrations" caveat in the notes,
and the Ultracel-vs-PES non-differentiation recorded. `BUF-CIP` stainless caustic as the **judgement**
case, its basis naming the ISPE "Assume" bookkeeping placeholder, the zero-2′-OH mechanism **without**
the degradation inference, and the brewery study that measured no benefit from hot caustic as the
counterweight. A **quench** row with the analytical-scale caveat. `BUF-DF`/`BUF-FINAL` compositions.
**Not added:** a PNK composition row (duplicates `BUF-LIG`), IMAC buffers (conditional on `Q-050`).
Two CIP rows minimum — TFF chemistry differs from every other unit operation.

The **unit-operation → solution guard** needs a prerequisite: three unit-op vocabularies resolve to
each other nowhere — `equip_id`, free-text `equipment.unit_op`, and hardcoded `RISK_UNIT_OPS` where
`Ligation` ≠ `Enzymatic ligation` and `Utilities` is absent. Fix the key, then guard on `equip_id`.

### Phase 5 — the sizing work, and the HBEL reversal
**The carryover criteria are citable** — register 10 ppm, 0.1% of therapeutic dose, no visible residue,
and the most-stringent-of-three rule from PIC/S PI 006-3 §7.11.3 and WHO TRS 1019 Annex 3 §11.6/§11.9–
11.10, as **`evidence`**. `P-HBEL-DS` itself (the PDE) **stays blank**: MACO is a division by one
number, a 10× band gives a 10× swab-limit band straddling the TOC/HPLC LOQ so it cannot select the
analytical method, and its research beat **failed on a safeguard false positive** and was never done.
The criteria and the PDE are different quantities — carry the first, keep the second a gap.

**CIP water and steam into the balance.** **The phosphorylation→ligation dilution as a vessel fill
requirement** — 2 mM *or* 5 mM to 1 mM, so V to 2–5V in one vessel, with the published contradiction
stated rather than resolved; testable against `SRC-PALL-US9248420`'s 13:1, plus a jacket check for the
65 °C anneal at the top fill. **UF/DF area from the registered hold-up loss** (0.10 × 227 L ≈ 23 L; at
1–2 L/m², 11–23 m²) with a consistency guard, since hold-up and area are not independent. **The
range-to-steel table** above, published from the model so it cannot drift.
`P-ENZ-CLEARANCE-LRV` stays blank: it forks on `Q-050` and the ligase (~38 kDa) is larger than the
duplex (~14 kDa), so size-based clearance runs the wrong way.

## Retrieval hazards to carry into the source rows

`fda.gov/media/74033/download` returns a **mis-filed document** (an unrelated IVD package insert), not
the cleaning guide — use the HTML inspection-guide URL. `picscheme.org/docview/3436` is a **newsletter**;
PI 006-3 is **3447**. Merck's own hosts 403. The Almac SI uses **U+2019, not a prime (U+2032)**, so a
quote written with a prime will not string-match. Two FDA chemistry-review PDFs 404 — the best
remaining lead for forced-degradation data on a marketed fully-2′-modified siRNA.

## Also register, do not fix here

`gen/flowsheet.py:32` `VIEW_W = 1160` has **30 px of slack**; any unit inserted into the product spine
clips the last box, with **no test catching it**. The line-ending guard's docstring says *"ten of the
twelve CSVs"* when it is **14 CRLF and 2 LF across 16 files**.

## Out of scope

The retro-fit audit of the 35 `assumption` rows (register it as a question). Anything downstream of
S05. **No new unit operation for phosphorylation** — `pfd.UNITS` is derived from `equipment.csv` so a
PFD cannot be opted out of, and a product stream would force the `VIEW_W` fix plus an SVG re-baseline.
No ISA clause text, letter tables or symbol tables; `SRC-ISA-5-1-2024` and `SRC-ISA-TR5-1-02-2024` stay
`not-retrieved`, `Q-053` stays open.

## Verification

```
git clean -fXd docs ; python -m pytest gen -q ; python -m gen.build ; mkdocs build --strict
```

Judged by **exit code**, never piped through `tail`; generated pages deleted first because CI runs
pytest **before** the build. Baseline **147**. Every new guard mutation-tested against a failing case
in `gen/test_mutations.py` — starting with the red team's reproduction, which must now fail. A column
addition touches the header **and every row** together or the field-count guard fires on all of them;
`buffers.csv` writes **no `""` for empties**, unlike `streams.csv`; keep rows single-line or the CR/LF
count guard trips. Eight SVGs byte-unchanged. CRLF verified per file.

The final report states what was verified **by execution** versus reasoned about, and for every
estimate: its basis, its falsifier, the question it did **not** close, and why a range was or was not
given. Also correct `TIER3-SLICE4-PLAN.md`, committed with claims this audit has since refuted.
