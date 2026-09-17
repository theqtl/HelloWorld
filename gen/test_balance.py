"""Integrity + balance tests. Run: python -m pytest gen/ -q"""
import os
from gen.dataio import load_rows, load_params, param_value
from gen.balance import run_all, purity_floor


def test_all_source_keys_resolve():
    sources = {r["source_key"] for r in load_rows("sources")}
    # parameters and risks reference source_key; blanks allowed
    for name in ("parameters", "risks"):
        for r in load_rows(name):
            key = (r.get("source_key") or "").strip()
            if key:
                assert key in sources, f"{name}: unknown source_key {key}"


def test_fact_params_have_sources():
    """Quality gate: a 'fact' parameter must cite a source (or reference another param)."""
    params = load_params()
    for r in params.values():
        if r["provenance"] == "fact":
            key = (r.get("source_key") or "").strip()
            assert key, f"fact parameter {r['param_id']} has no source_key"


def test_assumption_params_reference_a_question():
    """Every assumption placeholder must point to an open question (Q-...)."""
    for r in load_rows("parameters"):
        if r["provenance"] == "assumption":
            assert "Q-" in (r.get("notes") or ""), \
                f"assumption {r['param_id']} not linked to an open question"


def test_no_value_without_provenance():
    for r in load_rows("parameters"):
        if (r.get("value") or "").strip():
            assert r["provenance"] in ("fact", "inference", "assumption"), \
                f"{r['param_id']} has a value but bad provenance {r['provenance']!r}"


def test_questions_referenced_exist():
    qids = {r["question_id"] for r in load_rows("questions")}
    for r in load_rows("parameters"):
        note = r.get("notes") or ""
        for ch in ".,/;()":
            note = note.replace(ch, " ")
        for tok in note.split():
            if tok.startswith("Q-") and len(tok) >= 5:
                assert tok in qids, f"{r['param_id']} references missing {tok}"


def test_balance_runs_and_is_sane():
    results = run_all()
    assert results, "no scenarios"
    for r in results:
        assert 0 < r.overall_yield_frac < 1
        # yield <1 means more API needed at ligation than delivered as DS
        assert r.api_at_ligation_kg > r.ds_api_per_campaign_kg
        for v in (r.ligation_volume_L, r.uf_retentate_volume_L, r.df_buffer_volume_L,
                  r.evap_water_removed_L, r.dryer_feed_mass_kg, r.wfi_approx_L,
                  r.aqueous_waste_approx_L, r.evap_duty_MJ, r.dryer_evap_duty_MJ):
            assert v >= 0
        # duty consistency: MJ/3.6 == kWh
        assert abs(r.evap_duty_MJ / 3.6 - r.evap_duty_kWh) < 1e-6


def test_balance_scales_with_demand():
    results = {r.scenario_id: r for r in run_all()}
    # more annual demand -> more API at ligation (same campaigns structure aside)
    assert results["S3"].annual_ds_api_kg > results["S1"].annual_ds_api_kg
    assert results["S3"].api_at_ligation_kg > results["S1"].api_at_ligation_kg


def test_purity_floor_monotonic_and_bounded():
    assert purity_floor(92, 1) > purity_floor(92, 3)      # more blocks -> lower floor
    assert purity_floor(95, 3) > purity_floor(90, 3)      # purer blocks -> higher floor
    assert 0 < purity_floor(92, 3) < 100
    # 3 x 92% blocks -> ~77.9%
    assert abs(purity_floor(92, 3) - 77.87) < 0.5


def test_data_files_present():
    for name in ("parameters", "streams", "equipment", "buffers", "utilities",
                 "risks", "questions", "sources", "scenarios"):
        assert load_rows(name), f"{name}.csv empty or missing"


# ---------------------------------------------------------------------------
# Regression guards added after the citation audit of 2026-09-17.
# Each of these would have caught a real defect that shipped in Tier 1.
# ---------------------------------------------------------------------------
import glob
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _doc_files():
    return sorted(glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True))


def _sources_blob():
    """All text in the source register, for checking whether a reference is registered."""
    return "\n".join(
        " ".join(r.values()) for r in load_rows("sources")
    )


# Reference shapes that must never appear in prose without being registered as a source.
# The Tier-1 site cited "USPTO 6187190" for a rule that patent does not contain; nothing
# in the suite could see it, because prose citations were invisible to the tests.
_REF_PATTERNS = [
    re.compile(r"\bUS\s?\d{7,8}\b"),
    re.compile(r"\bUSPTO\s+\d{6,8}\b"),
    re.compile(r"\bWO\s?\d{4}/?\d{6}\b"),
    re.compile(r"\bEP\s?\d{6,}\b"),
    re.compile(r"\b10\.\d{4,9}/[^\s)\]]+"),
]


