"""Mutation tests: every guard here is proven against a FAILING case, not just a passing one.

A green suite says nothing about whether a guard can see the defect it claims to guard. The
only proof is to introduce the defect and watch the guard fail. Slice 2 did this with a
throwaway script that was never committed, so the claim could not be re-checked; this module
is that harness made permanent.

Three design rules, each a reaction to a specific hazard:

1. MUTATE A COPY, NEVER THE TREE. `data/` is copied to a pytest tmp_path and
   `gen.dataio.DATA_DIR` is pointed at the copy. `load_rows` resolves that global at call
   time, so every guard reached through it reads the copy. The working tree is never
   written to at all - so an interrupted run cannot leave a mutated CSV behind, which a
   snapshot-and-restore harness can. (Slice 2's harness snapshotted bytes; that was already
   a deliberate improvement on `git checkout --`, which would silently revert uncommitted
   work. Not touching the tree is better still.)

2. ANCHOR EVERY MUTATION ON A ROW ID, never on a field value. Row order is not guaranteed
   and a field value like `,at_line,` is not unique.

3. ASSERT THE GUARD RAISES. A mutation case that passes is a guard that is blind.

Guards that read `ROOT/data` directly rather than through `load_rows` - the CRLF and
field-count guards - cannot be redirected this way and are not covered here; that limit is
stated rather than hidden.
"""
import csv
import io
import os
import shutil

import pytest

from gen.dataio import DATA_DIR as REAL_DATA_DIR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: CSVs that are CRLF on disk. The copy must keep each file's own endings, or a mutation
#: would also be testing a line-ending change and the failure would be ambiguous.
_LF_ONLY = {"streams.csv", "scenarios.csv"}


def _rewrite(path, row_id_col, row_id, fields):
    """Set `fields` on the one row whose `row_id_col` is `row_id`. Preserves endings."""
    raw = open(path, "rb").read()
    rows = list(csv.reader(io.StringIO(raw.decode("utf-8")), strict=True))
    header, body = rows[0], rows[1:]
    idx = header.index(row_id_col)
    hit = 0
    for r in body:
        if r[idx] != row_id:
            continue
        hit += 1
        for col, value in fields.items():
            r[header.index(col)] = value
    assert hit == 1, f"expected exactly 1 row with {row_id_col}={row_id!r}, found {hit}"
    terminator = "\n" if os.path.basename(path) in _LF_ONLY else "\r\n"
    buf = io.StringIO()
    csv.writer(buf, quoting=csv.QUOTE_MINIMAL, lineterminator=terminator).writerows(
        [header] + body)
    open(path, "wb").write(buf.getvalue().encode("utf-8"))


@pytest.fixture
def mutate(tmp_path, monkeypatch):
    """Return a function that mutates one row of one CSV in an isolated copy of data/."""
    copy = tmp_path / "data"
    shutil.copytree(REAL_DATA_DIR, copy)
    monkeypatch.setattr("gen.dataio.DATA_DIR", str(copy))

    def _apply(csv_name, row_id_col, row_id, **fields):
        _rewrite(str(copy / (csv_name + ".csv")), row_id_col, row_id, fields)

    return _apply


def test_the_harness_does_not_touch_the_working_tree(mutate):
    """The harness's own premise, checked: mutating must not write to data/."""
    before = {n: open(os.path.join(REAL_DATA_DIR, n), "rb").read()
              for n in sorted(os.listdir(REAL_DATA_DIR)) if n.endswith(".csv")}
    mutate("parameters", "param_id", "P-DS-TM", range_kind="")
    after = {n: open(os.path.join(REAL_DATA_DIR, n), "rb").read()
             for n in sorted(os.listdir(REAL_DATA_DIR)) if n.endswith(".csv")}
    assert before == after, "the mutation harness wrote to the real data/ directory"


def test_the_harness_mutation_is_actually_visible(mutate):
    """And the other half: the mutation must reach the code under test."""
    from gen.dataio import load_params
    mutate("parameters", "param_id", "P-DS-TM", range_kind="")
    assert (load_params()["P-DS-TM"].get("range_kind") or "") == "", (
        "the mutation did not reach load_params - DATA_DIR redirection is not working, so "
        "every mutation case below would be vacuously green")


# ---------------------------------------------------------------------------
# test_band_parameters_carry_an_explicit_range
#
# The direction that matters is the one the REPLACED guard could not see: a row that
# carries a range but is not flagged as a band. P-YIELD-OVERALL-PUB was exactly that
# defect in the live tree, undetected, because the old guard classified on the 'BAND:'
# prose token and only ever checked 'flagged but unranged'.
# ---------------------------------------------------------------------------

def test_mutation_a_range_without_a_kind_is_caught(mutate):
    """THE case the old guard was blind to. If this passes, nothing has been fixed."""
    from gen.test_balance import test_band_parameters_carry_an_explicit_range as guard
    mutate("parameters", "param_id", "P-DS-TM", range_kind="")
    with pytest.raises(AssertionError, match="no range_kind"):
        guard()


def test_mutation_a_kind_without_a_range_is_caught(mutate):
    """The reverse direction: a kind describing nothing."""
    from gen.test_balance import test_band_parameters_carry_an_explicit_range as guard
    mutate("parameters", "param_id", "P-MW-NT", range_kind="evidence")
    with pytest.raises(AssertionError, match="carries no range"):
        guard()


def test_mutation_an_unknown_kind_is_caught(mutate):
    """A typo must not render as a confident statement about the process."""
    from gen.test_balance import test_band_parameters_carry_an_explicit_range as guard
    mutate("parameters", "param_id", "P-DS-TM", range_kind="evidenece")
    with pytest.raises(AssertionError, match="outside"):
        guard()


def test_mutation_a_half_range_is_caught(mutate):
    from gen.test_balance import test_band_parameters_carry_an_explicit_range as guard
    mutate("parameters", "param_id", "P-DS-TM", range_high="")
    with pytest.raises(AssertionError, match="only one of"):
        guard()


def test_mutation_an_inverted_range_is_caught(mutate):
    from gen.test_balance import test_band_parameters_carry_an_explicit_range as guard
    mutate("parameters", "param_id", "P-DS-TM", range_low="99")
    with pytest.raises(AssertionError, match="range_low"):
        guard()


def test_mutation_a_value_outside_its_range_is_caught(mutate):
    from gen.test_balance import test_band_parameters_carry_an_explicit_range as guard
    mutate("parameters", "param_id", "P-EVAP-T-BOIL", value="99")
    with pytest.raises(AssertionError, match="outside its range"):
        guard()


def test_mutation_a_non_numeric_bound_reports_rather_than_raises(mutate):
    """The old guard called float() unguarded, so a bad bound raised ValueError instead of
    reporting an offender. The rewrite must report it as a band defect."""
    from gen.test_balance import test_band_parameters_carry_an_explicit_range as guard
    mutate("parameters", "param_id", "P-DS-TM", range_low="about 58")
    with pytest.raises(AssertionError, match="not numeric"):
        guard()


def test_mutation_prose_claiming_an_unbacked_band_is_caught(mutate):
    """The one direction the legacy prose token is still policed in."""
    from gen.test_balance import test_band_parameters_carry_an_explicit_range as guard
    mutate("parameters", "param_id", "P-MW-NT", notes="BAND: 300-360 Da across sources")
    with pytest.raises(AssertionError, match="flag a BAND"):
        guard()


# ---------------------------------------------------------------------------
# test_an_ich_range_kind_is_not_claimed_without_demonstration
#
# Both ICH kinds are empty in the register, so this guard has no live row and is proven
# ONLY by mutation - the same standing as `not_measurable` in gen/controls.py. These two
# cases are the entirety of its evidence, which is why they are here.
# ---------------------------------------------------------------------------

def test_mutation_an_assumption_promoted_to_a_design_space_is_caught(mutate):
    """P-EVAP-T-BOIL is an assumption placeholder. Calling it a design space is the
    ISA-conformance over-claim in a different register."""
    from gen.test_balance import (
        test_an_ich_range_kind_is_not_claimed_without_demonstration as guard)
    mutate("parameters", "param_id", "P-EVAP-T-BOIL", range_kind="design_space")
    with pytest.raises(AssertionError, match="cannot rest on an assumption"):
        guard()


def test_mutation_an_unsourced_proven_acceptable_range_is_caught(mutate):
    """A PAR is a range WE characterised. One with no source names no such work."""
    from gen.test_balance import (
        test_an_ich_range_kind_is_not_claimed_without_demonstration as guard)
    mutate("parameters", "param_id", "P-EVAP-T-BOIL",
           range_kind="proven_acceptable_range", provenance="fact", source_key="")
    with pytest.raises(AssertionError, match="no source_key"):
        guard()


# ---------------------------------------------------------------------------
# test_a_partial_read_says_what_was_read
#
# The value `partial-text-read` is only an improvement on over-claiming if it states its
# extent. Without this guard it is `full-text-read` with a softer name.
# ---------------------------------------------------------------------------

def test_mutation_a_partial_read_without_an_extent_is_caught(mutate):
    from gen.test_balance import test_a_partial_read_says_what_was_read as guard
    mutate("sources", "source_key", "SRC-ALMAC-2023",
           access="partial-text-read", notes="read some of it", verified="checked")
    with pytest.raises(AssertionError, match="which part was read"):
        guard()


def test_mutation_a_partial_read_with_a_section_list_passes(mutate):
    """The other half: a row that DOES state its extent must not be refused. A guard that
    rejects the honest case as well as the dishonest one would just push everyone back to
    `full-text-read`."""
    from gen.test_balance import test_a_partial_read_says_what_was_read as guard
    mutate("sources", "source_key", "SRC-ALMAC-2023",
           access="partial-text-read",
           notes="Sections 4.2.2 and 4.3.2 read; 15 of 27 pages.", verified="")
    guard()


def test_mutation_the_access_vocabulary_still_refuses_a_typo(mutate):
    """Adding a value to a controlled vocabulary must not loosen it."""
    from gen.test_balance import test_access_values_are_in_the_controlled_vocabulary as guard
    mutate("sources", "source_key", "SRC-ALMAC-2023", access="partial-read")
    with pytest.raises(AssertionError, match="controlled vocabulary"):
        guard()


