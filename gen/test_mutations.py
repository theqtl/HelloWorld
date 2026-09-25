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
