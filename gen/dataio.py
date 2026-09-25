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