# ---------------------------------------------------------------------------
# test_purity_floor_defaults_to_the_registered_block_purity
#
# The guard used to hardcode the exponent as 3, so it agreed with the code only while the
# register happened to say 3. Now it reads P-N-BLOCKS. The mutation that proves the
# difference is moving the block count: the old form would have passed.
# ---------------------------------------------------------------------------

def test_mutation_the_purity_floor_guard_follows_the_registered_block_count(mutate):
    """Move P-N-BLOCKS and the guard must still agree with the code.

    This is the POSITIVE case, and it is the whole point: with the exponent hardcoded at 3
    this guard failed on a register that legitimately said 2. Passing here proves it now
    tracks the register instead of a literal.
    """
    from gen.test_balance import (
        test_purity_floor_defaults_to_the_registered_block_purity as guard)
    mutate("parameters", "param_id", "P-N-BLOCKS", value="2")
    guard()


def test_mutation_a_blank_block_count_is_caught(mutate):
    """purity_floor() reads both inputs, so a blank must be reported, not silently defaulted."""
    from gen.test_balance import (
        test_purity_floor_defaults_to_the_registered_block_purity as guard)
    mutate("parameters", "param_id", "P-N-BLOCKS", value="")
    with pytest.raises(AssertionError, match="must both carry values"):
        guard()


def test_mutation_the_floor_moves_with_the_corrected_block_purity(mutate):
    """The correction from the misread 92 to the measured 93.6 must actually reach the floor.

    Guards the specific defect this slice fixed: a yield read as a purity. If the floor did
    not move when P-BLOCK-PUR moved, the register and the published ceiling would be
    decoupled and the correction would be cosmetic.
    """
    from gen.balance import purity_floor
    before = purity_floor()
    mutate("parameters", "param_id", "P-BLOCK-PUR", value="92")
    after = purity_floor()
    assert after < before, (
        f"purity_floor did not follow P-BLOCK-PUR: {before:.2f}% -> {after:.2f}%")
    assert abs(before - 82.0) < 0.05, f"corrected floor should be 82.0%, got {before:.2f}%"
    assert abs(after - 77.87) < 0.05, f"the old misread gave 77.87%, got {after:.2f}%"


# ---------------------------------------------------------------------------
# Tier-3 slice 3: the four new registers.
#
# `gen/envelope.py` raises ValueError with EVERY problem it found rather than the first, so each
# case below asserts on the phrase belonging to the guard it is proving. Several of these guards
# check a row against ITS OWN data rather than against a vocabulary, and those are the ones worth
# having: the acceptance panel found two envelope rows whose verdict claimed a measured endpoint
# their own notes denied, and a vocabulary check could never have seen it.
# ---------------------------------------------------------------------------

def _validate():
    from gen.envelope import validate
    return validate


def test_mutation_an_unknown_bracket_verdict_is_caught(mutate):
    mutate("envelopes", "envelope_id", "ENV-003", bracket_verdict="two_indepedent")
    with pytest.raises(ValueError, match="not in the controlled vocabulary"):
        _validate()()


def test_mutation_two_independent_endpoints_citing_one_source_is_caught(mutate):
    """THE case the whole register exists for, in the direction that flatters a band.

    A range whose ends came from one document, labelled as two independent ones, is the defect
    `P-BLOCK-PUR` shipped with. If this passes, the register has a verdict column and no teeth.
    """
    mutate("envelopes", "envelope_id", "ENV-003", high_source_key="SRC-HONGENE-BROCHURE-2025")
    with pytest.raises(ValueError, match="verdict contradicts its own data"):
        _validate()()


def test_mutation_one_source_both_ends_citing_two_is_caught(mutate):
    """And the opposite direction, because a one-directional guard ships the other one."""
    mutate("envelopes", "envelope_id", "ENV-001", high_source_key="SRC-KELLY-OPRD-2025")
    with pytest.raises(ValueError, match="ONE named source at both ends"):
        _validate()()


def test_mutation_a_sourceless_verdict_carrying_a_source_is_caught(mutate):
    """The hole the acceptance panel walked through, now closed.

    `P-EPS-260` is bracketed by argument and says so - "NO SOURCE AT EITHER END, by construction".
    A verdict on that row that implies a citation overstates the standing of the band which decides
    the in-line/at-line question, and the first version of this register did exactly that.
    """
    mutate("envelopes", "envelope_id", "ENV-012", low_source_key="SRC-MALEK-2019")
    with pytest.raises(ValueError, match="must not carry a citation"):
        _validate()()


def test_mutation_a_single_point_spanning_an_interval_is_caught(mutate):
    """The per-branch enzyme loadings are points in incommensurable units, not bands."""
    mutate("envelopes", "envelope_id", "ENV-007", high="2")
    with pytest.raises(ValueError, match="a point that spans an interval is a band"):
        _validate()()


def test_mutation_an_ich_range_kind_in_the_envelope_register_is_caught(mutate):
    """Both ICH kinds are empty by design, and the emptiness has to be defended in BOTH registers.

    gen/test_balance.py guards parameters.csv. Without this case, envelopes.csv would be a second
    door into the same over-claim - which is how the ISA claim survived one directory away.
    """
    mutate("envelopes", "envelope_id", "ENV-013", range_kind="design_space")
    with pytest.raises(ValueError, match="is an ICH term of art"):
        _validate()()


def test_mutation_an_unresolvable_endpoint_source_is_caught(mutate):
    mutate("envelopes", "envelope_id", "ENV-005", high_source_key="SRC-NOT-A-SOURCE")
    with pytest.raises(ValueError, match="is not in the source register"):
        _validate()()


def test_mutation_an_endpoint_driving_nothing_that_exists_is_caught(mutate):
    """An endpoint that sizes nothing is a literature note; one that sizes a thing which does not
    exist is worse, because it reads as a link to the plant."""
    mutate("envelopes", "envelope_id", "ENV-005", high_drives_ref="UT-NOPE")
    with pytest.raises(ValueError, match="resolves to no equipment"):
        _validate()()


def test_mutation_a_refused_bracket_written_as_a_range_is_caught(mutate):
    """The user's standing rule, proven: a `not_a_range` span must not appear as a range.

    Mutating the PARAMETER rather than the envelope, because that is the direction the defect comes
    from - someone fills in a band because the two numbers are sitting there.
    """
    from gen.envelope import range_written_where_refused
    mutate("parameters", "param_id", "P-LIG-SEG-CONC",
           range_low="1.5", range_high="10", range_kind="evidence")
    offenders = range_written_where_refused()
    assert offenders, (
        "range_written_where_refused did not see a not_a_range span written as a range in "
        "parameters.csv - the standing rule is unenforced")
    assert "P-LIG-SEG-CONC" in offenders[0]


def test_mutation_a_band_losing_its_endpoint_audit_is_caught(mutate):
    """Every number a reader can use off parameters.csv must have an audit saying whose claims its
    two ends are. Proven by moving an envelope row off its parameter."""
    from gen.envelope import unaudited_bands
    mutate("envelopes", "envelope_id", "ENV-010", param_id="P-MW-NT")
    offenders = unaudited_bands()
    assert offenders and any("P-DS-TM" in o for o in offenders), (
        f"unaudited_bands missed a band with no audit: {offenders}")


def test_mutation_a_design_intent_band_over_an_unreachable_corner_is_caught(mutate):
    """The inscribed-box rule, and it has NO live row - this case is its entire evidence.

    Points a coupling that declares its corner unreachable at the one parameter carrying a
    `design_intent` band, so both sides of the corner are design intent and the pair asserts
    operation where nobody has operated.
    """
    from gen.envelope import corner_rule_offenders
    mutate("couplings", "coupling_id", "CPL-005",
           param_a="P-EVAP-T-BOIL", param_b="P-EVAP-T-BOIL")
    offenders = corner_rule_offenders()
    assert offenders, (
        "corner_rule_offenders did not see a design_intent band spanning a corner declared "
        "unreachable - the only guard in the slice with no live row is blind")
    assert "CPL-005" in offenders[0]


def test_mutation_an_unknown_coupling_vocabulary_is_caught(mutate):
    mutate("couplings", "coupling_id", "CPL-001", corner_reachable="maybe")
    with pytest.raises(ValueError, match="corner_reachable"):
        _validate()()


def test_mutation_a_point_value_with_no_argument_is_caught(mutate):
    """A bare point value is a claim that the variable does not matter, and that claim needs
    defending in writing. This is the guard that makes the four-way split mean something."""
    mutate("infoneeds", "need_id", "IN-002", point_argument="")
    with pytest.raises(ValueError, match="bare point"):
        _validate()()


def test_mutation_an_argument_for_a_point_that_is_not_there_is_caught(mutate):
    """The reverse: an argument on a row carrying no point value will be read as justifying one."""
    mutate("infoneeds", "need_id", "IN-003",
           point_argument="25 C is fine because both examples agreed")
    with pytest.raises(ValueError, match="justifying something it does not"):
        _validate()()


def test_mutation_an_anchor_clause_nobody_read_is_caught(mutate):
    """THE defect the acceptance panel found in this slice: four rows cited an ICH Q11 "s4.3" that
    does not exist, and 105 green tests never resolved a clause against its document.

    The guard couples the two registers - a clause an information need cites must appear in its
    source row's `clauses_read` - so a fabricated section number now fails the build.

    Note the clause used here. "s4.3" is the exact string the panel found, and it is also the string
    that defeated the FIRST version of this guard: that version searched the source's prose, and the
    corrective sentence added to SRC-ICH-Q11 ("there is no s4.1, s4.2 or s4.3 to cite") contains it,
    so the guard found the clause and passed. Keeping "s4.3" here is deliberate - it is the one input
    that proves the check is reading the delimited field and not the prose.
    """
    mutate("infoneeds", "need_id", "IN-001", anchor_clause="s4.3")
    with pytest.raises(ValueError, match="clauses_read does not list it"):
        _validate()()


