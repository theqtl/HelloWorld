"""CSV loading helpers. Single source of truth = data/*.csv."""
import csv
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def load_rows(name):
    """Load data/<name>.csv as a list of dict rows."""
    path = os.path.join(DATA_DIR, name + ".csv")
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_params():
    """Return {param_id: row} for parameters.csv."""
    return {r["param_id"]: r for r in load_rows("parameters")}


def param_value(params, pid):
    """Float value of a parameter, or None if blank/unparseable.

    Never invents a value: a blank stays None so callers can flag a gap.
    """
    row = params.get(pid)
    if not row:
        return None
    raw = (row.get("value") or "").strip()
    if raw == "":
        return None
    try:
        return float(raw)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# `range_kind` says WHAT KIND OF CLAIM a band is. `range_low`/`range_high` say
# only how wide it is, which is not the same thing and was being conflated.
#
# Two of these are ICH's own terms and are used with ICH's meaning; three are
# this project's, because ICH has no term for them. Adopting ICH's word where
# ICH has one is deliberate: coining a synonym would imply a distinction the
# guidelines do not make. The mixed vocabulary is itself licensed - ICH
# Q8/Q9/Q10 Q&As (R5) Ch. 2.1 Q8: "The applicant may elect to use proven
# acceptable ranges or design space for different aspects of the manufacturing
# process."
# ---------------------------------------------------------------------------

#: The controlled vocabulary for parameters.range_kind. One value per row.
RANGE_KINDS = {
    # --- this project's terms, for things ICH does not name ---
    "evidence",        # the span over which someone, somewhere, has published a number.
                       # ICH has NO term for this. Its use is governed by ICH Q11 s3.2
                       # (prior knowledge): the relevance to this drug substance must be
                       # justified. Says what is KNOWN, not what is possible or permitted.
    "argued",          # bracketed by physical or chemical argument rather than measured.
                       # May legitimately carry no source at either endpoint - and must
                       # then say so. NOT a design space: ICH admits first principles INTO
                       # a design space (Q11 s3.1.6, Points to Consider s6.1), but only
                       # once the input-to-CQA relationship is demonstrated and the scale
                       # relevance justified. Neither holds here.
    "design_intent",   # a band this project commits to for SIZING. Ours, not ICH's, and
                       # deliberately not called a design space: nothing in this concept
                       # has been "demonstrated to provide assurance of quality".
    # --- ICH's terms, with ICH's meanings. Both are EMPTY today, and that is
    #     informative rather than an oversight: this concept contains no
    #     characterised range and no approved one. ---
    "proven_acceptable_range",  # ICH Q8(R2) Annex s4 Glossary: "A characterised range of
                       # a process parameter for which operation within this range, WHILE
                       # KEEPING OTHER PARAMETERS CONSTANT, will result in producing a
                       # material meeting relevant quality criteria." Univariate BY
                       # DEFINITION. A set of these is explicitly NOT a design space
                       # (Q8(R2) s2.4.5).
    "design_space",    # ICH Q8(R2) Part I s3 / Annex s4 Glossary, re-adopted for drug
                       # substance by ICH Q11 s3.1.6: "The multidimensional combination and
                       # interaction of input variables ... that have been DEMONSTRATED to
                       # provide assurance of quality ... proposed by the applicant and
                       # subject to regulatory assessment and approval."
}

#: Kinds that are ICH terms of art, so a row claiming one is making a regulatory
#: claim and not merely describing a spread.
RANGE_KINDS_ICH = frozenset({"proven_acceptable_range", "design_space"})


def param_range(params, pid):
    """(low, high, kind) for a parameter, or None if it carries no range.

    Mirrors param_value's contract: never invents anything, and a blank stays None so
    callers can flag a gap. Raises on an unknown kind rather than letting a typo render
    as a confident statement about the process - the same reason `access` and
    `clearance_model` raise.
    """
    row = params.get(pid)
    if not row:
        return None
    lo = (row.get("range_low") or "").strip()
    hi = (row.get("range_high") or "").strip()
    kind = (row.get("range_kind") or "").strip()
    if not (lo and hi):
        return None
    if kind not in RANGE_KINDS:
        raise ValueError(
            f"{pid}: range_kind {kind!r} is not in the controlled vocabulary; "
            f"expected one of {sorted(RANGE_KINDS)}"
        )
    try:
        return (float(lo), float(hi), kind)
    except ValueError:
        raise ValueError(f"{pid}: range_low/range_high are not numeric: {lo!r}, {hi!r}")


