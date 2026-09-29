# Audit Tier-3 slice 4 — the completed, merged work

`theqtl/HelloWorld`. The slice is **merged to `main` as `d6c5676`**. Its whole diff is
`2ab632c..d6c5676`: 29 files, **+4,246 / −188**, 13 squashed commits, and it took the suite from
**147 to 234 tests**. The plan and working brief are at the repo root as `TIER3-SLICE4-PLAN.md` and
`TIER3-SLICE4-EXECUTE.md`.

**READ-ONLY. Do not edit, commit, push or open a PR.** Produce findings. Fixes come later, if approved.

## Why this needs an adversarial audit rather than a read-through

The slice's own history is the argument. Before a line was implemented, three audit rounds ran and
**each overturned something**:

1. Four role reviewers, launched together so none saw the others: **all four rejected.**
2. A red team on the planner's four findings: **two refuted, one's reasoning refuted.**
3. A second-order audit that re-retrieved the documents behind round 2: **refuted the plan's headline
   research result**, and found a published contradiction underneath a withdrawal the planner had
   already made.

Then **phase 4 refuted six more of the plan's own claims** by retrieving its own sources. Nothing in
this project has survived first assertion intact. Treat every claim below as a claim with a name on
it, and prefer a refutation with evidence over agreement.

## The claims to attack, and how

### Wave 1 — the red team, BY EXECUTION not by reading

Copy the repo to a scratch directory and exploit it. Never write to the working tree. For each, report
CONFIRMED / PARTLY WRONG / REFUTED with the command and its output.

1. **"An estimate is physically unable to reach a balance number."** Try to make one reach it. Put a
   `judgement` row with an `est_value` on a parameter `gen/balance.py` reads and see whether any
   published figure moves.
2. **"The fabricated-value refusal works."** Re-run the original exploit — set
   `P-LIG-SEG-CONC.value = 5` with provenance untouched — and confirm it now FAILS. Then try to get
   round it: the same value under `judgement`; under `fact` citing a source that exists but is graded
   `abstract-only`; under `inference` with a source that resolves; the value written with a
   `range_kind` that differs from the envelope's. Report every variant that slips through.
3. **"`judgement` is refused outside `ESTIMATE_REGISTERS`."** Try it in each of the other eight
   provenance-carrying registers.
4. **The four `estimate_offenders()` limbs, each attacked separately** (`gen/envelope.py:314`): the
   quantity column staying blank; `basis` tokens resolving; no source graded
   `abstract-only`/`record-only`/`not-retrieved`; at least one `Q-` named; that question being `open`.
   Find the limb with the weakest enforcement.
5. **"Every new guard is mutation-proved, and each proof re-checked by disabling the guard."** Test it
   properly: neuter each of the six new offender functions in turn — `provenance_offenders`
   (`gen/dataio.py:285`), `solution_offenders` (`:162`), `cip_coverage_offenders` (`:218`),
   `criterion_source_offenders` (`:272`), `estimate_offenders` (`:314`), `value_written_where_refused`
   (`gen/envelope.py:713`) — make it return `[]`, and confirm at least one test fails. **A guard whose
   disabling breaks nothing is not a guard**, and this is the single highest-value check in the audit.
6. **The unbounded-loss fix.** Phase 5 claims `P-UFDF-HOLDUP-LOSS` at 1.2 previously gave a composed
   yield of −0.2917 and a ligation volume of −30,483 L, published by the build. Confirm that now fails,
   and probe the bound: try 0.85, 0.99, 1.0, and a negative value. Is the guard's range the right one?
7. **Re-run every published figure** rather than trusting it: the Mid-scenario ligation volumes
   (claimed 33,340 / 11,002 / 8,229 L at 5 / 15 / 20 g/L), `cip_water_approx_L` (2,800 L) and
   `cip_circuits` (7). Use the `_excipient_sensitivity` deep-copy idiom; write nothing.
8. **Verify the housekeeping claims:** 234 tests on `d6c5676` and 147 on `2ab632c`; the eight
   committed SVGs byte-unchanged across the slice; no `data/*.csv` line-ending flip; the gates green in
   CI order with generated pages deleted first.

### Wave 2 — the retrieval audit, on documents not on the register