def test_mutation_an_unknown_disposition_or_anchor_strength_is_caught(mutate):
    mutate("infoneeds", "need_id", "IN-005", disposition="unknowable")
    with pytest.raises(ValueError, match="not in the controlled vocabulary"):
        _validate()()


def test_mutation_an_anchor_strength_typo_is_caught(mutate):
    mutate("infoneeds", "need_id", "IN-005", anchor_strength="generic-anchor")
    with pytest.raises(ValueError, match="anchor_strength"):
        _validate()()


def test_mutation_a_blocker_that_is_not_a_registered_question_is_caught(mutate):
    """A reviewer's binding blocker has to be something this repository already tracks, or the panel
    is generating new work rather than judging the register it was handed."""
    mutate("verdicts", "verdict_id", "V-001", blocker_ref="Q-999")
    with pytest.raises(ValueError, match="not a registered question id"):
        _validate()()


def test_mutation_a_verdict_outside_accept_reject_is_caught(mutate):
    """Deliberately binary and deliberately not averaged."""
    mutate("verdicts", "verdict_id", "V-002", verdict="ACCEPT_WITH_COMMENTS")
    with pytest.raises(ValueError, match="verdict"):
        _validate()()


def test_mutation_a_verdict_that_cannot_be_moved_is_caught(mutate):
    mutate("verdicts", "verdict_id", "V-003", what_would_change_it="")
    with pytest.raises(ValueError, match="cannot be moved"):
        _validate()()


def test_mutation_a_page_claiming_the_panel_signed_off_is_caught(tmp_path):
    """The honesty sweep, proven both ways.

    Not routed through the CSV harness: this guard sweeps published pages, so its mutation is a
    page. Both directions matter - a guard that only catches the false claim would be satisfied by
    deleting the disclaimer, and a guard that refuses the disclaimer creates pressure to do exactly
    that.
    """
    from gen.envelope import signoff_claim_offenders
    bad = tmp_path / "bad.md"
    bad.write_text(
        "# Concept\n"
        "This package has been reviewed by a licensed professional engineer.\n"
        "The panel has approved the concept for construction.\n",
        encoding="utf-8")
    offenders = signoff_claim_offenders([str(bad)])
    assert len(offenders) == 2, f"the sweep missed a sign-off claim: {offenders}"

    good = tmp_path / "good.md"
    good.write_text(
        "# Concept\n"
        "These are four role-based reviews this project ran itself.\n"
        "They are **not** a design review by licensed engineers and approve nothing.\n"
        "Nothing here has been reviewed or approved by a qualified person or a regulator.\n",
        encoding="utf-8")
    assert not signoff_claim_offenders([str(good)]), (
        "the sweep refused an honest disclaimer, which would push a writer to delete it")


def test_mutation_the_purity_sensitivity_follows_the_registered_block_count(mutate):
    """The published ceiling moves with the register, so the sensitivity that discloses it must too.

    The acceptance panel's process reviewer made this table the condition of acceptance: an
    exclusion whose cost is not shown is indistinguishable from one made because it flatters the
    route. If the table were typed in rather than computed, it would go stale the moment anyone
    moved the block count - which is the defect the data layer exists to prevent.
    """
    from gen.envelope import purity_ceiling_sensitivity
    n3, rows3 = purity_ceiling_sensitivity()
    assert n3 == "3"
    mutate("parameters", "param_id", "P-N-BLOCKS", value="2")
    n2, rows2 = purity_ceiling_sensitivity()
    assert n2 == "2", "the sensitivity table did not follow P-N-BLOCKS"
    key3 = [k for k in rows3[0] if k.startswith("DS full-length ceiling")][0]
    key2 = [k for k in rows2[0] if k.startswith("DS full-length ceiling")][0]
    assert key3 != key2, "the column header must name the block count it was computed at"
    # Fewer ligations, so fewer blocks compounding: every ceiling must rise.
    for a, b in zip(rows3, rows2):
        lo = float(a[key3].strip("* %"))
        hi = float(b[key2].strip("* %"))
        assert hi > lo, f"ceiling did not rise when the block count fell: {lo} -> {hi}"


# ---------------------------------------------------------------------------
# test_every_data_csv_is_published_somewhere
#
# This guard globs the REAL data/ directory rather than going through load_rows, so the
# DATA_DIR redirection cannot reach it - the same limit the module docstring records for the
# CRLF and field-count guards. What can be mutated is the guard's own declaration of which
# CSVs are published elsewhere, and that is where its logic lives: the exemption must be
# EARNED by the generator's output, not granted by appearing in a list.
#
# All three fields of an entry are mutated, because all three can lie independently: the
# page it claims, the generator it names, and the column it says that generator prints.
# ---------------------------------------------------------------------------

def test_mutation_an_undeclared_csv_with_no_register_page_is_caught(monkeypatch):
    """Drop an exemption and the CSV becomes invisible data, which must fail.

    Stands in for the real defect: four CSVs were committed, guarded and read by the
    generator while no page showed them.
    """
    import gen.test_balance as tb
    monkeypatch.setattr(tb, "_PUBLISHED_ELSEWHERE",
                        {k: v for k, v in tb._PUBLISHED_ELSEWHERE.items() if k != "impurities"})
    with pytest.raises(AssertionError, match="no register spec"):
        tb.test_every_data_csv_is_published_somewhere()


def test_mutation_an_unearned_exemption_is_caught(monkeypatch):
    """Claiming publication of a column the generator does not print must fail.

    This is the half that caught a real error while being written: the declaration first
    named `impurity_id`, and the overlay renders impurities by NAME, so the exemption was
    being asserted rather than demonstrated.
    """
    import gen.test_balance as tb
    monkeypatch.setattr(tb, "_PUBLISHED_ELSEWHERE",
                        dict(tb._PUBLISHED_ELSEWHERE,
                             impurities=("balance/impurities.md", "render_impurities",
                                         "impurity_id")))
    with pytest.raises(AssertionError, match="exemption is not earned"):
        tb.test_every_data_csv_is_published_somewhere()


def test_mutation_a_generator_that_reaches_no_page_is_caught(monkeypatch):
    """A generator that renders text gen/build.py never writes publishes nothing.

    The page path is the half of the claim the generator itself cannot evidence: calling it
    proves the rows are rendered, not that any reader sees them.
    """
    import gen.test_balance as tb
    monkeypatch.setattr(tb, "_PUBLISHED_ELSEWHERE",
                        dict(tb._PUBLISHED_ELSEWHERE,
                             impurities=("balance/nonexistent-page.md", "render_impurities",
                                         "name")))
    with pytest.raises(AssertionError, match="does not write that page"):
        tb.test_every_data_csv_is_published_somewhere()


def test_mutation_an_exemption_naming_a_missing_generator_is_caught(monkeypatch):
    import gen.test_balance as tb
    monkeypatch.setattr(tb, "_PUBLISHED_ELSEWHERE",
                        dict(tb._PUBLISHED_ELSEWHERE,
                             impurities=("balance/impurities.md", "render_nothing", "name")))
    with pytest.raises(AssertionError, match="does not define"):
        tb.test_every_data_csv_is_published_somewhere()


def test_mutation_the_publication_guard_reads_the_generator_not_the_built_page(tmp_path,
                                                                              monkeypatch):
    """The guard must pass with no built pages on disk at all.

    Its first version checked `os.path.exists(docs/<page>)`. Those pages are generated and
    gitignored, so it passed on a machine that had just run the build and failed in CI, where
    pytest runs first. Point DOCS at an empty directory: nothing is written there, and the
    guard must still reach its verdict from the generators.
    """
    import gen.build as build
    import gen.test_balance as tb
    monkeypatch.setattr(build, "DOCS", str(tmp_path / "docs"))
    assert not os.path.exists(os.path.join(str(tmp_path / "docs"), "balance", "results.md"))
    tb.test_every_data_csv_is_published_somewhere()
    assert not os.path.exists(str(tmp_path / "docs")), (
        "the guard wrote a page - it must render in memory, not build into the docs tree")


# ---------------------------------------------------------------------------
# Reachability: the nav bijection, the orphan-page rule, the access legend
#
# These three guards read mkdocs.yml, gen/build.py and docs/ directly, so DATA_DIR
# redirection cannot reach them. What is mutated instead is the derived set each one
# compares - which is where the logic is - and the vocabulary constant the legend is
# checked against.
# ---------------------------------------------------------------------------

def test_mutation_a_page_missing_from_the_nav_is_caught(monkeypatch):
    """Drop a nav entry and its page becomes reachable only by search, which must fail."""
    import gen.test_balance as tb
    real = tb._nav_pages()
    victim = "process/ligation-envelope.md"
    assert victim in real, "the fixture page is no longer in the nav; pick another"
    monkeypatch.setattr(tb, "_nav_pages", lambda: real - {victim})
    with pytest.raises(AssertionError, match="no mkdocs.yml nav entry lists them"):
        tb.test_every_page_is_in_the_nav_and_every_nav_entry_is_a_real_page()


def test_mutation_a_nav_entry_with_no_page_behind_it_is_caught(monkeypatch):
    """A sidebar row pointing at nothing must fail here, not at mkdocs build time."""
    import gen.test_balance as tb
    real = tb._nav_pages()
    monkeypatch.setattr(tb, "_nav_pages", lambda: real | {"process/not-a-page.md"})
    with pytest.raises(AssertionError, match="nothing writes and no file provides"):
        tb.test_every_page_is_in_the_nav_and_every_nav_entry_is_a_real_page()


def test_mutation_a_generated_page_nothing_links_to_is_caught(monkeypatch):
    """The real defect, reproduced: a page correctly built and linked from nowhere.

    Declaring a page generated is the faithful mutation, because the orphan that prompted this
    guard was generated and unlinked. The ADR is the fixture: it is hand-written and, correctly,
    no page links to it.
    """
    import gen.test_balance as tb
    real = tb._generated_pages()
    orphan = "adr/0001-information-architecture.md"
    monkeypatch.setattr(tb, "_generated_pages", lambda: real | {orphan})
    with pytest.raises(AssertionError, match="reachable only from the sidebar"):
        tb.test_every_generated_page_is_linked_from_a_hand_written_page()


