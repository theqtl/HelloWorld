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