# ---------------------------------------------------------------------------
# THE TWO AXES THAT WERE ONE COLUMN.
#
# `provenance` answers "what kind of act produced this number?" - did someone
# read it out of a document, derive it here, or park a placeholder. That is a
# question about THIS PROJECT's relationship to the figure.
#
# `envelopes.endpoint_sourcing` answers a different question: "what standing do
# the two ENDPOINTS have as retrieved claims?" - a question about the literature,
# answered without reference to what this project then does with the band.
#
# Both columns were called `provenance` and eleven envelope rows consequently
# read as flat contradictions of `parameters.csv`: ENV-001/002/003/007/008/009/
# 010/012/014/015/016 say `fact` or `inference` where the parameter they audit
# says `assumption`. Verified by reproduction, 2026-09-27: eleven rows, every one
# disagreeing in the same direction. None of them was a data error. `P-BLOCK-PUR`
# is the clearest case - ENV-001's endpoints ARE published measurements (a fact
# about the record) while the value this project carries for the parameter IS an
# assumption (a fact about this project), and both statements are true at once.
#
# So the columns are separated rather than reconciled. They share three tokens
# today and that is a coincidence of history, not a shared vocabulary: keeping
# them as two constants is what stops a value added to one axis becoming
# silently legal on the other.
# ---------------------------------------------------------------------------

#: The controlled vocabulary for the `provenance` column, wherever it appears.
#: One value per row. Lived in gen/test_balance.py until slice 4: a vocabulary
#: that only a test knows cannot raise at build time, and three of the eleven
#: registers carrying the column were never checked against it at all.
PROVENANCE_VOCAB = {
    "fact",        # read out of a cited document. Must carry a source_key.
    "inference",   # derived here, by arithmetic or argument, from things that are cited.
    "assumption",  # an illustrative placeholder the model needs in order to run at all,
                   # registered as a gap. Says nothing about what the real value is.
    "judgement",   # an EDUCATED ESTIMATE: a number this project is prepared to defend on
                   # stated grounds, while admitting that no document states it. Added in
                   # slice 4 because one word - `assumption` - was covering two unlike
                   # things. `P-EVAP-T-BOIL` = 50 degrees C is an illustrative placeholder
                   # the balance needs in order to run at all; `P-EPS-260` = 20-25 mL/mg/cm
                   # is bracketed from A260 conversions plus hypochromicity by someone who
                   # can say why. Calling both `assumption` told a reader that the second
                   # was as arbitrary as the first, and calling either `inference` would
                   # have claimed a derivation from cited things that neither has.
                   #
                   # THREE OBLIGATIONS TRAVEL WITH IT, and all three are guarded, because a
                   # provenance that is merely nicer to write is how a placeholder gets
                   # promoted for free:
                   #   1. the number goes in `est_value`, NEVER in the register's own value
                   #      column - so the balance is PHYSICALLY unable to consume it
                   #      (`param_value` reads `value`), and "an estimate never closes its
                   #      question" is structural rather than a promise;
                   #   2. `basis` says on what grounds, resolving its own SRC-/P-/EQ-/Q-
                   #      tokens, and may not rest on a source nobody here has read;
                   #   3. `falsifier` says what observation would show the estimate wrong.
                   # See ESTIMATE_REGISTERS for where it is legal at all.
}

#: The controlled vocabulary for `envelopes.endpoint_sourcing` - deliberately a
#: SEPARATE constant from PROVENANCE_VOCAB even though the tokens coincide. See
#: the note above.
ENDPOINT_SOURCING = {
    "fact",        # both endpoints are figures printed in a retrieved document.
    "inference",   # at least one endpoint is bracketed here rather than quoted.
    "assumption",  # the endpoints are this project's own choice of span.
}

#: Registers carrying a `provenance` column, with the column that names a row.
#: `envelopes` is absent on purpose: it carries `endpoint_sourcing` instead.
PROVENANCE_REGISTERS = (
    ("buffers", "buffer_id"),
    ("controls", "control_id"),
    ("couplings", "coupling_id"),
    ("equipment", "equip_id"),
    ("impurities", "impurity_id"),
    ("infoneeds", "need_id"),
    ("instruments", "instrument_id"),
    ("parameters", "param_id"),
    ("scenarios", "scenario_id"),
    ("utilities", "utility_id"),
    ("verdicts", "verdict_id"),
)