def test_mutation_an_access_label_absent_from_the_legend_is_caught(monkeypatch):
    """Exactly the defect found: a vocabulary value the legend does not explain."""
    import gen.test_balance as tb
    monkeypatch.setattr(tb, "ACCESS_VOCAB", set(tb.ACCESS_VOCAB) | {"skim-read"})
    with pytest.raises(AssertionError, match="absent from the reading-list legend"):
        tb.test_the_access_legend_covers_the_whole_vocabulary()


def test_mutation_a_legend_label_outside_the_vocabulary_is_caught(monkeypatch):
    """The other direction: a legend row left behind after a value was retired."""
    import gen.test_balance as tb
    monkeypatch.setattr(tb, "ACCESS_VOCAB",
                        {v for v in tb.ACCESS_VOCAB if v != "partial-text-read"})
    with pytest.raises(AssertionError, match="not in ACCESS_VOCAB"):
        tb.test_the_access_legend_covers_the_whole_vocabulary()


# ---------------------------------------------------------------------------
# Slice 4 phase 0: the two provenance axes, and the vocabularies that moved.
# ---------------------------------------------------------------------------

def test_mutation_a_bad_provenance_in_buffers_is_caught(mutate):
    """`buffers.csv` was one of eight registers whose `provenance` nothing checked.

    It is the register slice 4's estimates land in, so it is the one worth proving first. Before
    this guard a misspelling here validated, and the row rendered as a confident statement about
    how well a buffer composition is known.
    """
    mutate("buffers", "buffer_id", "BUF-DF", provenance="assumtpion")
    with pytest.raises(ValueError, match="buffers.csv BUF-DF: provenance"):
        _validate()()


def test_mutation_a_bad_provenance_in_equipment_is_caught(mutate):
    """A second unchecked register, to prove the guard is not buffers-specific."""
    mutate("equipment", "equip_id", "U01-LIG", provenance="guess")
    with pytest.raises(ValueError, match="equipment.csv U01-LIG: provenance"):
        _validate()()


def test_mutation_a_bad_endpoint_sourcing_is_caught(mutate):
    """The renamed column is enforced under its new name."""
    mutate("envelopes", "envelope_id", "ENV-011", endpoint_sourcing="facts")
    with pytest.raises(ValueError, match="ENV-011: endpoint_sourcing"):
        _validate()()


def test_mutation_a_blank_endpoint_sourcing_is_caught(mutate):
    """Blank is not a legal value on either axis.

    Worth its own case because the rename went through a state where the column did not exist
    and every row read blank - so "the guard fires on a typo" and "the guard fires when the
    column is gone" are different claims and only one of them was proved by the case above.
    """
    mutate("envelopes", "envelope_id", "ENV-011", endpoint_sourcing="")
    with pytest.raises(ValueError, match="ENV-011: endpoint_sourcing ''"):
        _validate()()


def test_mutation_re_adding_provenance_to_envelopes_is_caught(monkeypatch, tmp_path):
    """The rename made permanent: a `provenance` column back on `envelopes.csv` must fail.

    Anchored on the HEADER rather than on a row id, because that is what the defect is - so this
    case writes a header instead of using the `mutate` fixture, which rewrites one row.
    """
    import shutil
    copy = tmp_path / "data"
    shutil.copytree(REAL_DATA_DIR, copy)
    path = copy / "envelopes.csv"
    raw = open(path, "rb").read()
    head, sep, rest = raw.partition(b"\r\n")
    assert b"endpoint_sourcing" in head
    open(path, "wb").write(head.replace(b"endpoint_sourcing", b"provenance") + sep + rest)
    monkeypatch.setattr("gen.dataio.DATA_DIR", str(copy))
    import gen.test_balance as tb
    with pytest.raises(AssertionError, match="carries a `provenance` column again"):
        tb.test_the_two_provenance_axes_are_separate_columns()


def test_mutation_a_bad_risk_unit_op_is_caught_against_the_imported_vocabulary(mutate):
    """The risk vocabulary moved out of the test file; the guard must still see a bad value.

    The move was the point in phase 0: the guard imports the vocabulary from `gen/dataio.py` rather
    than declaring it three lines above itself. Phase 4 went further and made it `risk_unit_ops()`,
    derived from equipment.csv - see
    test_mutation_the_risk_vocabulary_follows_equipment_rather_than_a_frozen_list, which is the case
    that proves the derivation. This one still covers the plain typo, which is the failure a
    derived vocabulary does nothing about.
    """
    mutate("risks", "risk_id", "R-001", unit_op="Ligaton")
    import gen.test_balance as tb
    with pytest.raises(AssertionError, match="outside the vocabulary"):
        tb.test_risk_unit_op_and_category_are_a_controlled_vocabulary()


# ---------------------------------------------------------------------------
# test_a_refused_bracket_is_not_written_as_a_value_either
#
# This is the one mutation in the file that reproduces a defect found by exploiting it
# rather than by reading the code. A red team set P-LIG-SEG-CONC.value = 5 with its
# provenance untouched and the whole suite stayed green (155 passed at the time) while
# `python -m gen.build` published the fabricated number on the register page. The three
# cases below pin the fix and, just as importantly, pin its LIMITS - the rule deliberately
# still permits a sourced single point, so a guard that rejected everything would be wrong.
# ---------------------------------------------------------------------------

def test_mutation_a_fabricated_value_on_a_refused_bracket_is_caught(mutate):
    """The red team's exact reproduction. It must now fail.

    `P-LIG-SEG-CONC` is blank because ENV-006 rules its span `not_a_range`: the low end is a
    demonstrated success and the high end a reported failure, so no width between them is a
    window of operation. An `assumption` value here is a plausible-looking number in the one
    place the register has argued at length that no number is available.
    """
    import gen.test_balance as tb
    mutate("parameters", "param_id", "P-LIG-SEG-CONC", value="5")
    with pytest.raises(AssertionError, match="rules the span not_a_range"):
        tb.test_a_refused_bracket_is_not_written_as_a_value_either()


def test_mutation_a_sourced_single_point_on_a_refused_bracket_is_allowed(mutate):
    """The limit of the rule, which matters as much as the rule.

    The policy `range_written_where_refused` states allows "a blank or a clearly-labelled single
    point". So a value that someone has actually measured or derived, and that cites where it came
    from, must PASS - otherwise the guard would forbid the register from ever recording that the
    question got answered.
    """
    import gen.test_balance as tb
    mutate("parameters", "param_id", "P-LIG-SEG-CONC",
           value="5", provenance="fact", source_key="SRC-ALMAC-2023")
    tb.test_a_refused_bracket_is_not_written_as_a_value_either()


def test_mutation_a_sourceless_fact_on_a_refused_bracket_is_caught(mutate):
    """`fact` alone does not buy a value - the source is what makes the point checkable.

    Without this case the guard could be satisfied by relabelling a fabricated number `fact`,
    which is a one-word edit.
    """
    import gen.test_balance as tb
    mutate("parameters", "param_id", "P-LIG-SEG-CONC",
           value="5", provenance="fact", source_key="")
    with pytest.raises(AssertionError, match="with no source"):
        tb.test_a_refused_bracket_is_not_written_as_a_value_either()


# ---------------------------------------------------------------------------
# test_every_buffer_reference_resolves_and_every_buffer_is_referenced
#
# First mutation coverage of buffers.csv in the file's history - the harness had none,
# which is why three separate buffer guards could be absent without anyone noticing.
# ---------------------------------------------------------------------------

def test_mutation_a_dangling_buffer_reference_is_caught(mutate):
    """A typo'd buffer id renders as a confident cross-reference to nothing."""
    import gen.test_balance as tb
    mutate("impurities", "impurity_id", "IMP-DIVALENT",
           notes="Enters with the ligation buffer, which carries MgCl2 (BUF-LIGG).")
    with pytest.raises(AssertionError, match="undefined buffer"):
        tb.test_every_buffer_reference_resolves_and_every_buffer_is_referenced()


def test_mutation_a_buffer_nothing_references_is_caught(mutate):
    """The other direction: a solution registered for a process that does not use it.

    Reaching this limb takes care, and the first attempt at this case was wrong in a way the guard
    itself caught. Renaming the buffer id looks like the faithful mutation, but it trips the
    DANGLING limb first - every citing register still names the old id - and the guard asserts
    dangling before orphan, so the orphan branch never ran. The mutation has to create an orphan
    WITHOUT creating a dangling token, which means silencing the citation rather than renaming the
    row. `BUF-DF` is cited exactly once in the whole data layer, by `streams.csv` S06, which makes
    it the only buffer this case can be built on.
    """
    import gen.test_balance as tb
    mutate("streams", "stream_id", "S06",
           notes="Final DV must exchange into a spray-dryable matrix (excipient choice is Q-038).")
    with pytest.raises(AssertionError, match="no other register names"):
        tb.test_every_buffer_reference_resolves_and_every_buffer_is_referenced()


def test_mutation_a_buffer_source_key_typo_is_caught(mutate):
    """buffers was absent from the source-key sweep until slice 4.

    Nothing in CI resolved it; the only guard that would have reads the RENDERED page, which CI
    never builds before pytest.
    """
    import gen.test_balance as tb
    mutate("buffers", "buffer_id", "BUF-LIG", source_key="SRC-ALMAC-2023-TYPO")
    with pytest.raises(AssertionError, match="unknown source_key|source_key"):
        tb.test_all_source_keys_resolve()


# ---------------------------------------------------------------------------
# Slice 4 phase 2: the fourth provenance.
#
# `judgement` is a nicer word than `assumption` and it is available for one edit, so the
# split only improves the register if the new label is HARDER to earn. Every obligation
# below is therefore proved against a failing case, and two cases prove the LIMITS -
# a legitimate estimate must pass, and a legitimate estimate must be marked. A guard
# that refused everything would be as wrong as one that refused nothing.
#
# `P-LIG-SEG-CONC` is the fixture throughout, for the reason phase 1 used it: it is the
# register's most carefully argued deliberate blank, so an estimate landing there is the
# most tempting shape this defect can take.
# ---------------------------------------------------------------------------