def test_prose_references_are_registered():
    """Every patent number or DOI written in prose must exist in data/sources.csv."""
    blob = _sources_blob()
    offenders = []
    for path in _doc_files():
        text = open(path, encoding="utf-8").read()
        for pat in _REF_PATTERNS:
            for m in pat.finditer(text):
                ref = m.group(0)
                digits = re.sub(r"\D", "", ref)
                if digits and digits in re.sub(r"\D", "", blob):
                    continue
                if ref in blob:
                    continue
                offenders.append(f"{os.path.relpath(path, ROOT)}: {ref}")
    assert not offenders, (
        "unregistered reference(s) cited in prose; add them to data/sources.csv "
        "or remove the claim: " + "; ".join(offenders)
    )


def test_source_keys_in_prose_are_defined():
    """Every SRC-* mentioned in the documents must be a real row in the source register."""
    defined = {r["source_key"] for r in load_rows("sources")}
    offenders = []
    for path in _doc_files():
        text = open(path, encoding="utf-8").read()
        for key in set(re.findall(r"SRC-[A-Z0-9-]+", text)):
            if key not in defined:
                offenders.append(f"{os.path.relpath(path, ROOT)}: {key}")
    assert not offenders, "undefined source key(s): " + "; ".join(offenders)


def test_reachability_is_honest_about_open_access():
    """A source with an open-access identifier must not be labelled paywalled.

    The spray-drying glass-transition error survived because the paper was marked
    'paywalled (abstract only)' when it is open access at PubMed Central, so nobody
    opened it.
    """
    offenders = []
    for r in load_rows("sources"):
        reach = (r.get("reachability") or "").lower()
        blob = " ".join(r.values())
        has_open_id = bool(re.search(r"PMC\d{5,}", blob)) or "open access" in blob.lower()
        if "paywall" in reach and has_open_id and "open access" not in reach:
            offenders.append(r["source_key"])
    assert not offenders, (
        "source(s) marked paywalled despite an open-access identifier: " + ", ".join(offenders)
    )


def test_every_question_reference_exists_in_every_csv():
    """Q-ids are cited from several registers, not just parameters.csv.

    All three throughput scenarios cited Q-001 (the annealing question) for annual
    demand, which is Q-002. Only parameters.csv was checked before.
    """
    qids = {r["question_id"] for r in load_rows("questions")}
    offenders = []
    for name in ("parameters", "scenarios", "risks", "equipment", "buffers", "utilities",
                 "streams", "sources"):
        for row in load_rows(name):
            for value in row.values():
                for tok in re.findall(r"Q-\d{3}", value or ""):
                    if tok not in qids:
                        offenders.append(f"{name}.csv: {tok}")
    assert not offenders, "reference(s) to undefined question(s): " + "; ".join(sorted(set(offenders)))


def test_scenarios_cite_the_demand_question():
    """Throughput scenarios are illustrative because annual demand is unknown (Q-002)."""
    for row in load_rows("scenarios"):
        assert "Q-002" in (row.get("notes") or ""), (
            f"scenario {row['scenario_id']} must cite Q-002, the annual demand question"
        )


def test_parameter_usage_matches_the_code():
    """`used_by` must tell the truth about which parameters the balance actually reads."""
    src = open(os.path.join(ROOT, "gen", "balance.py"), encoding="utf-8").read()
    wrong = []
    for r in load_rows("parameters"):
        pid, used_by = r["param_id"], (r.get("used_by") or "").strip()
        assert used_by in ("balance", "analysis", "docs"), f"{pid}: bad used_by {used_by!r}"
        referenced = pid in src
        if used_by in ("balance", "analysis") and not referenced:
            wrong.append(f"{pid} claims used_by={used_by} but never appears in gen/balance.py")
        if used_by == "docs" and referenced:
            wrong.append(f"{pid} is marked docs-only but gen/balance.py reads it")
    assert not wrong, "; ".join(wrong)


def test_solids_close_between_evaporator_and_dryer():
    """One solids basis through the train: what leaves the evaporator must reach the dryer."""
    params = load_params()
    r = param_value(params, "P-EXCIPIENT-RATIO")
    y_evap = param_value(params, "P-YLD-EVAP") / 100.0
    f_pre = param_value(params, "P-EXCIP-FRAC-PRE-EVAP")
    for res in run_all():
        api_after_evap = res.evap_outlet_solids_kg / (1.0 + f_pre * r) * y_evap
        expected_dry_solids = api_after_evap * (1.0 + r)
        actual_dry_solids = res.dryer_feed_mass_kg - res.dryer_water_evaporated_kg
        assert abs(expected_dry_solids - actual_dry_solids) < 1e-6, (
            f"{res.scenario_id}: solids do not close across evaporation "
            f"({expected_dry_solids} vs {actual_dry_solids})"
        )


def test_balance_refuses_a_blank_required_input():
    """A gap must raise, never silently become a number. The latent-heat fallback broke this."""
    import pytest
    params = load_params()
    params["P-H2O-LHV"]["value"] = ""
    scn = load_rows("scenarios")[0]
    from gen.balance import run_scenario
    with pytest.raises(ValueError):
        run_scenario(scn, params)