# ---------------------------------------------------------------------------
# WHERE AN EDUCATED ESTIMATE MAY LIVE, and why the answer is three registers and
# not eleven.
#
# The acceptance panel's second blocker was that the guards for this feature were
# written against `parameters.csv` while the estimates it exists for land in
# `buffers.csv` - so the rows the feature was built for escaped every check.
# Scoping the columns to "wherever this slice happens to put a number" would
# repeat that defect one slice later, so the line is drawn on a property of the
# register instead:
#
#   AN ESTIMATE MAY LIVE WHERE THE ROW CARRIES A QUANTITY OF ITS OWN - one that
#   cannot be referenced out to `parameters.csv` without putting a number in two
#   places.
#
# Three registers qualify, and the reason differs in each:
#   * `parameters` - the register that exists for numbers.
#   * `buffers`    - a composition is a RECIPE. Splitting `Tris-HCl 50 mM; KCl
#                    100 mM; MgCl2 10 mM; DTT 1 mM` into four parameters would put
#                    one buffer in four rows and let them drift apart.
#   * `scenarios`  - a scenario's demand and campaign count ARE the scenario;
#                    `gen/balance.py:132-133` reads them off the row directly.
#
# The other eight provenance-carrying registers state no quantity of their own -
# verified column by column: they carry ids, controlled-vocabulary values and
# prose, and where they need a number they REFERENCE one (`controls.param_ref`,
# `infoneeds.satisfied_by`, `envelopes.param_id`). `equipment.turndown` looks like
# a counter-example and is not: all seven rows state a turndown BASIS in prose with
# the numeric ratio explicitly pending. An estimate in any of them would be a
# second home for a number, which is the defect `instruments.csv` has no
# `control_loop` column in order to avoid. So `judgement` is REFUSED there, by
# guard, rather than merely unused.
# ---------------------------------------------------------------------------

#: The provenance value that carries an educated estimate. Named once, because three
#: modules and two test files have to agree on it.
ESTIMATE_PROVENANCE = "judgement"

#: The three columns an estimate needs, on every register where one is legal.
#: `est_value` is deliberately NOT `value`: see the note on ESTIMATE_PROVENANCE's
#: first obligation.
ESTIMATE_COLUMNS = ("est_value", "basis", "falsifier")

#: {register: the value columns an estimate may NOT write}. The keys are the registers
#: where `judgement` is legal; the values are the quantity columns that must stay BLANK
#: on an estimate row, which is what makes the balance unable to consume one.
ESTIMATE_REGISTERS = {
    "parameters": ("value",),
    "buffers": ("components", "ph"),
    "scenarios": ("annual_ds_demand_kg_yr", "campaigns_per_yr"),
}

#: The controlled vocabulary for `questions.status`. Free text until slice 4, which is
#: why it needs one now: an estimate must name the question it does NOT close, and that
#: obligation is empty if the question's state cannot be read mechanically.
QUESTION_STATUS = {
    "open",                # nobody here has answered it.
    "partially_resolved",  # part of it is settled and the rest is not. Five rows today.
    "resolved",            # EMPTY today, and informative rather than an oversight: this
                           # register has never closed a question. The eighteen ids missing
                           # from the Q-001..Q-070 sequence were never issued, not retired.
}

#: Access grades meaning NOBODY HERE HAS READ THE DOCUMENT. An estimate's basis may not
#: rest on one of these, because "we estimated it on the strength of a paper we did not
#: read" is the citation defect the source register was built to stop, wearing the new
#: provenance as cover.
#:
#: `redacted` and `partial-text-read` are deliberately NOT here, and the reason is worth
#: stating: the four `redacted` rows are EPARs and FDA chemistry reviews that WERE read,
#: with the numbers blacked out. A regulator publishing an assessment with the figure
#: removed is precisely the condition that makes an estimate necessary, so citing it as a
#: basis is honest - it is what happened.
ACCESS_GRADES_UNREAD = frozenset({"abstract-only", "record-only", "not-retrieved"})


def question_status_offenders():
    """Rows of questions.csv whose `status` is outside QUESTION_STATUS."""
    return [
        f"questions.csv {r.get('question_id')}: status {(r.get('status') or '').strip()!r} is not "
        f"in the controlled vocabulary; expected one of {sorted(QUESTION_STATUS)}"
        for r in load_rows("questions")
        if (r.get("status") or "").strip() not in QUESTION_STATUS
    ]


def provenance_offenders():
    """Rows whose `provenance` is outside PROVENANCE_VOCAB, across every register.

    Enforced everywhere rather than on the three registers a test happened to reach, for the
    reason every other vocabulary here is enforced: a misspelling does not fail, it renders as a
    confident statement about how well a number is known.
    """
    problems = []
    for name, id_col in PROVENANCE_REGISTERS:
        for r in load_rows(name):
            value = (r.get("provenance") or "").strip()
            if value not in PROVENANCE_VOCAB:
                problems.append(
                    f"{name}.csv {r.get(id_col)}: provenance {value!r} is not in the controlled "
                    f"vocabulary; expected one of {sorted(PROVENANCE_VOCAB)}")
    for r in load_rows("envelopes"):
        value = (r.get("endpoint_sourcing") or "").strip()
        if value not in ENDPOINT_SOURCING:
            problems.append(
                f"envelopes.csv {r.get('envelope_id')}: endpoint_sourcing {value!r} is not in the "
                f"controlled vocabulary; expected one of {sorted(ENDPOINT_SOURCING)}")
    return problems


