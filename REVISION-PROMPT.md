# Revision brief — apply the evidence dive to the site

You are picking up an siRNA drug-substance knowledge base after an evidence dive. The dive was
deliberately barred from editing the site; you are not. Your job is to land its findings on the
pages, the registers and the balance, and to do it without introducing new unsourced numbers.

Read this whole brief before you touch anything.

## 0. What this is, and what it is NOT

The site documents an enzymatic-ligation siRNA drug substance and its greenfield cGMP facility. It
builds from `main` and publishes to GitHub Pages. The presentation layer is generated from
`data/*.csv` by `gen/`.

Hard non-goals, unchanged from the previous brief:

- **Do not propose a different process.** Enzymatic ligation, filtration-led purification,
  evaporation, spray drying and microbial control are settled decisions. Do not relitigate them.
  Do not suggest lyophilisation. Note carefully: the dive established that the one approved siRNA
  process in the register dries by lyophilisation. That is a fact to record where relevant, **not**
  an argument to change this process, and you must not use it as one.
- **Do not add or remove unit operations, streams or equipment items** to make a finding fit.
- **Do not invent, round, extrapolate or "tidy" a number.** A gap stays blank and is registered as
  a question. The mass balance refuses to run on a blank, and that is a feature.

## 1. Your authoritative inputs

1. `RESEARCH-QUEUE.md` at the repository root. Twenty-eight findings, **F-001 to F-028**, ordered
   by impact, each with a verbatim quotation, the scale and system it applies to, a confidence
   level and a proposed action. Three call-out tables at the top separate contradictions, closed
   questions, and new questions and risks.
2. `data/sources.csv`. Seventy-eight rows, each with the controlled `access` column recording what
   was actually read, and `reachability` recording how to get it. The `notes` field of many rows
   carries the verbatim quotations and the scope caveats you will need. **Read the notes.** Several
   contain corrections to the row's own `citation` field that the dive was not allowed to make.
3. `docs/sources/reading-list.md`. The curriculum, plus three sections you should treat as working
   material: the census of what nobody has read, twenty sourced statements, and a table of claims
   to not repeat.
4. `README.md` for the provenance discipline, and `docs/adr/0001-information-architecture.md` for
   why the site is built this way.

## 2. THE RULE THAT MATTERS MOST: verify each finding against the live page before you edit

The queue is a research artifact, not a work order. It was written by parallel agents and then by a
lead session that did not always check the page it was describing.

**There is a worked example of this failure inside the queue itself.** F-016 was originally entered
as a contradiction claiming the diafiltration clearance equation on the equations page was
mislabelled. It is not. `EQ-DIAF` states `C/C₀ = e^{−σN}` with σ defined as the sieving coefficient,
which is the correct pairing, and the page already carries a note about the alternative form. The
finding was written against a paraphrase rather than the page. It has been retracted in place and
now reads as a source upgrade. **Read F-016 before you start. It is the shape of the mistake you are
most likely to repeat.**

So, for every finding you intend to act on:

1. Open the file and the exact block the finding says it affects. Quote what is actually there.
2. Check the finding's claim against that text, not against its summary.
3. If the finding is right, act on it.
4. If the finding is wrong, **retract it in the queue in place**, the way F-016 was retracted: keep
   the identifier, mark it retracted, say what you checked and what the page actually says. Do not
   delete it and do not silently skip it.
5. If you cannot tell, act on the part you can verify and leave the rest, saying which is which.

Report the count of findings you applied, retracted and deferred. A session that applies
twenty-eight findings without retracting any has probably not checked.

## 3. Write scope

You may edit the whole repository. That is a licence to be careful, not a licence to be broad.

- **Pages** under `docs/`: findings, process, equations, balance prose, facility, `docs/devel/`,
  `docs/techtransfer/`, diagrams.
- **Registers** in `data/`: `parameters.csv`, `streams.csv`, `equipment.csv`, `buffers.csv`,
  `utilities.csv`, `risks.csv`, `questions.csv`, `scenarios.csv`, and `sources.csv`.
- **Code** in `gen/`: `balance.py`, `build.py`, `tables.py`, `dataio.py`, `test_balance.py`.

Do not edit generated files. `docs/registers/*.md`, `docs/balance/results.md` and
`docs/process/streams.md` are produced by `python -m gen.build` and are git-ignored. Edit the CSVs.

`data/sources.csv` rules still hold: do not delete rows, and do not change `source_key` values,
because the documents link to them. You **may** now fix a `citation` field the dive could only flag
in `notes`. F-005 is one such case and there are others; search the notes for the word CORRECTED.

## 4. Provenance discipline, which the test suite enforces

Every numeric value is flagged **fact** (cited), **inference** (our reasoning or arithmetic) or
**assumption** (illustrative placeholder, registered as an open question). The suite checks that a
fact parameter cites a source, that an assumption points at a question, that every question
identifier referenced in any CSV exists, and that a numeric claim in prose has a citation, a
parameter, an equation or a provenance flag within a few lines of it.