#: A fully legitimate estimate. Every failing case below is this dict with one thing wrong,
#: so the failure is attributable to that one thing and not to a second defect further down.
_GOOD_ESTIMATE = dict(
    provenance="judgement",
    value="",
    est_value="0.5",
    basis=("Bracketed from the segment concentrations in SRC-ALMAC-2023 against P-LIG-T; "
           "leaves Q-064 open."),
    falsifier="A measured segment concentration from a kilogram-scale campaign.",
)


def _estimate(**overrides):
    return {**_GOOD_ESTIMATE, **overrides}


def test_mutation_a_legitimate_estimate_is_accepted(mutate):
    """The limit of the rule, and the case that matters most.

    Nothing in the repository carries this provenance yet, so every other case here proves the
    guard can refuse. This one proves it can also ACCEPT - without it the whole feature could be
    satisfied by a guard that rejects the fourth provenance outright, and the suite would be green.
    """
    mutate("parameters", "param_id", "P-LIG-SEG-CONC", **_estimate())
    _validate()()


def test_mutation_an_estimate_that_writes_the_value_column_is_caught(mutate):
    """THE case the whole design rests on.

    An estimate in `value` is consumable by gen/balance.py, and the moment one is, "an estimate
    never closes its question" becomes a promise rather than a property. This is also the shape
    the old vocabulary could not refuse at all: relabelling the red team's fabricated
    `P-LIG-SEG-CONC` value from `assumption` to `judgement` must not buy it a home.
    """
    mutate("parameters", "param_id", "P-LIG-SEG-CONC", **_estimate(value="5"))
    with pytest.raises(ValueError, match="an estimate wrote value='5'"):
        _validate()()


def test_mutation_the_balance_still_refuses_an_estimate_as_an_input(mutate):
    """The structural claim, proved by running the balance rather than by reading the code.

    `P-DF-DIAVOL` is `_require`d at gen/balance.py:105. Turn it into a correctly-formed estimate -
    number moved to `est_value`, basis and falsifier stated, everything the guard asks for - and the
    balance must still refuse to run. Not because a guard forbids it: because `param_value` reads
    `value`, finds a blank, and `_require` raises. That is the difference between a rule and a
    property, and it is the one claim in this phase that no amount of reading the CSV could
    establish.

    The first draft of this case used `P-LIG-CONV`, which reads like a balance input and is not -
    `used_by` says `analysis`, and gen/impurity.py is what consumes it. The case passed nothing and
    proved nothing, and the fix was to pick the fixture off `used_by` rather than off its name.
    """
    from gen.balance import run_all
    mutate("parameters", "param_id", "P-DF-DIAVOL",
           **_estimate(est_value="7",
                       basis="Bracketed from the diafiltration data in SRC-ALMAC-2023; leaves "
                             "Q-020 open.",
                       falsifier="A measured residual at a stated diavolume count for this duplex."))
    with pytest.raises(ValueError, match="P-DF-DIAVOL is blank"):
        run_all()


def test_mutation_an_estimate_with_no_basis_is_caught(mutate):
    """Without the basis, `judgement` and `assumption` are one word again with two spellings."""
    mutate("parameters", "param_id", "P-LIG-SEG-CONC", **_estimate(basis=""))
    with pytest.raises(ValueError, match="with a blank basis"):
        _validate()()


def test_mutation_an_estimate_with_no_falsifier_is_caught(mutate):
    """An estimate no observation could contradict is an opinion wearing a number."""
    mutate("parameters", "param_id", "P-LIG-SEG-CONC", **_estimate(falsifier=""))
    with pytest.raises(ValueError, match="with a blank falsifier"):
        _validate()()


def test_mutation_an_estimate_with_no_number_is_caught(mutate):
    """A basis and a falsifier with nothing between them is a gap, and a gap is registered as one."""
    mutate("parameters", "param_id", "P-LIG-SEG-CONC", **_estimate(est_value=""))
    with pytest.raises(ValueError, match="with a blank est_value"):
        _validate()()


def test_mutation_a_basis_citing_a_source_that_does_not_exist_is_caught(mutate):
    """A defence resting on a reference that resolves to nothing is resting on nothing.

    The same defect class as the fabricated ICH Q11 "s4.3" the acceptance panel found: a citation
    that looks like one and is not, which passed every gate because nothing resolved it.
    """
    mutate("parameters", "param_id", "P-LIG-SEG-CONC",
           **_estimate(basis="Bracketed from SRC-ALMAC-2023-TYPO; leaves Q-064 open."))
    with pytest.raises(ValueError, match="basis cites SRC-ALMAC-2023-TYPO, which resolves to "
                                        "nothing"):
        _validate()()


def test_mutation_a_basis_citing_a_parameter_that_does_not_exist_is_caught(mutate):
    """A second token shape, because one resolving shape does not prove the other three."""
    mutate("parameters", "param_id", "P-LIG-SEG-CONC",
           **_estimate(basis="Bracketed against P-LIG-TEMPERATURE; leaves Q-064 open."))
    with pytest.raises(ValueError, match="basis cites P-LIG-TEMPERATURE"):
        _validate()()


def test_mutation_a_basis_citing_an_equation_that_does_not_exist_is_caught(mutate):
    """`EQ-` resolves against the equations page's own headings, via gen/envelope.equation_ids()."""
    mutate("parameters", "param_id", "P-LIG-SEG-CONC",
           **_estimate(basis="Bracketed via EQ-SEGMENT; leaves Q-064 open."))
    with pytest.raises(ValueError, match="basis cites EQ-SEGMENT"):
        _validate()()


def test_mutation_an_estimate_resting_on_an_unread_document_is_caught(mutate):
    """The laundering case, and the reason this guard exists at all.

    "Estimated on the strength of" a paper nobody here opened is the 2026-09-17 citation defect
    with a better label on it. `SRC-ISO-10628-1` is `not-retrieved` - paywalled, never obtained -
    so it cannot support anything.
    """
    mutate("parameters", "param_id", "P-LIG-SEG-CONC",
           **_estimate(basis="Bracketed from SRC-ISO-10628-1; leaves Q-064 open."))
    with pytest.raises(ValueError, match="graded 'not-retrieved' - nobody here has read it"):
        _validate()()


def test_mutation_an_estimate_may_rest_on_a_redacted_document(mutate):
    """The deliberate carve-out, which is a limit and not an oversight.

    The four `redacted` sources are EPARs and FDA chemistry reviews that WERE read with the numbers
    blacked out. A regulator publishing an assessment with the figure removed is precisely what
    makes an estimate necessary, so citing it is honest - it is what happened. Refusing it would
    push the true basis into free text where nothing resolves it.
    """
    mutate("parameters", "param_id", "P-LIG-SEG-CONC",
           **_estimate(basis="Bracketed from SRC-FDA-OXLUMO-CHEMR; leaves Q-064 open."))
    _validate()()


def test_mutation_an_estimate_naming_no_open_question_is_caught(mutate):
    """An estimate that names no question reads as having closed one."""
    mutate("parameters", "param_id", "P-LIG-SEG-CONC",
           **_estimate(basis="Bracketed from SRC-ALMAC-2023 against P-LIG-T."))
    with pytest.raises(ValueError, match="basis names no Q- question"):
        _validate()()


def test_mutation_an_estimate_naming_a_closed_question_is_caught(mutate):
    """`Q-017` is `partially_resolved`, so it is the fixture no test has to invent.

    Either the estimate closed the question - in which case it is not an estimate - or the question
    register is wrong. Both are defects and the guard does not have to choose between them.
    """
    mutate("parameters", "param_id", "P-LIG-SEG-CONC",
           **_estimate(basis="Bracketed from SRC-ALMAC-2023; leaves Q-017 open."))
    with pytest.raises(ValueError, match="status is 'partially_resolved'"):
        _validate()()


def test_mutation_the_fourth_provenance_outside_its_registers_is_caught(mutate):
    """`judgement` is refused where the row states no quantity of its own.

    `utilities` is the fixture: it carries `provenance` and its columns are `driven_by` and
    `scenario_dependent` - nothing numeric. An estimate there would have no `est_value` to live in
    and no basis column to defend it, so the label would promise a defence that has nowhere to go.
    """
    mutate("utilities", "utility_id", "UT-WFI", provenance="judgement")
    with pytest.raises(ValueError, match="is not legal in this register"):
        _validate()()


def test_mutation_an_estimate_column_on_a_row_that_is_not_an_estimate_is_caught(mutate):
    """The converse direction: a number with the label's benefits and none of its obligations.

    Same reasoning as `infoneeds.point_argument`, which may not be populated on a row carrying no
    point value - an argument attached to the wrong thing will be read as justifying it.
    """
    mutate("parameters", "param_id", "P-LIG-T", est_value="37")
    with pytest.raises(ValueError, match="est_value is populated on a 'assumption' row"):
        _validate()()


def test_mutation_a_basis_on_a_row_that_is_not_an_estimate_is_caught(mutate):
    """A second column of the three, because one proved column does not prove the other two."""
    mutate("parameters", "param_id", "P-LIG-T",
           basis="Bracketed from SRC-ALMAC-2023; leaves Q-010 open.")
    with pytest.raises(ValueError, match="basis is populated on a 'assumption' row"):
        _validate()()


def test_mutation_an_estimate_in_buffers_may_not_touch_the_composition(mutate):
    """`buffers` is the register the feature exists for, so the rule is proved there too.

    The panel's second blocker was that phase 2's guards covered `parameters.csv` while the
    estimates land here - the rows the feature was built for escaped every check. A buffer's
    quantity columns are `components` and `ph`, and an estimate may write neither.
    """
    mutate("buffers", "buffer_id", "BUF-DF", provenance="judgement", ph="7.0",
           est_value="Tris 20 mM", basis="From SRC-ALMAC-2023; leaves Q-038 open.",
           falsifier="A vendor-stated or measured composition for this step.")
    with pytest.raises(ValueError, match="an estimate wrote ph='7.0'"):
        _validate()()