The register is not evidence for itself. Retrieve each document and check the quote character by
character. `curl` beats WebFetch on long documents (WebFetch silently truncates and has produced a
confident false "no data" in this project); Espacenet, WIPO, ACS, ScienceDirect, NEB and Merck's own
hosts 403; the Almac SI uses **U+2019, not a prime**, so a quote written with a prime will not match.

1. **The three estimates' bases** — every `SRC-` token in `BUF-CIP`, `BUF-DF` and `BUF-FINAL`.
2. **`SRC-ATWELL-2017`**: did it run 90 full-factorial coupon cleans, and does it find 1% w/v NaOH the
   minimum for an effective clean? **Which industry is it?** If it is a brewery study, is that
   disclosed in the row, and is a brewery soil sound evidence for a ligase/oligo soil?
3. **Phase 5's carryover criteria**: PIC/S PI 006-3 §7.11.3 and WHO TRS 1019 Annex 3 — the 10 ppm and
   0.1%-of-dose figures verbatim, and the most-stringent-of-three rule. **Then the strongest specific
   claim in the whole slice: that WHO sources its 10 ppm figure to a heavy-metals limit for starting
   materials, and that it is therefore not health-based.** That claim is load-bearing for why
   `P-HBEL-DS` stays blank. Verify or refute it.
4. **The Almac contradiction**: that `5 mM` appears once in the main text and never in the SI, `2 mM`
   three times in the SI and never in the main text, and **no erratum reconciles them**. Count them
   yourself with two independent extractors.
5. **`SRC-SIRNA-LABELS`**: that four of seven approved siRNA products carry no weighed excipient at
   160–200 mg/mL, and that Givlaari and Leqvio are verbatim *"formulated in Water for Injection"*.
6. **Spot-check two of the six plan claims phase 4 says it refuted** — including that the Millipore
   guide *"names no polymer for either membrane"*. If phase 4's refutations are themselves wrong, two
   layers of correction are built on sand.

### Wave 3 — the role panel, all four launched in ONE message so none sees the others

Each returns, in at most 500 words: `ACCEPT` or `REJECT`; ONE binding blocker; two or three concrete
additions; and anything actively wrong with a file or line. Tell each not to hedge into consensus.

- **QA / regulatory CMC.** Could an estimate be read as a specification, an established condition or a
  proven acceptable range — on the site, in a CSV export, or in a register printout? Is registering
  10 ppm and 0.1%-of-dose as `fact` honest given they are one convention re-published? Is
  `P-HBEL-DS` staying blank defensible, or is it now a gap the slice made easier to ignore?
- **Process / facility engineer.** After all six phases, does anything size? Is the CIP water floor
  useful or actively misleading, given it counts no rinse and crosses a 50× scale gap? Is the
  33,340 L finding actionable or a curiosity?
- **Data architect.** Judge the schema as built, not as planned. Is `est_value`/`basis`/`falsifier`
  the right shape, or does an estimate belong in its own register? Did the slice introduce **new**
  polysemy while fixing the old — four vocabularies now describe epistemic status, plus
  `endpoint_sourcing`. Is `ESTIMATE_REGISTERS` a principled set or an allow-list?
- **Epistemics / knowledge management.** The user's actual requirement was *"it would be clear what is
  inferred when I look"*. **Check the LIVE DEPLOYED SITE, not just the repo** — the slice's own
  history includes a page that was correctly generated, correctly gitignored, correctly guarded and
  linked from nothing. Does the marker appear where numbers are read? Does the estimates census list
  all three? What decays now that did not before, and what guard prevents it?

## Deliverable

1. A verdict per Wave 1 claim, with the command and output that decides it.
2. A verdict per Wave 2 document, with the verbatim text and URL.
3. The four panel verdicts, reproduced without reconciliation — **four rejections for four different
   reasons is a publishable result, not a failure.**
4. A defect list ranked by severity, separating **things that are wrong** from **things that are
   merely unfinished** (the slice deliberately left `buffer_ref`, `P-HBEL-DS`,
   `P-ENZ-CLEARANCE-LRV` and `P-LIG-SEG-CONC` — do not report a deliberate gap as a defect; the plan
   and brief say which are which).
5. Explicitly: **what you verified by execution or retrieval, versus what you took on trust.** If you
   could not check something, say so rather than assuming it holds.