def test_purity_floor_defaults_to_the_registered_block_purity():
    """The figure quoted in the documents and the one used in code must be the same figure."""
    from gen.balance import purity_floor
    registered = param_value(load_params(), "P-BLOCK-PUR")
    assert abs(purity_floor() - purity_floor(registered, 3)) < 1e-9


def test_flowsheet_stream_ids_match_the_register():
    """The diagram lost its product-outlet arrow because nothing checked it against the data."""
    svg = open(os.path.join(ROOT, "docs", "diagrams", "bfd.svg"), encoding="utf-8").read()
    drawn = set(re.findall(r"\bS\d{2}\b", svg))
    registered = {r["stream_id"] for r in load_rows("streams")}
    missing = registered - drawn
    unknown = drawn - registered
    assert not missing, f"stream(s) in the register but absent from the flowsheet: {sorted(missing)}"
    assert not unknown, f"stream(s) drawn but not in the register: {sorted(unknown)}"


def test_flowsheet_units_resolve_to_equipment():
    """Every from_unit/to_unit must be a real equipment id or a declared boundary sentinel."""
    sentinels = {"SUPPLY", "WASTE", "DS-STORE"}
    equip = {r["equip_id"] for r in load_rows("equipment")}
    offenders = []
    for r in load_rows("streams"):
        for field in ("from_unit", "to_unit"):
            unit = r[field]
            if unit not in equip and unit not in sentinels:
                offenders.append(f"{r['stream_id']}.{field}={unit}")
    assert not offenders, "unresolved unit reference(s): " + ", ".join(offenders)


def test_diagram_is_not_duplicated_in_prose():
    """The flowsheet drifted because it existed twice. It must live in exactly one file."""
    offenders = []
    for path in _doc_files():
        if "<svg" in open(path, encoding="utf-8").read():
            offenders.append(os.path.relpath(path, ROOT))
    assert not offenders, (
        "inline SVG copy found in " + ", ".join(offenders) +
        "; include docs/diagrams/bfd.svg with a snippet instead of pasting it"
    )


def test_every_csv_row_has_the_right_number_of_fields():
    """A malformed row silently shifts every column after it.

    buffers.csv carried a stray tenth field that put a provenance value in the
    source_key column, and nothing detected it because load_rows() still returned
    truthy rows.
    """
    import csv as _csv
    offenders = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "*.csv"))):
        with open(path, newline="", encoding="utf-8") as fh:
            reader = _csv.DictReader(fh)
            width = len(reader.fieldnames)
            for lineno, row in enumerate(reader, start=2):
                if None in row:
                    offenders.append(
                        f"{os.path.basename(path)} line {lineno}: "
                        f"{width + len(row[None])} fields, header has {width}"
                    )
                if any(v is None for v in row.values()):
                    offenders.append(
                        f"{os.path.basename(path)} line {lineno}: fewer fields than header"
                    )
    assert not offenders, "malformed CSV row(s): " + "; ".join(offenders)


# A physical quantity asserted in prose must have a citation, a parameter id, an equation id
# or an explicit provenance flag within a few lines of it. This is the check that would have
# caught nearly every citation defect found in the 2026-09-17 audit: an unsourced RNA recovery
# figure, a vendor titre that existed nowhere, a concentration ceiling belonging to another
# paper, a film thickness absent from both cited pages.
_QUANTITY = re.compile(
    r"(?<![\w.-])\d+(?:\.\d+)?\s?(?:%|percent|g/L|mg/mL|kDa|Da|kJ/kg|EU/mL|CFU|LMH|mM|°C|kWh)\b"
)
_CITATION = re.compile(
    r"SRC-[A-Z0-9-]+|\bP-[A-Z0-9-]{3,}|\bEQ-[A-Z]+|\bQ-\d{3}|\bR-\d{3}"
    r"|prov-assumption|prov-inference"
)

# Lines whose numbers are qualitative or self-evident rather than sourced claims.
_QUANTITY_ALLOWLIST = (
    "<< 1 kDa",          # salts are obviously far below a kDa
    "(<1 kDa)",
)


def test_numeric_claims_in_prose_carry_a_citation():
    offenders = []
    for path in _doc_files():
        rel = os.path.relpath(path, ROOT)
        # Generated register pages carry their provenance in columns; the ADR is an
        # architecture argument, not a process claim.
        if "/registers/" in rel or rel.endswith(("balance/results.md", "process/streams.md")):
            continue
        if "/adr/" in rel:
            continue
        lines = open(path, encoding="utf-8").read().split("\n")
        for i, line in enumerate(lines):
            if not _QUANTITY.search(line):
                continue
            if any(tok in line for tok in _QUANTITY_ALLOWLIST):
                continue
            window = "\n".join(lines[max(0, i - 3): i + 4])
            if not _CITATION.search(window):
                offenders.append(f"{rel}:{i + 1}  {line.strip()[:90]}")
    assert not offenders, (
        "numeric claim(s) with no citation, parameter, equation or provenance flag nearby:\n  "
        + "\n  ".join(offenders)
    )