def test_mutation_an_estimate_in_scenarios_may_not_touch_the_demand(mutate):
    """The third estimate register, and the one whose numbers gen/balance.py reads off the row.

    `annual_ds_demand_kg_yr` and `campaigns_per_yr` are read at gen/balance.py:132-133 rather than
    through `param_value`, so this is a second path by which an estimate could reach a computed
    figure, and it needs its own case.
    """
    mutate("scenarios", "scenario_id", "S1", provenance="judgement", est_value="250",
           basis="From SRC-ALMAC-2023; leaves Q-002 open.",
           falsifier="A published or commercially confirmed annual demand.")
    with pytest.raises(ValueError, match="an estimate wrote annual_ds_demand_kg_yr"):
        _validate()()


def test_mutation_a_question_status_typo_is_caught(mutate):
    """`questions.status` was free text until this slice made it load-bearing.

    An estimate must name a question that is still `open`, and that check is worth nothing if
    `opne` validates - the status would simply never equal `open` and every estimate would be
    refused for the wrong reason.
    """
    mutate("questions", "question_id", "Q-064", status="opne")
    with pytest.raises(ValueError, match="Q-064: status 'opne'"):
        _validate()()


# --- Visibility: the cell marker and the census ------------------------------
#
# These read gen/build.py and docs/ rather than only the CSVs, so two of them monkeypatch the
# derived value instead of redirecting DATA_DIR - the idiom the nav and legend cases use above.

def test_mutation_a_legitimate_estimate_is_marked_in_its_cell(mutate):
    """The positive case, and without it the marker guard is vacuous.

    No row carries this provenance today, so `test_an_estimate_is_marked_in_the_cell_where_the
    _number_is_read` currently iterates nothing and passes. This case supplies the row and asserts
    the marker really appears - the panel's first blocker was invisibility, and a green suite over
    zero rows is exactly how invisibility survives.
    """
    import gen.test_balance as tb
    from gen.build import _with_provenance_markers, ESTIMATE_CELL_MARKER, VALUE_CELL_MARKER
    from gen.dataio import load_rows
    mutate("parameters", "param_id", "P-LIG-SEG-CONC", **_estimate())
    raw = {r["param_id"]: r for r in load_rows("parameters")}
    marked = {r["param_id"]: r
              for r in _with_provenance_markers(load_rows("parameters"), "parameters")}
    row = marked["P-LIG-SEG-CONC"]
    assert row["est_value"] == f"0.5 {ESTIMATE_CELL_MARKER}", row["est_value"]
    assert row["value"] == VALUE_CELL_MARKER, row["value"]
    # Every other row must come through untouched, compared against the register rather than
    # against a value typed here. The first draft of this case asserted `P-LIG-T` equals "37";
    # it is 25, so the case failed for a reason that had nothing to do with the transform. That
    # is harness rule 2 - anchor on a row id, never on a field value - and it applies to the
    # assertion as much as to the mutation.
    untouched = {pid: r for pid, r in marked.items() if pid != "P-LIG-SEG-CONC"}
    assert all(r["value"] == raw[pid]["value"] for pid, r in untouched.items()), (
        "the transform changed a row that is not an estimate")
    tb.test_an_estimate_is_marked_in_the_cell_where_the_number_is_read()


def test_mutation_an_estimate_rendering_as_a_bare_blank_is_caught(mutate):
    """The defect the marker exists to stop, reached through the data.

    A `judgement` row whose value column is populated cannot be marked - the transform will not
    overwrite a number - so the guard must see it. That is the same row state
    `test_mutation_an_estimate_that_writes_the_value_column_is_caught` refuses at validate time;
    proving BOTH guards see it is the point, because the visibility guard has to hold even if the
    validator is ever relaxed.
    """
    import gen.test_balance as tb
    mutate("parameters", "param_id", "P-LIG-SEG-CONC", **_estimate(value="5"))
    with pytest.raises(AssertionError, match="must not render as an unfilled gap"):
        tb.test_an_estimate_is_marked_in_the_cell_where_the_number_is_read()


def test_mutation_an_estimate_marker_on_a_row_that_is_not_one_is_caught(mutate):
    """The other direction: a marker claiming a defence nobody wrote.

    Reached by planting the marker text in the CSV itself, which is the faithful mutation - the
    marker is Markdown, so nothing stops a register row from containing it verbatim.
    """
    import gen.test_balance as tb
    from gen.build import VALUE_CELL_MARKER
    mutate("parameters", "param_id", "P-LIG-T", value=VALUE_CELL_MARKER)
    with pytest.raises(AssertionError, match="carries an estimate marker on a 'assumption' row"):
        tb.test_an_estimate_is_marked_in_the_cell_where_the_number_is_read()


def test_mutation_an_estimate_register_rendered_without_the_transform_is_caught(monkeypatch,
                                                                               tmp_path):
    """A transform nothing calls is dead code a guard can still prove correct.

    Mutates gen/build.py's SOURCE, because that is what the wiring guard reads - and it reads the
    source rather than the built page for the reason the publication guard does: the pages are
    gitignored and CI runs pytest first.
    """
    import gen.test_balance as tb
    src = open(os.path.join(ROOT, "gen", "build.py"), encoding="utf-8").read()
    doctored = src.replace("        if name in ESTIMATE_REGISTERS:\n"
                           "            rows = _with_provenance_markers(rows, name)\n", "")
    assert doctored != src, "the wiring this case removes is no longer in gen/build.py"
    (tmp_path / "gen").mkdir()
    (tmp_path / "gen" / "build.py").write_text(doctored, encoding="utf-8")
    monkeypatch.setattr(tb, "ROOT", str(tmp_path))
    with pytest.raises(AssertionError, match="must apply _with_provenance_markers"):
        tb.test_the_marker_transform_is_wired_into_every_estimate_register()


def test_mutation_a_numeric_reader_that_falls_back_to_the_estimate_is_caught(monkeypatch,
                                                                            tmp_path):
    """The structural property, checked from the other side, and in the place it would really break.

    `test_mutation_the_balance_still_refuses_an_estimate_as_an_input` proves the numeric path refuses
    an estimate TODAY. This proves the guard would notice somebody making it read one - and the
    mutation is written against `param_value` in gen/dataio.py rather than against gen/balance.py,
    because that is the accessor every consumer goes through. A one-line fallback there hands an
    estimate to the balance, the impurity overlay and the envelope page at once while balance.py
    itself still reads `value`, which is exactly the hole a balance-only guard would have left.
    """
    import gen.test_balance as tb
    (tmp_path / "gen").mkdir()
    for name in tb._NUMERIC_READERS:
        src = open(os.path.join(ROOT, "gen", name), encoding="utf-8").read()
        if name == "dataio.py":
            doctored = src.replace(
                '    raw = (row.get("value") or "").strip()\n',
                '    raw = (row.get("value") or "").strip()\n'
                '    raw = raw or (row.get("est_value") or "").strip()\n')
            assert doctored != src, "param_value no longer has the line this case mutates"
            src = doctored
        (tmp_path / "gen" / name).write_text(src, encoding="utf-8")
    monkeypatch.setattr(tb, "ROOT", str(tmp_path))
    with pytest.raises(AssertionError, match="gen/dataio.py reads est_value"):
        tb.test_no_numeric_reader_consumes_an_estimate()


def test_mutation_an_estimate_reaches_the_census_page(mutate):
    """The census claims to list every estimate in the repository, so a real one must appear.

    Vacuous today for the same reason the marker guard is - no row carries the provenance - and this
    case is what makes it real. It asserts the RENDERED page carries the basis and the falsifier,
    not merely that a census row exists: for a `scenarios` estimate this page is the only place a
    reader could ever see either, since that register has no register page at all.
    """
    import gen.test_balance as tb
    from gen.build import render_estimates
    mutate("parameters", "param_id", "P-LIG-SEG-CONC", **_estimate())
    page = render_estimates()
    assert "P-LIG-SEG-CONC" in page
    assert "leaves Q-064 open" in page
    assert "kilogram-scale campaign" in page
    assert "_No rows._" not in page
    tb.test_every_estimate_reaches_the_census()


def test_mutation_a_provenance_value_absent_from_the_legend_is_caught(monkeypatch):
    """Exactly the defect this phase found: a vocabulary the legend does not explain.

    The `prov-*` chips were hand-written prose and the vocabulary was a Python constant, with
    nothing relating the two - so the legend had gone three values deep and would have stayed there.
    """
    import gen.test_balance as tb
    monkeypatch.setattr(tb, "PROVENANCE_VOCAB", set(tb.PROVENANCE_VOCAB) | {"hunch"})
    with pytest.raises(AssertionError, match="absent from the docs/index.md legend"):
        tb.test_the_provenance_legend_covers_the_whole_vocabulary()


def test_mutation_a_legend_chip_outside_the_vocabulary_is_caught(monkeypatch):
    """The other direction: a legend entry left behind after a value was retired."""
    import gen.test_balance as tb
    monkeypatch.setattr(tb, "PROVENANCE_VOCAB",
                        {v for v in tb.PROVENANCE_VOCAB if v != "judgement"})
    with pytest.raises(AssertionError, match="not in PROVENANCE_VOCAB"):
        tb.test_the_provenance_legend_covers_the_whole_vocabulary()


def test_mutation_an_estimated_quantity_with_no_parameter_named_is_caught(monkeypatch, tmp_path):
    """The rule the plan asked for: the chip does not satisfy `_CITATION` on its own.

    Writes a page making exactly the claim the rule refuses - a quantity labelled as an educated
    estimate with nothing naming the row that carries its basis - and proves the guard sees it.

    THE FIXTURE USES `mM` AND NOT A PERCENTAGE. That began as a way around a defect in the guard
    this one rides on: `_QUANTITY` ended its unit alternation with `\b`, a word boundary after `%`
    requires a WORD character next, and so `0.5%`, `0.5 %.` and `0.5% of` all failed to match.
    PHASE 3 CORRECTED THAT - `%` now sits on its own branch with no boundary assertion, and
    `test_mutation_a_bare_percentage_with_no_citation_is_caught` holds the correction in place. The
    count registered here was seven prose lines across THREE pages, not four; all seven were judged
    individually and one of them was carrying a block-purity band `Q-011` had already retracted.
    The fixture stays on `mM` anyway, because this case is about the estimate chip and not about
    which units `_QUANTITY` recognises, and it should not fail for an unrelated reason.
    """
    import gen.test_balance as tb
    page = tmp_path / "estimated.md"
    page.write_text(
        "# A page\n\n"
        "The wash runs at <span class=\"prov-judgement\">judgement</span> 125 mM caustic.\n",
        encoding="utf-8")
    monkeypatch.setattr(tb, "_doc_files", lambda: [str(page)])
    with pytest.raises(AssertionError, match="flagged as an educated estimate with no parameter"):
        tb.test_an_estimated_quantity_in_prose_names_the_parameter_it_estimates()