Two rules the dive applied that you should keep applying:

- **Carry the scale and system with the number.** A bench result on unmodified RNA does not transfer
  to kilograms of modified phosphorothioate siRNA. Several findings are built on antisense
  single-strand data, on messenger RNA, on plasmid DNA, on polysialic acid or on a sticky
  small molecule. The transfer judgement belongs on the page, not in your head.
- **Separate what a source says from what was concluded from it.** The queue labels its inferences.
  Keep that separation when the inference moves onto a page.

## 5. Work order

Take the queue's own ordering, but group the work so the balance changes once.

### Stage 1 — corrections to things that are currently wrong

F-002, F-005, F-006, F-007, F-020, F-021, F-023 and F-027 all correct something that is on the site
now. These are the cheapest wins and the highest risk of embarrassment if left. In particular:

- F-002: the note on Q-018 says no oligonucleotide evaporation data was found. There is a
  precedent, it is open access, and it was in the register the whole time marked reachable with
  nobody recorded as having read it. **Do not cite its "few hours" figure as a residence time** —
  it is a batch cycle time, and the queue entry says so.
- F-023: strike any surviving "30 kDa upper limit" for membrane cut-off. What replaces it points the
  other way, to cut-offs well below the product mass. Note that the underlying study's own cut-off
  list is still unavailable, so Q-035 stays open on that specific point.
- F-021: four standards are at superseded editions. Update them and note that the explosion
  parameters of the actual powder are a testing deliverable, not a literature value.

### Stage 2 — the two findings that change the reasoning, not just the numbers

- **F-022** is the largest single change this dive produced. The filtration finding treats the
  drug-substance purity specification as an unknown number that decides whether the filtration-only
  case closes. There is no such number and there is not meant to be one: the limit is set from the
  applicant's own toxicology batches and tightens as commercial batches accumulate. Rewrite the
  reasoning of `docs/findings/filtration.md` §6 point 3 and §7 around that, and restate Q-033 from
  "what is the number" to "what capability does the route demonstrate, and can the toxicology
  programme qualify what it leaves behind". F-014 and F-028 belong in the same edit; F-028 adds the
  caveat that purity multiplies only within one analytical dimension.
- **F-001** is the strongest external check on the thesis and it cuts against it. Both routes of the
  only named commercial practitioner end in HPLC purification of the siRNA itself. Land this in
  §7 and in the evidence-quality admonition, and register the new risk. Do **not** soften it, and do
  not conclude from it that the process should change. The honest statement is that the site is
  ahead of demonstrated practice at the final-purification step.

### Stage 3 — the balance and the parameter register

Do these together and re-run the balance once.

- **F-008**: per-ligation conversion and overall mass yield are different quantities, an order of
  magnitude apart. Split them into separate parameters. A balance that reads a per-ligation
  conversion as a step yield overstates output by roughly two to four times.
- **F-018**: `P-YLD-DRY` is a flat 90%. Measured dryer recoveries run 8.6% to 22% unoptimised and
  61% to 89% optimised. Replace the point value with a band and a sensitivity case.
- **F-019**: `P-YLD-UFDF` is not a constant. Loss is exponential in retention and in the combined
  concentration-and-diavolume term, with membrane adsorption as a second additive term and hold-up
  as a third. Hold-up dominates at small batch size and gets worse at plant scale. Add the hold-up
  term explicitly. Note the queue's honesty here: the source equation sits in a graphic that did not
  extract and was **not** reconstructed, so either derive it and show your working or keep the
  relationship qualitative and cite the worked points.
- `P-YLD-EVAP` remains wholly unsupported. Leave it as a flagged assumption against a question
  rather than inventing a basis for it.
- **F-012** and **F-013**: re-anchor `P-BLOCK-PUR` to the measured hectogram-scale block purities,
  and cite the independent validation of the purity-floor model. Two routes converge on the same
  floor from different directions, and that is the strongest quantitative support `EQ-PURITY` has.

After editing, `python -m pytest gen -q` must pass, including the test that solids close between the
evaporator and the dryer and the test that the balance refuses a blank input.

### Stage 4 — the drying and evaporation pages

- **F-003**: reorder the spray-drying finding so the glass transition leads and the melting
  temperature follows as the looser limit. The gap is 5 °C to 25 °C. Re-rank Q-039 above Q-030.
  Carry the warning that the per-modification temperature increment was measured over three
  positions and must not be extrapolated across twenty-one.
- **F-015**: retire atomisation shear as a governing risk for a short duplex and say why it is still
  a real risk for plasmid DNA.
- **F-024**: restate Q-021 from "what ratio does the molecule need" to "what ratio does the dryer
  need". Four of seven approved products carry no weighed excipient at all. State the transfer
  judgement: all seven are liquid injectables and no dried siRNA product has ever been approved.