# ---------------------------------------------------------------------------
# Vocabularies relocated here in slice 4. Each was a module constant somewhere a
# consumer could not reach it: BRACKET_VERDICTS and DISPOSITIONS lived in the
# RENDERER, so the vocabulary was owned by the thing that draws the page rather
# than by the thing that loads the data, and RISK_UNIT_OPS lived in the TEST
# FILE, so nothing raised at build time and the only enforcement was a guard
# re-listing its own expectation.
# ---------------------------------------------------------------------------

#: What the two endpoints of a band ACTUALLY are. This is the column slice 3 exists for: a width
#: says how far apart two numbers are and says nothing about whether they are two claims or one.
BRACKET_VERDICTS = {
    "two_independent",              # two endpoints citing two DIFFERENT sources. The only verdict
                                    # under which a band is a band without qualification.
    "one_source_both_ends",         # both endpoints citing the SAME source. NOT automatically
                                    # refused - a band may still be the honest summary of what one
                                    # study found - but the register has to disclose it.
    "no_source_either_end",         # neither endpoint cites a source, because neither is a citation:
                                    # the span is bracketed by argument, or it is a choice this
                                    # project is making. Legitimate, and must not be dressed up as
                                    # anything else.
    "measurement_plus_unverifiable",  # one endpoint verified against its document, one whose
                                    # document could not be re-read. Carried and labelled, never
                                    # presented as two measurements.
    "not_a_range",                  # the two ends are different KINDS of claim - a success and a
                                    # failure, or two bases with a switched denominator - so no width
                                    # between them is a window of operation. A parameter with this
                                    # verdict must carry NO range of that kind in parameters.csv and
                                    # NO value either, and `range_written_where_refused` and
                                    # `value_written_where_refused` enforce the two halves.
    "single_point",                 # one endpoint only, in this branch's own units: low == high. The
                                    # per-branch enzyme loadings are this, because their units do not
                                    # convert into one another at all.
}
# WHY THIS COLUMN ASKS EXACTLY ONE QUESTION. An earlier version of this vocabulary carried a
# `measurement_plus_argument` value, and the acceptance panel caught it labelling two rows that have
# no measured endpoint at all - `P-EPS-260`, which states "NO SOURCE AT EITHER END, by construction",
# and the evaporator's `design_intent` band, whose endpoints are explicitly ours and not measured. The
# fault was structural rather than clerical: that value mixed "how many independent citations do the
# endpoints have" with "is this band measured or argued", and the second question is ALREADY answered
# by `range_kind` (evidence versus argued versus design_intent). One column, one question - so every
# verdict below is now checkable against the row's own data, which is what let the guard find nothing
# wrong before.

#: Verdicts under which a numeric interval may be published as a range at all.
BRACKET_VERDICTS_RANGEABLE = frozenset(BRACKET_VERDICTS - {"not_a_range", "single_point"})

#: How an information requirement is currently answered. The four-way split.
DISPOSITIONS = {
    "bracketed_evidence",   # answered by a band whose endpoints are published measurements
    "bracketed_argument",   # answered by a band bracketed from physical or chemical argument
    "point_justified",      # answered by ONE value, with a stated reason why no range is needed.
                            # A bare point value is a claim that the variable does not matter, and
                            # that claim needs defending - so `point_argument` may not be blank.
    "not_knowable",         # cannot be answered from the public record at all
}

#: Controlled vocabulary for risks.csv. Neither column was enforced before slice 3's guard, so a
#: new risk row could ship an invalid unit_op or category silently and simply never be found by
#: anyone filtering the register. Moved out of the test file in slice 4 so the vocabulary is owned
#: by the data layer. NOTE the limit this does not fix: `unit_op` here is free text that resolves
#: to no `equip_id`, so `Ligation` and the equipment register's `Enzymatic ligation` are different
#: strings for one unit operation and `Utilities` is absent from this set entirely.
RISK_UNIT_OPS = {"All", "Cleaning", "Evaporation", "Filtration", "Ligation",
                 "Spray drying", "UF/DF"}
RISK_CATEGORIES = {"formulation", "microbial", "process", "product", "purity", "quality"}