def test_mutation_an_estimated_quantity_naming_its_parameter_passes(monkeypatch, tmp_path):
    """And the limit: the same claim, traceable, must pass.

    Without this the guard could be satisfied by refusing the chip in prose altogether, which would
    make the feature invisible in exactly the place the panel objected to.
    """
    import gen.test_balance as tb
    page = tmp_path / "estimated.md"
    page.write_text(
        "# A page\n\n"
        "`P-CIP-NAOH` is <span class=\"prov-judgement\">judgement</span> at 125 mM.\n",
        encoding="utf-8")
    monkeypatch.setattr(tb, "_doc_files", lambda: [str(page)])
    tb.test_an_estimated_quantity_in_prose_names_the_parameter_it_estimates()


def test_mutation_a_generated_page_left_out_of_gitignore_is_caught(monkeypatch):
    """The defect walked into while building the census page, reproduced.

    A page correctly generated, navigated and linked, and tracked by git - so every build would
    show it as a diff and the data change that caused it would be reviewed without being read.
    """
    import gen.test_balance as tb
    real = tb._generated_pages()
    monkeypatch.setattr(tb, "_generated_pages", lambda: real | {"registers/not-ignored.md"})
    with pytest.raises(AssertionError, match="not listed in .gitignore"):
        tb.test_every_generated_page_is_gitignored()


def test_mutation_a_bare_percentage_with_no_citation_is_caught(monkeypatch, tmp_path):
    """The hole phase 2 measured and phase 3 closed, held shut by a failing case.

    `_QUANTITY` used to read `(?:%|percent|...)\\b` - ONE word boundary after the whole
    alternation. `%` is not a word character, so `\\b` demanded a word character after it and every
    percentage that ended a clause slipped through. For the guard's whole life it had never policed
    a percentage, which is the single most common way a number is written in this repo's prose.

    THE THREE SHAPES BELOW ARE THE THREE THAT FAILED, and they are checked as a group because
    fixing one spelling and not another is exactly how the bug survived: a percentage at end of
    line, one followed by sentence punctuation, and one followed by a word. If a future edit
    reinstates the trailing boundary, every one of them stops matching and this case goes green -
    so the assertion is that the guard RAISES on all three at once.
    """
    import gen.test_balance as tb
    page = tmp_path / "uncited.md"
    page.write_text(
        "# A page\n\n"
        "Conversion reached 0.5%\n"
        "\n\n\n\n"
        "Recovery was 29 %.\n"
        "\n\n\n\n"
        "It clears 99.9% of the salt.\n",
        encoding="utf-8")
    monkeypatch.setattr(tb, "_doc_files", lambda: [str(page)])
    with pytest.raises(AssertionError, match="numeric claim") as exc:
        tb.test_numeric_claims_in_prose_carry_a_citation()
    message = str(exc.value)
    for shape in ("0.5%", "29 %.", "99.9%"):
        assert shape in message, (
            f"the corrected _QUANTITY missed {shape!r}; a percentage in this shape is unpoliced again")


def test_mutation_a_cited_percentage_passes(monkeypatch, tmp_path):
    """And the limit, or the fix would just be a ban on percentages.

    Same three shapes, each with a real token in its window. Without this the guard could be
    satisfied by never writing a percentage in prose, which is not the property wanted.
    """
    import gen.test_balance as tb
    page = tmp_path / "cited.md"
    page.write_text(
        "# A page\n\n"
        "Conversion reached 0.5% (SRC-ALMAC-2023).\n"
        "\n\n\n\n"
        "Recovery was 29 %. See `Q-011`.\n"
        "\n\n\n\n"
        "`EQ-DIAF` gives 99.9% of the salt cleared.\n",
        encoding="utf-8")
    monkeypatch.setattr(tb, "_doc_files", lambda: [str(page)])
    tb.test_numeric_claims_in_prose_carry_a_citation()


def test_mutation_the_corrected_quantity_pattern_still_refuses_a_longer_unit(monkeypatch, tmp_path):
    """The trailing `\\b` was there for a reason, and moving it must not drop that reason.

    The word-spelled units keep their boundary so `10 mMol` does not match `mM` and report a
    millimolar claim that was never made. Only the `%` branch lost the assertion, because `%` needs
    none. This case fails if a future simplification hoists the boundary out of the group.
    """
    import gen.test_balance as tb
    assert not tb._QUANTITY.search("10 mMol"), (
        "_QUANTITY matched '10 mMol' as a millimolar quantity; the word-spelled units have lost "
        "their trailing word boundary")
    page = tmp_path / "longer-unit.md"
    page.write_text("# A page\n\nThe buffer was 10 mMol overall.\n", encoding="utf-8")
    monkeypatch.setattr(tb, "_doc_files", lambda: [str(page)])
    tb.test_numeric_claims_in_prose_carry_a_citation()


# ---------------------------------------------------------------------------
# Slice 4 phase 4: the unit-operation key, and the solution join it made possible.
#
# The key came first for a reason these cases make concrete. `risks.unit_op` used to hold a
# third spelling of the unit operation - `Ligation` where equipment says `Enzymatic ligation`
# and `UF/DF` where it says `Ultrafiltration/Diafiltration`, with `Utilities` missing from the
# vocabulary altogether - while `instruments.unit_op` and `streams.from_unit`/`to_unit` already
# held `equip_id`. Two of these cases prove the old spellings are now refused; two prove the
# vocabulary is DERIVED from equipment.csv rather than frozen into a literal, which is the
# property that stopped `Utilities` being missing in the first place.
# ---------------------------------------------------------------------------

def test_mutation_a_solution_naming_no_unit_operation_is_caught(mutate):
    """A composition with nowhere to go. Blank was the state of every buffer row before phase 4."""
    mutate("buffers", "buffer_id", "BUF-LIG", equip_ref="")
    with pytest.raises(ValueError, match="blank equip_ref"):
        _validate()()


def test_mutation_a_solution_naming_a_unit_operation_that_does_not_exist_is_caught(mutate):
    """The dangling direction, mutated to the OLD spelling on purpose.

    `Ligation` is what risks.csv said for the whole of Tier 3 until phase 4, so this is the
    mistake a reader of the old register would actually make - and it must now fail rather than
    render as a cross-reference.
    """
    mutate("buffers", "buffer_id", "BUF-LIG", equip_ref="Ligation")
    with pytest.raises(ValueError, match="is not an equip_id"):
        _validate()()


def test_mutation_a_unit_operation_no_solution_names_is_caught(mutate):
    """The reverse direction, which is the one that found five gaps.

    `U00-BUF` is reached by exactly one buffer - `BUF-CIP`, which cleans it - so dropping it from
    that row's `equip_ref` is the only way to build this case without also creating a dangling
    token, the same constraint `test_mutation_a_buffer_nothing_references_is_caught` works under.
    A unit operation with no solution is a piece of plant nobody has said how to clean.
    """
    mutate("buffers", "buffer_id", "BUF-CIP",
           equip_ref="U06-CIP;U01-LIG;U02-CF;U04-EVAP;U05-SD")
    with pytest.raises(ValueError, match=r"U00-BUF: no row of buffers\.csv names it"):
        _validate()()


def test_mutation_the_superseded_risk_unit_op_spelling_is_refused(mutate):
    """`UF/DF` was legal in risks.csv until phase 4 and resolved to nothing. Both guards see it."""
    mutate("risks", "risk_id", "R-005", unit_op="UF/DF")
    import gen.test_balance as tb
    with pytest.raises(AssertionError, match="outside the vocabulary"):
        tb.test_risk_unit_op_and_category_are_a_controlled_vocabulary()
    with pytest.raises(AssertionError, match="is not an equip_id"):
        tb.test_the_unit_operation_vocabularies_resolve_to_one_key()


def test_mutation_the_risk_vocabulary_follows_equipment_rather_than_a_frozen_list(mutate):
    """The derivation itself, which a passing suite cannot demonstrate.

    Rename a unit operation's `equip_id` in equipment.csv and every risk filed against it must
    immediately fall outside the vocabulary. Under the old hardcoded literal this mutation would
    have changed nothing at all - which is exactly how `Utilities` came to be absent from a
    vocabulary that was supposed to describe the plant.
    """
    mutate("equipment", "equip_id", "U01-LIG", equip_id="U01-LIGASE")
    import gen.test_balance as tb
    with pytest.raises(AssertionError, match=r"unit_op 'U01-LIG'"):
        tb.test_risk_unit_op_and_category_are_a_controlled_vocabulary()


def test_mutation_a_new_unit_operation_with_no_solution_fails_the_join(mutate):
    """The forward-looking half: the eighth unit operation cannot be added without a solution.

    Mutating an existing `equip_id` is the available way to simulate an ADDED row - the harness
    edits rows rather than appending them - and it has the same effect on the join, because the
    new id is one no buffer names.
    """
    mutate("equipment", "equip_id", "U04-EVAP", equip_id="U07-NEW")
    with pytest.raises(ValueError, match=r"U07-NEW: no row of buffers\.csv names it"):
        _validate()()