- **F-009**: register the evaporator turndown risk. Minimum wetting rate sets a hard minimum feed per
  unit tube perimeter, a small batch must recirculate, and recirculation multiplies cumulative
  thermal exposure, which is what R-004 is about. A rotary evaporator is not a scale-down model of a
  falling film.

### Stage 5 — microbial control, water and the contamination control strategy

- **F-006**: replace the ladder with the oligonucleotide-specific figure, stated as what it is, a
  statement of practice with a case-by-case escape, not a pharmacopoeial limit and not a
  specification.
- **F-025**: **remove the endotoxin ladder rather than replacing it.** There is no compendial
  endotoxin ladder. The limit is calculated from dose, so it is a quantity per milligram of
  substance, not per millilitre of a process stream, and the current ladder is the wrong kind of
  quantity. Derive a limit from the intended dose instead, or leave it blank against a question.
- **F-026**: set the water grade per process step from the guideline's own table, and tie the choice
  to the requirement for an endotoxin specification on the substance.
- **F-027**: weaken the nuclease assertion to what is evidenced. Protection is positional, the
  evidence is serum challenge rather than a manufacturing hold, and the hold half of Q-031 stays
  open with the failed search recorded.
- **F-020**: state why a contamination control strategy is needed rather than inherited. The
  published low-bioburden argument has two premises and this process has neither.

### Stage 6 — ligation, blocks, development and technology transfer

F-004, F-010, F-011 and F-017 for the pages. F-019's mass-balance discipline and the scale-down
material belong on `docs/devel/`. The technology-transfer gaps the queue names are concrete: no
scale-up protocol, no hold-time protocols, no cleaning-validation master plan with health-based
exposure limits, no forced-degradation data, no side-by-side comparison of sending and receiving
units, no acceptance criteria for a successful transfer, no gap analysis.

### Stage 7 — new register entries

The queue's third call-out table lists new questions and risks not yet registered. Add them with
proper identifiers, continuing the existing numbering. The ones that look most exposed:

- Magnesium and calcium bind the polyanion and can block impurity clearance in diafiltration, and
  the ligation buffer contains magnesium chloride.
- No health-based exposure limit exists anywhere in the registers for cleaning validation of shared
  filtration and drying equipment.
- Dust explosion on the dryer, cyclone and receiver.
- Hold-time limits on the aqueous intermediates.
- In-line ultraviolet concentration measurement saturates on a 21-mer at process concentration.
- Q-032 should be restated from "not yet found" to "not publicly available". No ppm, log-reduction,
  immunoassay or total-protein figure for ligase clearance exists in any patent, paper or vendor
  document that the dive read, and it read the whole relevant patent estate.

## 6. Tests

Add guards; never weaken one. The suite currently has twenty-six tests and every one of them
encodes a defect that actually shipped. If an existing test fails because of something you did, fix
what you did.

Guards worth adding, in rough order of value:

- A parameter that is a range or a band must not be stored as a bare point value, or must carry its
  range explicitly. This is what F-018 and F-019 are really about.
- A transferability claim: any parameter whose source row's `scale_system` names a different
  molecule class must say so in its notes.
- The reverse of the existing reading-list guard: a source whose `access` is a full read must not
  still be sitting in the reading list's unread census.
- A check that no page states a residence time citing a source whose note says the figure is a batch
  cycle time. If that is too specific to encode, encode the general form: a numeric claim must not
  cite a source row whose notes contain the word TRAP for that figure.

## 7. Before you commit

- `python -m pytest gen -q` — all tests pass, including the ones you add.
- `python -m gen.build` — clean.
- `mkdocs build --strict` — clean.
- Re-read your own diff adversarially. Every number you added: does it have a source, a scale and a
  provenance flag? Every number you removed: is the gap registered as a question?
- Check that you have not created a claim the sources do not support. The dive's own worst moment was
  writing a contradiction against a paraphrase. Yours will be writing a conclusion against a
  quotation that is narrower than the conclusion.

Commit to this session's designated branch and push. Do not open a pull request unless asked. Do not
merge to `main`.

## 8. Report back in chat, not in the repository

- How many findings you applied, how many you retracted, and how many you deferred, with the
  identifiers in each group.
- What changed in the balance, and by how much the headline numbers moved.
- Which open questions you were able to close or re-scope on the register, and which you re-opened.
- Anything in the queue you found to be wrong, and what the page actually said.
- Anything you believe is still wrong on the site and did not fix, with the reason.

## 9. What good looks like

A reader who knew the site before should be able to see, from the diff alone, which conclusions
moved and why, with a quotation behind every change. Nothing you write should require them to take
your word for it. The site should end the session with fewer unsupported numbers than it started
with, and with its remaining gaps stated more plainly rather than filled in.