# ---------------------------------------------------------------------------
# Slice 4 phase 4: the same estimate obligations, now against ROWS THAT REALLY CARRY THEM.
#
# The nine phase-2 cases above all supply the estimate themselves, because no row carried
# `judgement` when they were written. Three do now - BUF-CIP, BUF-DF and BUF-FINAL - and a
# guard proved only against a synthetic row is a guard proved against a row whose shape the
# test author chose. These two mutate the live ones.
# ---------------------------------------------------------------------------

def test_mutation_the_first_real_estimate_may_not_write_its_composition(mutate):
    """BUF-CIP is the first row in this repository to carry the fourth provenance.

    Its number lives in `est_value` and `components` stays blank, which is what makes the recipe
    unconsumable. Writing the recipe into `components` is the exact promotion the provenance
    exists to prevent, and it must fail on the real row and not only on a supplied one.
    """
    mutate("buffers", "buffer_id", "BUF-CIP", components="NaOH 1% w/v (0.25 M) at 50 C, 30 min")
    with pytest.raises(ValueError, match="an estimate wrote components="):
        _validate()()


def test_mutation_closing_the_question_under_a_live_estimate_is_caught(mutate):
    """Mutate the QUESTION, not the estimate - the direction nothing else covers.

    `BUF-CIP` leaves Q-074 open, and Q-074 is a real row somebody could mark resolved without
    ever opening buffers.csv. The contradiction is then silent unless the guard reads across:
    either the estimate closed the question, in which case it is not an estimate, or the question
    register is wrong.
    """
    mutate("questions", "question_id", "Q-074", status="resolved")
    with pytest.raises(ValueError, match=r"basis names Q-074, whose status is 'resolved'"):
        _validate()()


# ---------------------------------------------------------------------------
# Slice 4 phase 5. The guards added with the sizing work and the carryover criteria,
# each proved against the defect it claims to catch.
# ---------------------------------------------------------------------------

def test_mutation_a_unit_operation_losing_its_cleaning_chemistry_is_caught(mutate):
    """The premise the balance's DERIVED circuit count rests on, attacked at its weakest point.

    `solution_offenders` would NOT catch this: drop the evaporator from the caustic wash's
    `equip_ref` and `U04-EVAP` is still named by nothing else... except that is exactly the case the
    wider guard also happens to see. So the mutation is chosen to separate the two guards - the
    evaporator is dropped from `BUF-CIP` while `BUF-MEMBRANE-CLEAN` keeps every unit it had, and the
    narrow guard must name `U04-EVAP` specifically as lacking a CLEANING chemistry rather than any
    solution at all.
    """
    from gen.envelope import cip_coverage_offenders
    mutate("buffers", "buffer_id", "BUF-CIP",
           equip_ref="U06-CIP;U00-BUF;U01-LIG;U02-CF;U05-SD")
    offenders = cip_coverage_offenders()
    assert any("U04-EVAP" in o for o in offenders), (
        "dropping the evaporator from the only caustic recipe that reaches it must be caught: the "
        "balance is still charging cleaning water for it. Got: " + "; ".join(offenders))


def test_mutation_the_cleaning_solution_constant_drifting_from_the_register_is_caught(mutate):
    """`CIP_SOLUTIONS` names rows; if a row is renamed the constant must break, not narrow.

    This is the failure mode a prose search would have had: silently matching fewer rows and
    shrinking what "cleaned" means without anything going red. Renaming the buffer id makes the
    constant point at nothing, and the guard has to say so rather than conclude that nothing is
    cleaned by caustic.
    """
    from gen.envelope import cip_coverage_offenders
    mutate("buffers", "buffer_id", "BUF-CIP", buffer_id="BUF-CAUSTIC")
    offenders = cip_coverage_offenders()
    assert any("CIP_SOLUTIONS" in o and "BUF-CIP" in o for o in offenders), (
        "a renamed cleaning row must break the constant explicitly. Got: " + "; ".join(offenders))


def test_mutation_blanking_a_cip_input_refuses_rather_than_cleaning_for_free(mutate):
    """Cleaning demand must not be able to return to zero by a blank.

    The whole point of the phase-5 term is that `U06-CIP` costs something. A blank wash volume is
    the shortest route back to zero litres, and `_require` has to refuse it - the same rule that
    already protects every thermal constant.
    """
    from gen.balance import run_all
    mutate("parameters", "param_id", "P-CIP-WASH-VOL", value="")
    with pytest.raises(ValueError, match="P-CIP-WASH-VOL"):
        run_all()


def test_mutation_a_loss_fraction_that_consumes_the_step_is_caught(mutate):
    """The composed-yield bound, proved through the DATA layer as well as in process.

    `test_a_loss_fraction_that_consumes_the_step_raises_instead_of_publishing` proves it against an
    in-memory parameter copy; this proves the same defect arriving the way it really would, as an
    edited CSV. Before the bound existed this mutation produced a MINUS 30,483 L ligation volume and
    a negative clean-water demand, and the build published them.
    """
    from gen.balance import run_all
    mutate("parameters", "param_id", "P-UFDF-HOLDUP-LOSS", value="1.2")
    with pytest.raises(ValueError, match="outside .0, 1."):
        run_all()


def test_mutation_a_value_written_into_the_refused_fill_ratio_is_caught(mutate):
    """The phase-1 refusal, exercised by the row phase 5 added.

    `P-LIG-FILL-RATIO` is blank because 2 and 5 are two readings of one number rather than two ends
    of a window. Picking one of them and writing it in is the tempting defect - it looks like
    progress - and it is the same shape as the `P-LIG-SEG-CONC` hole the red team walked through.
    """
    from gen.envelope import value_written_where_refused
    mutate("parameters", "param_id", "P-LIG-FILL-RATIO", value="5")
    offenders = value_written_where_refused()
    assert any("P-LIG-FILL-RATIO" in o for o in offenders), (
        "writing one side of a published contradiction into the value column must be refused. "
        "Got: " + "; ".join(offenders))


def test_mutation_citing_the_transfer_guideline_for_the_criteria_is_caught(mutate):
    """THE TRAP, proved. Both keys resolve, both are WHO, both were read in full.

    `SRC-WHO-TRS1044` is the technology-transfer guideline and `SRC-WHO-TRS1019-A3` is the validation
    one. Swap them on a carryover criterion and every pre-existing guard in this repository stays
    green - the source resolves, the access grade is a read grade, the provenance is `fact` with a
    source. Nothing but a guard that knows the two documents apart can see it.
    """
    from gen.dataio import load_params, load_rows
    mutate("parameters", "param_id", "P-CARRYOVER-PPM", source_key="SRC-WHO-TRS1044")
    params = load_params()
    row = params["P-CARRYOVER-PPM"]
    sources = {r["source_key"]: r for r in load_rows("sources")}
    # Everything the existing guards check still passes, which is the point:
    assert row["provenance"] == "fact"
    assert row["source_key"] in sources
    assert sources[row["source_key"]]["access"] == "full-text-read"
    # And the phase-5 guard is the only thing that sees it - at build time, not just here.
    from gen.envelope import criterion_source_offenders, validate
    offenders = criterion_source_offenders()
    assert any("P-CARRYOVER-PPM" in o and "SRC-WHO-TRS1044" in o for o in offenders), (
        "the wrong WHO document must be named explicitly. Got: " + "; ".join(offenders))
    with pytest.raises(ValueError, match="technology-transfer"):
        validate()


def test_mutation_a_criterion_citing_nothing_that_prints_it_is_caught(mutate):
    """The other direction of the same guard: a criterion whose citation prints no criterion.

    Dropping the source entirely and leaving the notes behind is the subtler version - the row still
    READS as sourced, because its notes quote the clause. `test_fact_params_have_sources` catches a
    blank `source_key` on a `fact` row, so this mutation also clears the notes to get past it and
    land on the guard that actually checks WHICH document.
    """
    from gen.envelope import criterion_source_offenders
    mutate("parameters", "param_id", "P-CARRYOVER-DOSE-FRAC",
           source_key="SRC-ICH-Q7", notes="Q-047", scale_system="")
    offenders = criterion_source_offenders()
    assert any("P-CARRYOVER-DOSE-FRAC" in o and "prints the" in o for o in offenders), (
        "a criterion citing a document that does not print it must be caught. Got: "
        + "; ".join(offenders))


def test_mutation_a_range_across_two_carryover_criteria_is_caught(mutate):
    """10 ppm and 0.1% of dose are ALTERNATIVES under a most-stringent rule, not a band.

    Banding two criteria with different denominators is the `not_a_range` defect in its purest form,
    and it would render as a window of acceptable carryover that no document permits. The band guard
    demands an endpoint audit for any range in `parameters.csv`, so this mutation has to be caught
    even before anyone asks what the two ends mean.
    """
    from gen.envelope import unaudited_bands
    mutate("parameters", "param_id", "P-CARRYOVER-PPM",
           range_low="0.1", range_high="10", range_kind="evidence")
    offenders = unaudited_bands()
    assert any("P-CARRYOVER-PPM" in o for o in offenders), (
        "a range invented across two different criteria must be caught as an unaudited band. "
        "Got: " + "; ".join(offenders))


def test_the_percent_per_million_branch_was_proved_against_the_old_regex():
    """`ppm` added to the prose-citation quantity pattern, with the old pattern shown to miss it.

    Phase 3 fixed the same class for `%` and recorded the method: prove the new branch catches
    something the old one did not, or the addition is decoration. This phase publishes the first ppm
    criterion in the register (`P-CARRYOVER-PPM`), so an uncited ppm claim in prose became a real
    hazard rather than a hypothetical one. Measured when it was added: ZERO existing prose lines are
    newly caught, so the guard closes a class rather than creating work.
    """
    import re as _re
    from gen.test_balance import _QUANTITY
    old = _re.compile(
        r"(?<![\w.-])\d+(?:\.\d+)?\s?"
        r"(?:%|(?:percent|g/L|mg/mL|kDa|Da|kJ/kg|EU/mL|CFU|LMH|mM|°C|kWh|MJ)\b)")
    for sample in ("no more than 10 ppm of any product", "a limit of 0.5 ppm in rinse water"):
        assert not old.search(sample), f"the old pattern already matched {sample!r}"
        assert _QUANTITY.search(sample), f"the new pattern must match {sample!r}"
