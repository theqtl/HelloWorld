"""Integrity + balance tests. Run: python -m pytest gen/ -q"""
import os
from gen.dataio import load_rows, load_params, param_value
from gen.balance import run_all, purity_floor


def test_all_source_keys_resolve():
    sources = {r["source_key"] for r in load_rows("sources")}
    # parameters, risks, impurities, controls and instruments reference source_key; blanks allowed
    for name in ("parameters", "risks", "impurities", "controls", "instruments"):
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
                 "risks", "questions", "sources", "scenarios", "impurities",
                 "controls", "instruments", "envelopes", "couplings", "infoneeds",
                 "verdicts"):
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
                 "streams", "sources", "impurities", "controls", "instruments",
                 "envelopes", "couplings", "infoneeds", "verdicts"):
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


def test_energy_duties_exceed_the_latent_minimum_by_construction():
    """The latent minimum is a STRICT floor, and it must hold structurally - not because the
    placeholder values happen to be large enough.

    The previous version of this test asserted the same ordering for a dryer model that
    contained no latent term at all, so it passed only while P-DRYGAS-RATIO was set high
    enough (it failed below ~24, and a 120 C inlet broke it). The model now adds only
    non-negative terms to the latent floor, and the heater duty is the process duty scaled by
    (T_in - T_amb)/(T_in - T_out) >= 1, so both orderings are guaranteed by the arithmetic.
    """
    for r in run_all():
        assert r.evap_feed_mass_kg > 0
        assert r.evap_sensible_MJ >= 0
        assert r.dryer_feed_sensible_MJ >= 0
        assert r.drying_gas_kg > 0
        assert r.evap_duty_full_MJ >= r.evap_duty_MJ
        assert r.dryer_process_duty_MJ >= r.dryer_evap_duty_MJ
        # the utility load is never below what the process needs
        assert r.dryer_heater_duty_MJ >= r.dryer_process_duty_MJ
        assert abs(r.evap_duty_full_MJ / 3.6 - r.evap_duty_full_kWh) < 1e-6
        assert abs(r.dryer_process_duty_MJ / 3.6 - r.dryer_process_duty_kWh) < 1e-6
        assert abs(r.dryer_heater_duty_MJ / 3.6 - r.dryer_heater_duty_kWh) < 1e-6


def test_the_latent_floor_ordering_survives_adverse_parameters():
    """The ordering must be structural, so it has to survive values that broke the old model.

    A 120 C inlet and a low outlet-to-ambient span used to make the dryer 'full duty' fall
    below its own latent floor. Nothing about the registered placeholders may be load-bearing.
    """
    from gen.balance import run_scenario
    scn = load_rows("scenarios")[0]
    for t_in, t_out, t_amb in ((120, 60, 20), (90, 55, 20), (150, 25, 20), (200, 56, 55)):
        params = load_params()
        params["P-DRY-T-IN"]["value"] = str(t_in)
        params["P-DRY-T-OUT"]["value"] = str(t_out)
        params["P-DRY-T-AMBIENT"]["value"] = str(t_amb)
        r = run_scenario(scn, params)
        assert r.dryer_process_duty_MJ >= r.dryer_evap_duty_MJ, (t_in, t_out, t_amb)
        assert r.dryer_heater_duty_MJ >= r.dryer_process_duty_MJ, (t_in, t_out, t_amb)


def test_an_impossible_operating_point_raises_instead_of_clamping():
    """An inverted temperature pair is a data error. It used to vanish into max(...,0) and
    report a silent 0 MJ duty; it must raise, like any other bad input."""
    import pytest
    from gen.balance import run_scenario
    scn = load_rows("scenarios")[0]
    for pid, bad in (("P-DRY-T-IN", "40"),        # inlet below outlet
                     ("P-DRY-T-AMBIENT", "90"),   # ambient above outlet
                     ("P-EVAP-T-FEED", "90")):    # feed above the boiling point
        params = load_params()
        params[pid]["value"] = bad
        with pytest.raises(ValueError):
            run_scenario(scn, params)


def test_the_base_case_actually_evaporates_something():
    """`evap_water` is clamped at zero for a legitimate reason (UF may already exceed the
    evaporator target), but that clamp can also absorb a wrong volume basis into a silent zero
    duty. Assert the registered base case still has evaporation to do, so that cannot pass
    unnoticed."""
    for r in run_all():
        assert r.evap_water_removed_L > 0, (
            f"{r.scenario_id}: the evaporator removes no water, so its duty is silently zero; "
            "check the volume basis rather than accepting the clamp"
        )


def test_blanking_a_thermal_constant_refuses():
    """Every energy-balance input obeys the blank-refusal rule: a gap raises, never
    silently defaults to a number (same invariant as P-H2O-LHV)."""
    import pytest
    from gen.balance import run_scenario
    scn = load_rows("scenarios")[0]
    for pid in ("P-CP-SOLN", "P-DRYGAS-CP", "P-EVAP-T-FEED", "P-EVAP-T-BOIL",
                "P-DRY-T-IN", "P-DRY-T-OUT", "P-DRY-T-AMBIENT", "P-SOLN-DENSITY",
                "P-HEAT-LOSS-FRAC"):
        params = load_params()
        params[pid]["value"] = ""
        with pytest.raises(ValueError):
            run_scenario(scn, params)


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
    """The figure quoted in the documents and the one used in code must be the same figure.

    The exponent is read from P-N-BLOCKS rather than written as a literal. It used to be a
    hardcoded 3, which made the guard agree with the code only for as long as the register
    happened to say 3 - so the one thing it was supposed to prove, that nothing drifts from
    the register, was the thing it stopped checking the moment the register moved.
    """
    from gen.balance import purity_floor
    params = load_params()
    f = param_value(params, "P-BLOCK-PUR")
    k = param_value(params, "P-N-BLOCKS")
    assert f is not None and k is not None, (
        "P-BLOCK-PUR and P-N-BLOCKS must both carry values - purity_floor() reads both")
    assert abs(purity_floor() - purity_floor(f, k)) < 1e-9


def test_flowsheet_stream_ids_match_the_register():
    """The diagram lost its product-outlet arrow because nothing checked it against the data."""
    svg = open(os.path.join(ROOT, "docs", "diagrams", "bfd.svg"), encoding="utf-8").read()
    drawn = set(re.findall(r"\bS\d{2}\b", svg))
    registered = {r["stream_id"] for r in load_rows("streams")}
    missing = registered - drawn
    unknown = drawn - registered
    assert not missing, f"stream(s) in the register but absent from the flowsheet: {sorted(missing)}"
    assert not unknown, f"stream(s) drawn but not in the register: {sorted(unknown)}"


def test_flowsheet_is_up_to_date():
    """bfd.svg is generated from data/streams.csv; the committed file must match render().

    CI runs the flowsheet drift tests against the committed SVG BEFORE gen.build
    regenerates it, so a stale committed file would pass the drift check while showing
    the wrong picture. This closes that gap: regenerate and commit after any data change.
    """
    from gen.flowsheet import render
    committed = open(os.path.join(ROOT, "docs", "diagrams", "bfd.svg"), encoding="utf-8").read()
    assert render() == committed, (
        "docs/diagrams/bfd.svg is stale; run `python -m gen.build` and commit the result"
    )


def test_flowsheet_layout_is_deterministic():
    """The generator must be a pure function of the data (no dict/order nondeterminism)."""
    from gen.flowsheet import render
    assert render() == render()


def test_flowsheet_legend_describes_the_actual_styles():
    """The legend claimed "Teal = product path" while the product arrows were currentColor, and
    "red dashed = waste" while the waste lines carried no dash pattern - two of three claims
    false. Inherited from the hand-drawn file, then carried into a GENERATED artifact under the
    claim that it could no longer drift, so it is now checked against the emitted CSS."""
    from gen.flowsheet import render
    svg = render()
    assert "Teal = product path" in svg and "red dashed = waste" in svg, "legend text changed"
    flow = re.search(r"\.flow \{[^}]*\}", svg).group(0)
    wflow = re.search(r"\.wflow \{[^}]*\}", svg).group(0)
    uflow = re.search(r"\.uflow \{[^}]*\}", svg).group(0)
    assert "#00897b" in flow, f"legend says teal, but .flow is {flow}"
    assert "stroke-dasharray" in wflow, f"legend says red DASHED, but .wflow is {wflow}"
    assert "stroke-dasharray" in uflow, f"legend says purple DASHED, but .uflow is {uflow}"


def test_flowsheet_survives_a_non_product_stream(monkeypatch):
    """A utility/CIP stream must not take down the build.

    Adding one raised KeyError, because only PRODUCT-stream nodes had a column - so the first
    CIP stream the contamination-control work adds would have broken `gen.build`, CI and the
    whole site build at once.
    """
    from gen import flowsheet
    extra = [
        {"stream_id": "S13", "name": "CIP supply", "from_unit": "U00-BUF",
         "to_unit": "U06-CIP", "stream_class": "utility", "phase": "aqueous",
         "carries": "cleaning solution", "notes": ""},
        {"stream_id": "S14", "name": "CIP return (waste)", "from_unit": "U06-CIP",
         "to_unit": "WASTE", "stream_class": "waste", "phase": "aqueous",
         "carries": "spent cleaning solution", "notes": ""},
    ]
    real = flowsheet.load_rows
    monkeypatch.setattr(
        flowsheet, "load_rows",
        lambda name: (real(name) + extra) if name == "streams" else real(name),
    )
    svg = flowsheet.render()
    assert "S13" in svg and "S14" in svg, "added streams were not drawn"
    assert "U06" in svg, "the connected CIP unit was silently dropped from the diagram"


def test_flowsheet_rejects_a_product_cycle():
    """A recycle stream must raise, never yield garbage ranks.

    The relaxation loop used to exit silently after N passes, and R-013 requires the
    evaporator to recirculate, so a recycle stream is a foreseeable data change.
    """
    import pytest
    from gen.flowsheet import _rank_product_nodes
    cyclic = [
        {"from_unit": "A", "to_unit": "B", "stream_class": "product"},
        {"from_unit": "B", "to_unit": "A", "stream_class": "product"},
    ]
    with pytest.raises(ValueError):
        _rank_product_nodes(cyclic)


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
    r"(?<![\w.-])\d+(?:\.\d+)?\s?(?:%|percent|g/L|mg/mL|kDa|Da|kJ/kg|EU/mL|CFU|LMH|mM|°C|kWh|MJ)\b"
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


# ---------------------------------------------------------------------------
# Source-access guards added 2026-09-18.
#
# Before these, the register could not tell you at a glance which sources had only
# ever been read as an abstract — precisely the condition that produced the
# 2026-09-17 citation defects. `reachability` was free text: 35 rows carried 14
# distinct values, and the six abstract-or-less sources were spelled five
# different ways. The controlled `access` column fixes the instrument; these
# three tests keep it honest.
#
# `access` says what was actually READ. `reachability` says how to GET it.
# ---------------------------------------------------------------------------

#: The controlled vocabulary. One value per row, nothing else.
ACCESS_VOCAB = {
    "full-text-read",   # the complete article or document was read
    "web-page-read",    # a web page, blog, vendor note, standard or patent read in full
    "partial-text-read",  # retrieved and readable in full; SPECIFIED SECTIONS read, not all
                        # of it. Added because the vocabulary could not express the true
                        # state of a long guideline whose text layer was searched entirely
                        # but whose body was read in part: `full-text-read` over-claims and
                        # `record-only` under-claims so far that it misleads. Three
                        # independent research passes reported the same gap and each
                        # refused to force a value. A row using this MUST enumerate the
                        # sections read and the page count in `notes` - see
                        # test_a_partial_read_says_what_was_read.
    "abstract-only",    # only the abstract, or an abstract-equivalent record summary
    "record-only",      # only bibliographic metadata confirmed; no abstract read
    "redacted",         # obtainable and read, but the numbers we need are withheld in it
    "not-retrieved",    # could not be obtained at all
}

#: Access values that mean nobody has read the work itself.
ACCESS_UNREAD = {"abstract-only", "record-only", "not-retrieved"}

#: Tokens that count as naming an open-access route out of a paywall. A row may
#: claim full-text-read behind a paywall only if it says HOW the full text was got.
_OPEN_ROUTE_TOKENS = (
    "open access", "open-access", "pmc", "europe pmc", "europepmc", "unpaywall",
    "repository", "scholarsphere", "etda", "eprint", "preprint", "biorxiv",
    "chemrxiv", "arxiv", "ssrn", "thesis", "dissertation", "figshare",
    "author manuscript", "accepted manuscript", "proceedings", "si retrieved",
)


def test_access_values_are_in_the_controlled_vocabulary():
    """`access` is a controlled column, not free text. That is the whole point of it."""
    offenders = []
    for r in load_rows("sources"):
        value = (r.get("access") or "").strip()
        if value not in ACCESS_VOCAB:
            offenders.append(f"{r['source_key']}: {value!r}")
    assert not offenders, (
        "source(s) with an access value outside the controlled vocabulary "
        f"{sorted(ACCESS_VOCAB)}: " + "; ".join(offenders)
    )


def test_a_partial_read_says_what_was_read():
    """`partial-text-read` is only honest if it states WHICH part was read.

    The value exists so a 49-page guideline whose text layer was searched entirely but
    whose body was read in sections is not forced to choose between over-claiming
    (`full-text-read`) and misleading (`record-only`). That is only an improvement if the
    row says what the sections were - otherwise it is `full-text-read` with a softer name,
    and the register has gained a hiding place rather than a distinction.

    So a partial read must name its extent: a section or clause reference, or a page
    count. The check is on the SHAPE of the claim, not on particular wording, because
    prescribing the phrasing would just move the problem into the phrasing.
    """
    import re as _re
    extent = _re.compile(
        r"(?:\bs(?:ec|ection)?\.?\s*\d)"      # section 4, s4, sec. 4
        r"|(?:§\s*\d)"                     # a section sign followed by a number
        r"|(?:\b\d+\s*(?:of|/)\s*\d+\s*(?:pp?\.?|pages?)\b)"   # 20 of 49 pages
        r"|(?:\b\d+\s*(?:pp\.?|pages?)\b)"     # 27 pages
        r"|(?:\bAnnex\s+[IVXA-Z0-9])"          # Annex II
        r"|(?:\bTable\s+[A-Z0-9])"             # Table A.2.1
        r"|(?:\bchapter\s+\d)",
        _re.I,
    )
    offenders = []
    for r in load_rows("sources"):
        if (r.get("access") or "").strip() != "partial-text-read":
            continue
        blob = (r.get("notes") or "") + " " + (r.get("verified") or "")
        if not extent.search(blob):
            offenders.append(r["source_key"])
    assert not offenders, (
        "source(s) marked partial-text-read that do not say which part was read. Name the "
        "sections or the page count in notes/verified, or use a different access value: "
        + ", ".join(offenders)
    )


def test_no_full_text_claim_behind_an_unexplained_paywall():
    """A paywalled row may claim full-text-read only if it names the route in.

    This combination is how the glass-transition error hid: the source was
    labelled paywalled while a number was carried from it as though read. The
    inverse — claiming a full read of something recorded as paywalled with no
    open-access mirror, repository, preprint or retrieved-SI route named — is the
    same defect with the fields swapped.
    """
    offenders = []
    for r in load_rows("sources"):
        if (r.get("access") or "").strip() != "full-text-read":
            continue
        reach = (r.get("reachability") or "").lower()
        if "paywall" not in reach:
            continue
        blob = " ".join(v or "" for v in r.values()).lower()
        if not any(tok in blob for tok in _OPEN_ROUTE_TOKENS):
            offenders.append(r["source_key"])
    assert not offenders, (
        "source(s) claiming full-text-read while recorded as paywalled with no "
        "open-access route named: " + ", ".join(offenders)
    )


def test_unread_sources_cited_from_findings_are_on_the_reading_list():
    """A headline finding may not rest on something nobody has read unless it is queued.

    The structural check. Two abstract-only sources were cited from findings pages
    and appeared nowhere on the reading list, so nobody was queued to pull them —
    one of them carrying the pore-distribution claim on the site's most important
    page. This makes that state impossible.
    """
    unread = {
        r["source_key"] for r in load_rows("sources")
        if (r.get("access") or "").strip() in ACCESS_UNREAD
    }
    reading_list = open(
        os.path.join(ROOT, "docs", "sources", "reading-list.md"), encoding="utf-8"
    ).read()

    offenders = []
    for path in sorted(glob.glob(os.path.join(ROOT, "docs", "findings", "*.md"))):
        rel = os.path.relpath(path, ROOT)
        text = open(path, encoding="utf-8").read()
        for key in sorted(set(re.findall(r"SRC-[A-Z0-9-]+", text))):
            if key in unread and key not in reading_list:
                offenders.append(f"{rel} cites {key}")
    assert not offenders, (
        "finding(s) resting on an unread source that is not queued on the reading "
        "list (add it to docs/sources/reading-list.md, or read it and update "
        "`access`): " + "; ".join(offenders)
    )


# ---------------------------------------------------------------------------
# Guards added 2026-09-18 by the revision session. Each encodes a defect the
# evidence dive found or created a risk of: a band stored as a bare point value
# (F-018, F-019), a cross-molecule number transferred without saying so, a source
# left in the "unread" census after it was actually read, and a batch-cycle-time
# figure cited as a residence time (F-002 trap).
# ---------------------------------------------------------------------------

def test_band_parameters_carry_an_explicit_range():
    """A band must not hide as a bare point value, and must say WHAT KIND of band it is.

    REPLACES the version that classified a band by the literal substring 'BAND:' in the
    free-text notes. That classifier was unreliable and could be shown to be: ten rows
    carry a range and only NINE carry the token, because P-YIELD-OVERALL-PUB writes
    'BAND (vendor-published):' with no colon after BAND. The old guard could not see it,
    because it only ever checked one direction - 'flagged but unranged' - and never
    'ranged but unflagged'. A one-directional guard on a two-directional claim, which is
    the failure test_the_unread_census_is_complete already records.

    The classifier is now the `range_kind` COLUMN, and the check runs both ways:
    a range implies a kind, and a kind implies a range. The prose token is still policed
    in the direction it can be wrong (prose claiming a band the columns do not carry),
    but it is no longer what identifies a band.
    """
    from gen.dataio import RANGE_KINDS
    params = load_params()
    offenders = []
    for r in load_rows("parameters"):
        pid = r["param_id"]
        notes = r.get("notes") or ""
        lo = (r.get("range_low") or "").strip()
        hi = (r.get("range_high") or "").strip()
        kind = (r.get("range_kind") or "").strip()
        banded = bool(lo and hi)

        if lo or hi:
            if not banded:
                offenders.append(f"{pid}: only one of range_low/range_high is set")
                continue
            try:
                flo, fhi = float(lo), float(hi)
            except ValueError:
                offenders.append(f"{pid}: range bound is not numeric: {lo!r}, {hi!r}")
                continue
            if flo > fhi:
                offenders.append(f"{pid}: range_low {flo} > range_high {fhi}")
            v = param_value(params, pid)
            if v is not None and not (flo <= v <= fhi):
                offenders.append(f"{pid}: value {v} outside its range [{flo}, {fhi}]")

        # Direction 1 - a range must declare what kind of claim it is. This is the
        # direction nothing checked, and the direction P-YIELD-OVERALL-PUB slipped.
        if banded and not kind:
            offenders.append(
                f"{pid}: carries a range but no range_kind - a band without a kind does not "
                f"say whether it is evidence, an argument, or a commitment")
        # Direction 2 - a kind must have a range to describe.
        if kind and not banded:
            offenders.append(f"{pid}: declares range_kind={kind!r} but carries no range")
        if kind and kind not in RANGE_KINDS:
            offenders.append(
                f"{pid}: range_kind {kind!r} outside {sorted(RANGE_KINDS)}")
        # The legacy prose token, policed only where it can lie: prose asserting a band
        # the columns do not carry. Its ABSENCE no longer means anything.
        if "BAND:" in notes and not banded:
            offenders.append(f"{pid}: notes flag a BAND but range_low/range_high are empty")
    assert not offenders, "band/range defect(s): " + "; ".join(offenders)


def test_an_ich_range_kind_is_not_claimed_without_demonstration():
    """Two range_kind values are ICH terms of art. Using one is a regulatory claim.

    `design_space` means, in ICH Q8(R2)'s own words, a combination of variables "that
    have been DEMONSTRATED to provide assurance of quality" and that is "subject to
    regulatory assessment and approval". `proven_acceptable_range` means a range WE have
    characterised, holding the other parameters constant. Nothing in this concept is
    either: every band here is literature, argument, or a sizing commitment.

    Both sets are EMPTY today and this guard is therefore proven by mutation rather than
    by a live row - the same standing as `not_measurable` in gen/controls.py. It exists so
    that a later slice cannot quietly promote a literature band to a design space, which
    would be the ISA-conformance over-claim in a different register. If a real design space
    is ever established, this guard is what has to be argued with first.
    """
    from gen.dataio import RANGE_KINDS_ICH
    offenders = []
    for r in load_rows("parameters"):
        kind = (r.get("range_kind") or "").strip()
        if kind not in RANGE_KINDS_ICH:
            continue
        prov = (r.get("provenance") or "").strip()
        if prov != "fact":
            offenders.append(
                f"{r['param_id']}: claims ICH term {kind!r} on provenance={prov!r}; an ICH "
                f"range is demonstrated, so it cannot rest on an assumption or an inference")
        if not (r.get("source_key") or "").strip():
            offenders.append(
                f"{r['param_id']}: claims ICH term {kind!r} with no source_key")
    assert not offenders, (
        "parameter(s) claiming an ICH range term without the demonstration it asserts. "
        "Re-examine the claim rather than relaxing this test: " + "; ".join(offenders))


#: Tokens in a source's scale_system that name a molecule class other than our
#: siRNA duplex. A parameter anchored to such a source must acknowledge the transfer.
_FOREIGN_CLASS_TOKENS = (
    "mrna", "messenger rna", "plasmid", "polysialic", "small molecule", "small-molecule",
    "antisense", "single strand", "single-strand", "single-stranded", "gapmer",
    "circular rna", " protein", "mab",
)
#: Tokens in a parameter's own notes that count as acknowledging the transfer.
_TRANSFER_CAVEAT_TOKENS = (
    "mrna", "plasmid", "polysialic", "small molecule", "small-molecule", "antisense",
    "single strand", "single-strand", "single-stranded", "gapmer", "moe", "protein",
    "not our", "not an sirna", "not a duplex", "not a nucleic", "different mol",
    "different molecular", "transfer", "surrogate", "circular rna",
)


def test_cross_molecule_parameters_declare_the_transfer():
    """A parameter whose source names a different molecule class must say so (transferability)."""
    sources = {r["source_key"]: r for r in load_rows("sources")}
    offenders = []
    for r in load_rows("parameters"):
        key = (r.get("source_key") or "").strip()
        if not key or key not in sources:
            continue
        scale = (sources[key].get("scale_system") or "").lower()
        if not any(tok in scale for tok in _FOREIGN_CLASS_TOKENS):
            continue
        notes = (r.get("notes") or "").lower() + " " + (r.get("scale_system") or "").lower()
        if not any(tok in notes for tok in _TRANSFER_CAVEAT_TOKENS):
            offenders.append(
                f"{r['param_id']} cites {key} (scale_system names a different molecule class) "
                f"but its notes state no transfer caveat"
            )
    assert not offenders, "; ".join(offenders)


def test_read_sources_are_not_in_the_unread_census():
    """The reverse of the reading-list guard: a source that WAS read must not still sit
    in the reading list's 'What we have not actually read' census (its first column)."""
    text = open(
        os.path.join(ROOT, "docs", "sources", "reading-list.md"), encoding="utf-8"
    ).read()
    m = re.search(r"##\s*What we have not actually read(.*?)(\n##\s|\Z)", text, re.S)
    assert m, "census section not found in reading-list.md"
    census = m.group(1)
    # First column of each census table row is the unread source: '| [SRC-XXX] | ...'
    listed = re.findall(r"^\|\s*\[(SRC-[A-Z0-9-]+)\]", census, re.M)
    access = {r["source_key"]: (r.get("access") or "").strip() for r in load_rows("sources")}
    offenders = [k for k in listed if access.get(k) not in ACCESS_UNREAD]
    assert not offenders, (
        "source(s) listed in the unread census whose access is actually a full read "
        "(remove them from the census or fix their access): " + ", ".join(offenders)
    )


def test_hbel_stays_a_registered_gap():
    """The health-based exposure limit is blocked on toxicology data that does not exist publicly,
    so its value must stay BLANK and registered against an open question - never invented."""
    params = load_params()
    row = params.get("P-HBEL-DS")
    assert row is not None, "P-HBEL-DS is not registered"
    assert not (row.get("value") or "").strip(), "P-HBEL-DS must have no value (it is a registered gap)"
    assert "Q-" in (row.get("notes") or ""), "P-HBEL-DS must reference an open question"


def test_ccs_cites_the_hbel_method_source():
    """The contamination-control section must cite the HBEL derivation method, not assert a number."""
    text = open(os.path.join(ROOT, "docs", "process", "microbial.md"), encoding="utf-8").read()
    assert "SRC-WHO-TRS1044" in text, "microbial CCS section must cite the HBEL method source"
    assert "P-HBEL-DS" in text, "microbial CCS section must reference the HBEL gap parameter"


def test_md_table_emits_markdown_only():
    """The register tables are Markdown pipe tables (sorted/filtered client-side over the rendered
    HTML), never hand-emitted HTML. Locks in that decision so md_table cannot start emitting tags."""
    from gen.tables import md_table
    # Real register data legitimately contains "<< 1 kDa", "> 0.2 um", "<1 CFU/mL", so a bare
    # "<" check only passed because it was fed hand-picked synthetic rows. Assert no HTML TAGS,
    # and assert it against the actual data the generator runs on.
    # controls.csv and instruments.csv carry the longest free-text notes in the repo, which is
    # exactly where '|' escaping matters most - a single unescaped pipe would split a cell and
    # shift every column after it, silently, on a rendered page nobody diffs.
    for name in ("parameters", "impurities", "streams", "sources", "controls", "instruments"):
        out = md_table(load_rows(name))
        assert not re.search(r"<\s*/?\s*[a-zA-Z][^>]*>", out), (
            f"md_table emitted an HTML tag for {name}.csv; it must emit Markdown pipe tables"
        )
        assert out.lstrip().startswith("|"), f"{name}.csv table is not a pipe table"


def test_table_enhancers_are_registered_and_anchored_outside_the_scroll_wrapper():
    """The sort and filter enhancements must be wired in, AND the filter must be anchored outside
    Material's horizontal scroll container.

    The previous version of this test only grepped mkdocs.yml and called os.path.exists twice, so
    it asserted no behaviour at all - it would have passed with an empty file, and it did pass
    while the filter box was being injected INSIDE `div.md-typeset__scrollwrap`
    (`overflow-x: auto`), where it scrolled out of view on the widest register tables. Verified in
    headless Chromium; this guard keeps the anchoring from regressing to `t.parentNode`.

    Browser check (not a pytest dependency - it needs a live port and a browser):
        mkdocs build && (cd site && python3 -m http.server 8766 &)
        $CHROME --headless --no-sandbox --virtual-time-budget=5000 \\
                --dump-dom http://127.0.0.1:8766/registers/parameters/ > dom.html
    then confirm a `.table-filter` exists and is NOT nested inside `.md-typeset__scrollwrap`.
    Note the page must be served over HTTP: under file:// Material's JS does not run at all, so a
    file-based check would falsely report the filter missing.
    """
    cfg = open(os.path.join(ROOT, "mkdocs.yml"), encoding="utf-8").read()
    for asset in ("javascripts/tablesort.js", "javascripts/tablefilter.js"):
        assert asset in cfg, f"{asset} is not registered in mkdocs.yml extra_javascript"
        assert os.path.exists(os.path.join(ROOT, "docs", asset)), f"missing asset file {asset}"
    js = open(os.path.join(ROOT, "docs", "javascripts", "tablefilter.js"), encoding="utf-8").read()
    assert "md-typeset__scrollwrap" in js, (
        "the filter must anchor on Material's scroll wrapper, or it lands inside the "
        "horizontally-scrolling region and scrolls away on wide tables"
    )
    assert "t.parentNode.insertBefore" not in js, (
        "inserting relative to the table puts the input inside the scroll wrapper"
    )


def test_impurity_classes_are_in_the_clearance_matrix():
    """Every impurity class in the data table must appear in the prose clearance matrix, so the
    numeric overlay and the qualitative matrix cannot drift apart."""
    matrix = open(os.path.join(ROOT, "docs", "process", "filtration.md"), encoding="utf-8").read()
    offenders = []
    for r in load_rows("impurities"):
        key = (r.get("matrix_key") or "").strip()
        if key and key not in matrix:
            offenders.append(f"{r['impurity_id']} ({key})")
    assert not offenders, (
        "impurity class(es) absent from the filtration clearance matrix: " + ", ".join(offenders)
    )


def test_unclearable_impurities_are_not_modelled_as_cleared():
    """Physical fact (filtration finding 1): neither block-internal n-1 nor the adenylylated
    dead-end can be removed by any filtration mode, so neither may be modelled as a downstream
    separation.

    AppN must NOT share the splint's model. The splint is genuinely absent by design (R-006);
    suppressing AppN is a proposed reaction restaging that is not demonstrated for this process,
    and the ATP requirement pulls against the concentration that suppresses it (Q-040). Rendering
    both as "designed out" presented an open gap as a solved problem.
    """
    clearing = {"diafiltration", "particulate", "block_clearable"}
    rows = {r["impurity_id"]: r for r in load_rows("impurities")}
    assert rows["IMP-N1"]["clearance_model"] == "block_floor", \
        "n-1 must be floored (block_floor), never modelled as cleared downstream"
    assert rows["IMP-APPN"]["clearance_model"] == "controlled_at_reaction", \
        "the adenylylated dead-end is suppressed at the reaction, and is NOT 'designed out'"
    assert rows["IMP-APPN"]["clearance_model"] != rows["IMP-SPLINT"]["clearance_model"], \
        "AppN and the splint are not the same kind of claim; see R-010 vs R-006"
    for iid in ("IMP-N1", "IMP-APPN"):
        assert rows[iid]["clearance_model"] not in clearing, f"{iid} modelled as cleared"


def test_impurity_overlay_is_deterministic_and_scenario_free():
    """Impurity fate is a fraction picture, independent of annual demand (Q-002): the overlay is a
    pure function of the parameters, and no throughput-scenario label leaks into it."""
    from gen.impurity import render
    out = render()
    assert out == render()
    for label in ("Low (illustrative)", "Mid (illustrative)", "High (illustrative)"):
        assert label not in out


def test_equipment_turndown_is_populated_or_flagged():
    """Turndown was a fully blank column in Tier 1 - a silent sizing stub. Every equipment
    item must state a turndown basis, or register the gap against an open question (Q-...)."""
    offenders = []
    for r in load_rows("equipment"):
        turndown = (r.get("turndown") or "").strip()
        notes = r.get("notes") or ""
        if not turndown and not re.search(r"Q-\d{3}", notes):
            offenders.append(r["equip_id"])
    assert not offenders, (
        "equipment item(s) with a blank turndown and no open-question reference: "
        + ", ".join(offenders)
    )


def test_equipment_moc_is_committed():
    """Materials of construction must be a decided candidate for every item, never left blank."""
    offenders = [
        r["equip_id"] for r in load_rows("equipment")
        if not (r.get("moc_candidate") or "").strip()
    ]
    assert not offenders, (
        "equipment item(s) with no materials of construction committed: " + ", ".join(offenders)
    )


def test_no_residence_time_cites_a_batch_cycle_time_trap():
    """No page may state a residence time citing a source whose notes TRAP that figure as a
    batch cycle time (F-002). A window that cites such a source next to 'residence time' must
    also carry the correction ('cycle time')."""
    trap_sources = {
        r["source_key"] for r in load_rows("sources")
        if re.search(r"\bTRAP\b", r.get("notes") or "")
    }
    offenders = []
    for path in _doc_files():
        lines = open(path, encoding="utf-8").read().split("\n")
        for i, line in enumerate(lines):
            if "residence time" not in line.lower():
                continue
            window = "\n".join(lines[max(0, i - 3): i + 4])
            if not any(k in window for k in trap_sources):
                continue
            if "cycle time" not in window.lower():
                offenders.append(f"{os.path.relpath(path, ROOT)}:{i + 1}  {line.strip()[:80]}")
    assert not offenders, (
        "residence-time claim(s) citing a batch-cycle-time TRAP source without the correction: "
        + "; ".join(offenders)
    )


def test_impurity_clearance_models_are_a_controlled_vocabulary():
    """A typo in clearance_model must not fall through to a claimed "registered gap".

    sources.csv already established this pattern (ACCESS_VOCAB); the impurity overlay's
    catch-all return made a misspelling render as a confident statement about the process.
    """
    from gen.impurity import CLEARANCE_MODELS
    offenders = [
        f"{r['impurity_id']}: {r['clearance_model']!r}" for r in load_rows("impurities")
        if r["clearance_model"] not in CLEARANCE_MODELS
    ]
    assert not offenders, (
        f"clearance_model outside {sorted(CLEARANCE_MODELS)}: " + "; ".join(offenders)
    )


def test_impurity_gaps_carry_a_registered_reference():
    """A gap must be shown as REGISTERED, so the reader can reach the register entry.

    Three rows used to render "(see notes)" on a page that has no notes column, and they were
    the only cells with no Q/R reference at all - so the page's own claim to show "registered
    gaps" was not delivered.
    """
    from gen.impurity import render
    out = render()
    assert "see notes" not in out, "the impurity page still points at a notes column it lacks"
    for r in load_rows("impurities"):
        if r["clearance_model"] in ("gap", "controlled_at_reaction"):
            ref = (r.get("gap_ref") or "").strip()
            assert re.fullmatch(r"[QR]-\d{3}", ref), (
                f"{r['impurity_id']} is a gap but its gap_ref is {ref!r}"
            )
            assert ref in out, f"{r['impurity_id']}'s registered reference {ref} is not rendered"


# ---------------------------------------------------------------------------
# Tier-3 slice 1: control strategy (data/controls.csv) and instrumentation
# (data/instruments.csv), added 2026-09-21.
#
# The three prose "control strategy anchor points" on the tech-transfer page were
# the CPP->CQA argument, and prose cannot be checked. Nothing in the repo could
# catch a control whose measurement does not exist on the stream it is claimed for,
# and the repo contained exactly that case: Q-042 records that in-line UV saturates
# on a 21-mer at process concentration, while the tech-transfer page advertised
# in-line UV on UF/DF as PAT.
#
# One correction is recorded here because it is instructive. The first version of
# that case said variable-pathlength slope spectroscopy IS at-line, and a guard was
# written to enforce it. That was a false invariant: the technique is used in-line
# (SRC-ROLINGER-2023), and what is actually true is arithmetic about OUR stream
# (test_the_at_line_decision_follows_from_the_arithmetic). A guard is only as good
# as the claim it encodes, and a green suite says nothing about whether that claim
# is true.
#
# Each guard below is written from its invariant, and several were written BEFORE the
# rows they check. That ordering is deliberate: a guard written last gets shaped to fit
# whatever rows already exist, which is the mirror image of the P-DRYGAS-RATIO failure
# (a value tuned until a test passed).
# ---------------------------------------------------------------------------

#: Controlled vocabulary for risks.csv. Neither column was enforced before, so a new
#: risk row could ship an invalid unit_op or category silently and simply never be
#: found by anyone filtering the register.
RISK_UNIT_OPS = {"All", "Cleaning", "Evaporation", "Filtration", "Ligation",
                 "Spray drying", "UF/DF"}
RISK_CATEGORIES = {"formulation", "microbial", "process", "product", "purity", "quality"}


def test_risk_unit_op_and_category_are_a_controlled_vocabulary():
    """A risk filed under a misspelt unit operation or category is invisible to anyone
    filtering the register, and nothing detected that before this guard."""
    offenders = []
    for r in load_rows("risks"):
        if r["unit_op"] not in RISK_UNIT_OPS:
            offenders.append(f"{r['risk_id']}: unit_op {r['unit_op']!r}")
        if r["category"] not in RISK_CATEGORIES:
            offenders.append(f"{r['risk_id']}: category {r['category']!r}")
    assert not offenders, (
        f"risks.csv value(s) outside the vocabulary "
        f"(unit_op {sorted(RISK_UNIT_OPS)}, category {sorted(RISK_CATEGORIES)}): "
        + "; ".join(offenders)
    )


# --- C. The instrument register ---------------------------------------------


def test_instrument_vocabularies_are_controlled():
    """`measured_variable` and `measurement_mode` are controlled for the same reason as
    `access` in sources.csv: a misspelling makes the row invisible to anyone filtering the
    register, and invisible to the in-line guard below - which is the one that carries Q-042."""
    from gen.controls import MEASURED_VARIABLES, MEASUREMENT_MODES
    offenders = []
    for r in load_rows("instruments"):
        if r["measured_variable"] not in MEASURED_VARIABLES:
            offenders.append(f"{r['instrument_id']}: measured_variable {r['measured_variable']!r}")
        if r["measurement_mode"] not in MEASUREMENT_MODES:
            offenders.append(f"{r['instrument_id']}: measurement_mode {r['measurement_mode']!r}")
    assert not offenders, (
        f"instruments.csv value(s) outside the vocabulary (measured_variable "
        f"{sorted(MEASURED_VARIABLES)}, measurement_mode {sorted(MEASUREMENT_MODES)}): "
        + "; ".join(offenders)
    )


def test_measurement_mode_is_never_blank():
    """Stated separately from the vocabulary guard because it is a different invariant: a blank
    would also fail the vocabulary check, but the reason it must not be blank is that the whole
    Q-042 argument is an in-line/at-line distinction. An instrument with no mode cannot take part
    in it, so the register would silently stop carrying the argument."""
    blanks = [r["instrument_id"] for r in load_rows("instruments")
              if not (r.get("measurement_mode") or "").strip()]
    assert not blanks, (
        "instrument(s) with no measurement_mode; the in-line/at-line distinction is the point "
        "of this register (Q-042): " + ", ".join(blanks)
    )


def test_an_in_line_optical_concentration_claim_cites_a_source():
    """An in-line optical concentration reading must be justified, not asserted.

    This guard's ORIGINAL rationale was wrong and is worth recording, because the error is the
    kind this repository exists to catch. It claimed such a reading was impossible - that
    variable-pathlength slope spectroscopy "is at-line, not in-line". That is a property of the
    benchtop SoloVPE, not of the technique: FlowVPE publishes 5 um to 8 mm and is used IN-LINE on
    UF/DF in the peer-reviewed literature (SRC-ROLINGER-2023). The guard's BEHAVIOUR was always
    defensible - demand a citation - so only the reasoning changes here, and it is no longer
    categorical: whether a reading is geometrically possible is arithmetic, and
    test_the_at_line_decision_follows_from_the_arithmetic below checks the arithmetic itself.
    """
    from gen.controls import OPTICAL_CONCENTRATION_VARIABLES
    offenders = []
    for r in load_rows("instruments"):
        if r["measured_variable"] not in OPTICAL_CONCENTRATION_VARIABLES:
            continue
        if r["measurement_mode"] != "in_line":
            continue
        if not (r.get("source_key") or "").strip():
            offenders.append(f"{r['instrument_id']} ({r['measured_variable']} on {r['unit_op']})")
    assert not offenders, (
        "instrument(s) claiming an IN-LINE optical concentration reading with no source "
        "establishing it is geometrically possible on that stream (Q-042, Q-051): "
        + "; ".join(offenders)
    )


def test_the_at_line_decision_follows_from_the_arithmetic():
    """C-013 is `at_line_only` BECAUSE of a number, and this is that number.

    The at-line choice used to rest on a categorical claim about the technique, which was false.
    It now rests on Beer-Lambert against two registered parameters, so it has to stay true by
    construction: if P-CONC-UF falls, or P-VPE-PATHLENGTH-MIN is corrected downward once the
    vendor answers Q-051, an in-line reading becomes possible and C-013 must be re-examined
    rather than left as a stale decision. That is what this test forces.
    """
    from gen.controls import required_pathlength_um, in_line_optical_possible
    params = load_params()

    conc = param_value(params, "P-CONC-UF")
    assert conc, "P-CONC-UF is blank; the at-line decision has no basis"
    band = required_pathlength_um(params, conc)
    assert band is not None, "P-EPS-260 must carry a range for the pathlength arithmetic to run"
    lo, hi = band
    assert lo < hi, f"pathlength band is not ordered: {band}"

    floor = param_value(params, "P-VPE-PATHLENGTH-MIN")
    assert floor, "P-VPE-PATHLENGTH-MIN is blank; nothing to compare the requirement against"

    assert in_line_optical_possible(params, conc) is False, (
        f"the required pathlength band at P-CONC-UF is {lo:.2f}-{hi:.2f} um against a published "
        f"in-line floor of {floor:g} um, so an in-line reading now looks POSSIBLE. C-013 is "
        f"recorded as at_line_only on the opposite finding - re-examine it rather than leaving "
        f"the control type stale (Q-042, Q-051)."
    )

    ctypes = {r["control_id"]: r["control_type"] for r in load_rows("controls")}
    assert ctypes.get("C-013") == "at_line_only", (
        f"C-013 is {ctypes.get('C-013')!r}; the arithmetic above says at_line_only"
    )


def test_instrument_tags_are_unique():
    """A duplicated tag on a P&ID is a drawing error that propagates into the control narrative;
    a free-text tag makes the register unsortable. Both ids and tags must be unique."""
    rows = load_rows("instruments")
    for col in ("instrument_id", "tag"):
        seen = {}
        for r in rows:
            seen.setdefault(r[col], 0)
            seen[r[col]] += 1
        dupes = [k for k, n in seen.items() if n > 1]
        assert not dupes, f"duplicate {col} in instruments.csv: " + ", ".join(sorted(dupes))


def test_instrument_tag_letters_are_legal_in_the_position_they_appear():
    """Tag letters are checked BY POSITION against the declared scheme, not against a list of the
    prefixes that happen to exist.

    The guard this replaced held `(TI|TIC|PI|PIC|FI|FIC|AI|QI|MI|LI|DPI)-\\d{4}` - an allow-list
    derived from the rows already in the file - so it could only ever bless them, and it did: `DPI`
    is wrong (D is a variable MODIFIER and cannot lead; differential pressure is PDI) and the guard
    asserted in its own failure message that the result was "ISA-style". A guard assembled from its
    data cannot find a fault in that data. This one is assembled from gen/controls.py's declared
    letter scheme instead, so a wrong letter fails wherever it appears.

    The scheme is THIS PROJECT'S, not a reproduction of any ISA table: the current edition was not
    retrieved and conformance is an open question (Q-053, SRC-ISA-5-1-2024).
    """
    from gen.controls import tag_letter_error
    offenders = [f"{r['instrument_id']} {r['tag']}: {tag_letter_error(r['tag'])}"
                 for r in load_rows("instruments") if tag_letter_error(r["tag"])]
    assert not offenders, (
        "instrument tag(s) using a letter that is not declared for the position it occupies "
        "(see TAG_FIRST_LETTERS in gen/controls.py, and Q-053): " + "; ".join(offenders)
    )


def test_the_declared_tag_scheme_does_not_claim_to_be_isa():
    """The scheme must say what it is, because saying otherwise is the defect that produced it.

    Every letter in use has to be declared, the two user's-choice assignments have to be marked as
    ours, and nothing in the module may present the table as ISA's - ISA-5.1-2024 is unread and
    reproducing its table here is prohibited anyway.
    """
    from gen.controls import TAG_FIRST_LETTERS, TAG_VARIABLE_MODIFIERS
    src = open(os.path.join(ROOT, "gen", "controls.py"), encoding="utf-8").read()

    used = {r["tag"].split("-")[0][0] for r in load_rows("instruments")}
    missing = sorted(used - set(TAG_FIRST_LETTERS))
    assert not missing, f"first letter(s) in use but not declared: {missing}"

    for letter in ("M", "Q"):
        assert "user's-choice" in TAG_FIRST_LETTERS.get(letter, ""), (
            f"{letter} is a user's-choice letter and must be labelled as this project's own "
            f"assignment, not left looking like a standard one"
        )
    assert "D" in TAG_VARIABLE_MODIFIERS and "D" not in TAG_FIRST_LETTERS, (
        "D must be a variable modifier and never a first letter, or DPI becomes legal again"
    )
    assert "UNVERIFIED" in src and "Q-053" in src, (
        "gen/controls.py must record that conformance to the current ISA edition is unverified"
    )


# --- B/E. The control matrix, and referential integrity across both new files ---

PROVENANCE_VOCAB = {"fact", "inference", "assumption"}


def _refs(value):
    """A reference cell holds one id, or several separated by ';'.

    Two control rows legitimately rest on a PAIR of parameters - the glass transition only means
    something at the moisture it was measured at, and the dryer outlet limit only means something
    against a melting temperature - so a single-valued column would have pushed the second half of
    each pair into free text where nothing could resolve it.
    """
    return [t.strip() for t in (value or "").split(";") if t.strip()]


def _equation_ids():
    text = open(os.path.join(ROOT, "docs", "equations", "index.md"), encoding="utf-8").read()
    return set(re.findall(r"^##\s*(EQ-[A-Z]+)", text, re.M))


def test_control_types_are_a_controlled_vocabulary():
    """Same invariant as CLEARANCE_MODELS: a typo must not fall through to a claimed control."""
    from gen.controls import CONTROL_TYPES
    offenders = [f"{r['control_id']}: {r['control_type']!r}" for r in load_rows("controls")
                 if r["control_type"] not in CONTROL_TYPES]
    assert not offenders, (
        f"control_type outside {sorted(CONTROL_TYPES)}: " + "; ".join(offenders)
    )


def test_control_param_ref_is_conditional_on_control_type():
    """The guard this slice exists for, and the only one with a NEGATIVE case worth proving.

    "Every non-blank param_ref resolves" is too weak: it permits a control row that names no
    parameter at all, which is precisely the defect - a control asserted in prose with nothing
    behind it. So the rule runs both ways.

      * A row that claims to control something (anything but `gap` / `not_measurable`) MUST name
        a parameter, and every id it names must resolve.
      * A `not_measurable` or `gap` row MUST leave param_ref blank. You cannot name the parameter
        for a quantity nobody can measure, and naming one would dress a gap up as a control.
      * A `not_measurable` row must additionally carry a gap reference, so the unmeasurable
        quantity is registered rather than merely asserted.
    """
    from gen.controls import PARAM_FORBIDDEN_TYPES
    params = load_params()
    offenders = []
    for r in load_rows("controls"):
        cid, ctype = r["control_id"], r["control_type"]
        refs = _refs(r.get("param_ref"))
        if ctype in PARAM_FORBIDDEN_TYPES:
            if refs:
                offenders.append(
                    f"{cid}: control_type={ctype} must leave param_ref blank, found {refs}")
            if ctype == "not_measurable" and not _refs(r.get("gap_ref")):
                offenders.append(f"{cid}: not_measurable with no gap_ref")
        else:
            if not refs:
                offenders.append(f"{cid}: control_type={ctype} names no parameter")
            for pid in refs:
                if pid not in params:
                    offenders.append(f"{cid}: param_ref {pid} does not resolve")
    assert not offenders, "control param_ref rule violated: " + "; ".join(offenders)


def test_control_and_instrument_references_resolve():
    """Referential integrity across the two new files.

    Registers that point at each other by free-text id drift the moment one of them is edited;
    the flowsheet already lost an arrow that way in Tier 1. Every cross-reference in these two
    files resolves to a row that exists, or the build fails.
    """
    from gen.flowsheet import SENTINELS
    units = {r["equip_id"] for r in load_rows("equipment")} | set(SENTINELS)
    streams = {r["stream_id"] for r in load_rows("streams")}
    risks = {r["risk_id"] for r in load_rows("risks")}
    questions = {r["question_id"] for r in load_rows("questions")}
    instruments = {r["instrument_id"] for r in load_rows("instruments")}
    equations = _equation_ids()

    offenders = []

    def check(where, label, values, universe):
        for v in values:
            if v not in universe:
                offenders.append(f"{where}: {label} {v} does not resolve")

    for r in load_rows("controls"):
        cid = r["control_id"]
        check(cid, "unit_op", [r["unit_op"]], units)
        check(cid, "equation_ref", _refs(r.get("equation_ref")), equations)
        check(cid, "risk_ref", _refs(r.get("risk_ref")), risks)
        check(cid, "instrument_ref", _refs(r.get("instrument_ref")), instruments)
        check(cid, "gap_ref", _refs(r.get("gap_ref")), questions | risks)
        if r["provenance"] not in PROVENANCE_VOCAB:
            offenders.append(f"{cid}: provenance {r['provenance']!r}")

    for r in load_rows("instruments"):
        iid = r["instrument_id"]
        check(iid, "unit_op", [r["unit_op"]], units)
        check(iid, "stream_ref", _refs(r.get("stream_ref")), streams)
        check(iid, "gap_ref", _refs(r.get("gap_ref")), questions | risks)
        if r["provenance"] not in PROVENANCE_VOCAB:
            offenders.append(f"{iid}: provenance {r['provenance']!r}")

    assert not offenders, "unresolved reference(s): " + "; ".join(offenders)


def test_a_control_that_acts_names_the_instrument_that_enforces_it():
    """A control strategy with no instrument behind it is a sentence, not a control.

    Blank is legitimate for exactly four types: a supplier specification has no in-facility
    instrument, a formulation choice is not an on-line measurement, and a `gap` or a
    `not_measurable` row has by definition nothing enforcing it.
    """
    from gen.controls import INSTRUMENT_OPTIONAL_TYPES
    offenders = [
        f"{r['control_id']} ({r['control_type']})" for r in load_rows("controls")
        if r["control_type"] not in INSTRUMENT_OPTIONAL_TYPES and not _refs(r.get("instrument_ref"))
    ]
    assert not offenders, (
        "control row(s) that act on the process but name no instrument: " + "; ".join(offenders)
    )


def test_every_control_row_carries_an_acceptance_basis_or_a_registered_gap():
    """Never both blank. A row with neither is an empty assertion, and the whole point of this
    slice is that a placeholder must be visible AS a placeholder."""
    offenders = []
    for r in load_rows("controls"):
        basis = (r.get("acceptance_basis") or "").strip()
        gap = _refs(r.get("gap_ref"))
        if not basis and not gap:
            offenders.append(f"{r['control_id']}: no acceptance basis and no gap reference")
        # A basis that states a number must say which registered parameter the number is,
        # for the same reason prose numbers must carry a citation.
        if basis and re.search(r"\d", basis) and not re.search(r"\bP-[A-Z0-9-]{3,}", basis):
            offenders.append(
                f"{r['control_id']}: acceptance_basis states a number with no parameter id")
    assert not offenders, "; ".join(offenders)


def test_control_gaps_render_as_registered_gaps():
    """A `gap` or `not_measurable` row must reach the reader AS a registered gap, with a
    reference they can follow - the same defect the impurity overlay had when three rows said
    "(see notes)" on a page with no notes column."""
    from gen.controls import render
    out = render()
    for r in load_rows("controls"):
        if r["control_type"] not in ("gap", "not_measurable"):
            continue
        for ref in _refs(r.get("gap_ref")):
            assert re.fullmatch(r"[QR]-\d{3}", ref), (
                f"{r['control_id']} is a gap but its gap_ref is {ref!r}")
            assert ref in out, (
                f"{r['control_id']}'s registered reference {ref} is not rendered")


def test_the_matrix_page_renders_its_id_columns():
    """The matrix page is NOT exempt from the prose-citation lint, and it passes that lint
    because every row carries a P-/Q-/R-/EQ- token on its own line. That claim is only true while
    the renderer actually emits the id columns - without this guard it would quietly degrade from
    a property into a coincidence the first time someone tidied the table."""
    from gen.controls import render
    out = render()
    missing = []
    for r in load_rows("controls"):
        tokens = (_refs(r.get("param_ref")) + _refs(r.get("equation_ref"))
                  + _refs(r.get("gap_ref")) + _refs(r.get("risk_ref"))
                  + _refs(r.get("instrument_ref")))
        assert tokens, f"{r['control_id']} carries no reference of any kind"
        for t in tokens:
            if t not in out:
                missing.append(f"{r['control_id']}: {t}")
    assert not missing, (
        "reference(s) present in controls.csv but not rendered on the matrix page: "
        + "; ".join(missing)
    )


def test_control_matrix_is_deterministic_and_scenario_free():
    """Control strategy is a set of limits and does not move with annual demand (Q-002)."""
    from gen.controls import render
    a, b = render(), render()
    assert a == b, "gen.controls.render() is not deterministic"
    for scn in load_rows("scenarios"):
        assert scn["label"] not in a, (
            f"the control matrix mentions scenario {scn['label']!r}; it must be scenario-free")


def test_the_enzyme_fork_renders_as_a_fork_and_not_as_a_decision():
    """Enzyme form is undecided (Q-050) and the register must not quietly decide it.

    Both clearance branches must render, both with a BLANK acceptance basis and a live gap
    reference, and neither may read as the selected route. This is the guard that keeps the
    'decisions taken' from becoming a decision nobody took.
    """
    from gen.controls import render
    out = render()
    branches = [r for r in load_rows("controls") if r["control_type"] == "downstream_removal"]
    assert len(branches) >= 2, (
        "enzyme clearance must be carried as TWO branches, neither asserted as chosen")
    for r in branches:
        cid = r["control_id"]
        assert not (r.get("acceptance_basis") or "").strip(), (
            f"{cid}: an enzyme-clearance branch must have a BLANK acceptance basis - "
            f"P-ENZ-CLEARANCE-LRV is blank for both branches (Q-032)")
        refs = _refs(r.get("gap_ref"))
        assert refs, f"{cid}: enzyme-clearance branch with no gap reference"
        for ref in refs:
            assert ref in out, f"{cid}: gap reference {ref} is not rendered"
    assert "Q-050" in out, "the matrix must show that enzyme form is open (Q-050)"


def test_enzyme_parameters_stay_registered_gaps():
    """P-HBEL-DS has a guard stopping anyone from quietly filling in a value the world does not
    have. These two need the same protection and for a sharper reason: a number in either one
    would silently CHOOSE an enzyme form, and enzyme form is the open question (Q-050) the whole
    clearance argument forks on.

    P-LIG-ENZ-LOAD: the only cited loading is a cell-free-extract loading, i.e. a whole proteome.
    P-ENZ-CLEARANCE-LRV: no ppm, log-reduction or immunoassay figure exists publicly for EITHER
    branch, which is what makes the chromatography-free thesis unproven rather than proven.
    """
    params = load_params()
    for pid in ("P-LIG-ENZ-LOAD", "P-ENZ-CLEARANCE-LRV"):
        row = params.get(pid)
        assert row is not None, f"{pid} is not registered"
        assert not (row.get("value") or "").strip(), (
            f"{pid} must have no value - it is a registered gap, and a value in it would decide "
            f"Q-050 by implication")
        assert "Q-050" in (row.get("notes") or ""), (
            f"{pid} must reference the enzyme-form question it is blocked by")


def test_the_clarification_item_stays_branch_aware():
    """U02-CF's sizing basis and notes used to presume an immobilised enzyme ("or centrifuge if
    immobilised enzyme"), which presupposed the answer to Q-050 in the equipment register while
    the question register called it open. Both fields must now name the fork, so the register
    cannot drift back to presuming one branch.

    It must also keep saying that the 85 C denature hold the soluble branch needs has NO unit
    here: this item is single-use depth media. That absence is registered rather than invented,
    because adding the vessel would half-commit to a branch nobody has chosen.
    """
    row = [r for r in load_rows("equipment") if r["equip_id"] == "U02-CF"]
    assert row, "U02-CF is not in the equipment register"
    row = row[0]
    blob = row["sizing_basis"] + " " + row["notes"]
    for tok in ("Q-050", "R-021", "R-002", "R-017"):
        assert tok in blob, f"U02-CF must reference {tok} to stay branch-aware; it does not"
    assert "Q-050" in row["sizing_basis"], (
        "U02-CF's SIZING BASIS must name the fork too - the notes alone let the sizing argument "
        "quietly keep presuming one branch")


def test_no_equipment_item_performs_the_denature_hold_while_q050_is_open():
    """The soluble branch of Q-050 needs a heated vessel or exchanger that is not in this concept.

    The failure mode this guards is subtle: someone reads the soluble branch, notices it needs a
    thermal step, and attaches that duty to the nearest existing item rather than registering the
    gap - which would make an unchosen branch look executable, and would put an 85 C duty on
    single-use depth media.

    The rule is deliberately CONDITIONAL on Q-050 still being open, not permanent. Once the
    enzyme form is actually chosen, a denature unit is the right thing to add and this guard
    stands aside on its own; what it refuses is a unit that appears while the question that would
    justify it is unanswered. It scans `name` and `unit_op` rather than the prose fields, because
    an item that performs the hold is NAMED for it - the prose fields are where the register
    legitimately says the opposite.
    """
    q050 = [r for r in load_rows("questions") if r["question_id"] == "Q-050"]
    assert q050, "Q-050 is not registered"
    if q050[0]["status"] != "open":
        return  # the fork has been resolved; a denature unit is now a legitimate entry
    offenders = [r["equip_id"] for r in load_rows("equipment")
                 if re.search(r"denatur|heat.kill", r["name"] + " " + r["unit_op"], re.I)]
    assert not offenders, (
        "equipment item(s) performing the enzyme denature hold while Q-050 - which decides "
        "whether that step exists at all - is still open: " + ", ".join(offenders)
    )


# ---------------------------------------------------------------------------
# Tier-3 slice 2: the process flow diagrams (gen/pfd.py), added 2026-09-25.
#
# docs/diagrams/index.md promised "a stream-numbered process flow diagram (PFD) with
# instrument tags" in a "Not yet drawn" admonition, and three other pages - both front
# pages among them - carried the same claim. The instruments existed as a register but
# nothing drew them, so nothing could catch a drawing that contradicted the register.
#
# The invariant these guards protect is that the drawing is DERIVED, never decorated.
# In particular the difference between a control loop and a laboratory result has to fall
# out of measurement_mode and the declared tag letters, because that distinction is the
# whole content of the Q-042 case and C-013 is the row that must not look like a control.
# Deriving it from `controls.instrument_ref` instead would have been an enumeration of the
# rows that happen to exist - the DPI mistake again - and would also have been WRONG:
# nine tags declare control and only two are in that register (Q-056).
# ---------------------------------------------------------------------------

PFD_DIR = os.path.join(ROOT, "docs", "diagrams")


def _pfd_path(unit):
    return os.path.join(PFD_DIR, "pfd-" + unit.lower() + ".svg")


def _generated_svgs():
    """Every generated SVG in the repository: the BFD and one PFD per unit operation."""
    from gen.pfd import UNITS
    return ([os.path.join(PFD_DIR, "bfd.svg")]
            + [_pfd_path(u) for u in UNITS])


def test_pfd_is_up_to_date():
    """Each committed PFD must equal render_svg(); same contract as the BFD at :344.

    CI runs the drift tests BEFORE gen.build regenerates anything, so a stale committed SVG
    would otherwise pass every other guard here while showing the wrong picture.
    """
    from gen.pfd import UNITS, render_svg
    stale = []
    for unit in UNITS:
        path = _pfd_path(unit)
        if not os.path.exists(path):
            stale.append(f"{unit}: docs/diagrams/pfd-{unit.lower()}.svg is missing")
            continue
        if open(path, encoding="utf-8").read() != render_svg(unit):
            stale.append(unit)
    assert not stale, (
        "process flow diagram(s) stale or missing; run `python -m gen.build` and commit the "
        "result: " + ", ".join(stale)
    )


def test_pfd_layout_is_deterministic():
    """The generator must be a pure function of the data, drawings and host page alike."""
    from gen.pfd import UNITS, render_page, render_svg
    for unit in UNITS:
        assert render_svg(unit) == render_svg(unit), f"{unit} render is not deterministic"
    assert render_page() == render_page()


def test_every_instrument_is_drawn_on_its_unit_pfd():
    """Set equality per unit op, both directions - the lesson of the lost product arrow.

    One direction catches an instrument silently dropped from a drawing. The other catches a
    tag drawn on a unit that does not own it, which a "count the bubbles" check would miss.
    Deliberately NOT an allow-list built from the tags already drawn.
    """
    from gen.pfd import UNITS, render_svg
    registered = {}
    for r in load_rows("instruments"):
        registered.setdefault(r["unit_op"], set()).add(r["tag"])

    offenders = []
    for unit in UNITS:
        svg = render_svg(unit)
        # Tags render as two text elements, the letters and the four digits, so recombine.
        drawn = set(re.findall(r'class="tag"[^>]*>([A-Z]{2,4})</text>\s*'
                               r'<text class="tag"[^>]*>(\d{4})</text>', svg))
        drawn = {f"{a}-{b}" for a, b in drawn}
        want = registered.get(unit, set())
        for tag in sorted(want - drawn):
            offenders.append(f"{unit}: {tag} is registered but not drawn")
        for tag in sorted(drawn - want):
            offenders.append(f"{unit}: {tag} is drawn but not registered on this unit")
    assert not offenders, "PFD/instrument-register mismatch: " + "; ".join(offenders)


def test_a_tag_that_declares_control_is_a_loop_capable_measurement():
    """A tag may not claim control while its reading comes off a withdrawn sample.

    The contradiction this forbids is the Q-042 case wearing the opposite mask: a loop cannot
    close on a sample somebody carried to a bench, so a `C` in the output position together
    with an at-line or off-line mode is a data error, not a loop to draw. Stated over the mode
    VOCABULARY rather than over the rows: `on_line` counts as loop-capable (a sample is
    diverted automatically and may be returned), so an automated sampler closing a loop is
    permitted and only a human-carried sample is refused. That is the premise, and it is the
    one that would have to change for this guard to be wrong.
    """
    from gen.controls import LOOP_CAPABLE_MODES, tag_declares_control
    offenders = [
        f"{r['instrument_id']} {r['tag']} is {r['measurement_mode']}"
        for r in load_rows("instruments")
        if tag_declares_control(r["tag"]) and r["measurement_mode"] not in LOOP_CAPABLE_MODES
    ]
    assert not offenders, (
        "instrument tag(s) declaring a control function on a reading no loop can close on - "
        f"the loop-capable modes are {sorted(LOOP_CAPABLE_MODES)}. Either the tag should not "
        "carry a control letter or the mode is wrong (Q-042, Q-056): " + "; ".join(offenders)
    )


def test_the_loop_rendering_follows_from_the_tag_and_the_mode():
    """Which bubbles get an actuator arrow is COMPUTED, and this is the computation.

    Written in the shape of test_the_at_line_decision_follows_from_the_arithmetic (:1025): the
    invariant is derived from the registers through the generator's own public function, then
    the drawing is checked against it. So if a tag gains a control letter, or a mode is
    corrected, the drawing has to move with it or this fails.

    C-013's instrument is asserted separately and deliberately. It is the row this repository
    built the at_line_only control type for, and the one that must never acquire an actuator
    arrow; it currently qualifies on two independent counts (at-line mode, no control letter),
    and this pins BOTH rather than trusting either alone.
    """
    from gen.pfd import UNITS, loop_state, render_svg
    instruments = load_rows("instruments")
    by_unit = {}
    for r in instruments:
        by_unit.setdefault(r["unit_op"], []).append(r)

    offenders = []
    for unit in UNITS:
        svg = render_svg(unit)
        expected_closed = sorted(r["tag"] for r in by_unit.get(unit, [])
                                 if loop_state(r) == "closed")
        drawn_actuators = len(re.findall(r'class="act"', svg))
        if drawn_actuators != len(expected_closed):
            offenders.append(
                f"{unit}: {drawn_actuators} actuator arrow(s) drawn but "
                f"{len(expected_closed)} closed loop(s) computed {expected_closed}")
        expected_dashed = sorted(r["tag"] for r in by_unit.get(unit, [])
                                 if loop_state(r) == "withdrawn")
        drawn_dashed = len(re.findall(r'class="bubw"', svg))
        if drawn_dashed != len(expected_dashed):
            offenders.append(
                f"{unit}: {drawn_dashed} dashed ring(s) drawn but "
                f"{len(expected_dashed)} withdrawn measurement(s) computed")
    assert not offenders, (
        "the PFD's loop rendering no longer follows from measurement_mode and the declared tag "
        "letters - re-examine which is wrong rather than adjusting this test: "
        + "; ".join(offenders)
    )

    c013 = [r for r in load_rows("controls") if r["control_id"] == "C-013"]
    assert c013, "C-013 is not registered"
    ref = c013[0]["instrument_ref"].strip()
    row = [r for r in instruments if r["instrument_id"] == ref]
    assert row, f"C-013 names instrument {ref!r}, which does not resolve"
    assert loop_state(row[0]) == "withdrawn", (
        f"C-013's instrument {ref} ({row[0]['tag']}) renders as "
        f"{loop_state(row[0])!r}, so the open loop would be drawn as a control. It is "
        f"at_line_only BECAUSE no loop can close on it (Q-042) - re-examine the row."
    )
    from gen.controls import tag_declares_control
    assert not tag_declares_control(row[0]["tag"]), (
        f"C-013's instrument tag {row[0]['tag']} now declares a control function, which "
        f"contradicts control_type=at_line_only"
    )


def test_pfd_instrument_stream_refs_touch_their_unit():
    """A stream_ref must name a stream the instrument's own unit actually touches.

    This is what makes a per-unit drawing well defined: a bubble is placed on one of its unit's
    own stream lanes, so a stream_ref pointing somewhere else has nowhere to go and would be
    drawn against an unrelated line. DEXPI Process 1.0 section 2.8.2 puts a sensing point "on a
    stream or a unit operation", and a blank stream_ref is therefore legal - it attaches to the
    unit - but a WRONG one is not.
    """
    streams = {r["stream_id"]: r for r in load_rows("streams")}
    offenders = []
    for r in load_rows("instruments"):
        ref = (r["stream_ref"] or "").strip()
        if not ref:
            continue
        s = streams.get(ref)
        if s is None:
            offenders.append(f"{r['instrument_id']}: stream_ref {ref} does not resolve")
        elif r["unit_op"] not in (s["from_unit"], s["to_unit"]):
            offenders.append(
                f"{r['instrument_id']} ({r['tag']}) is on {r['unit_op']} but {ref} runs "
                f"{s['from_unit']}->{s['to_unit']}")
    assert not offenders, (
        "instrument(s) whose stream_ref names a stream their unit operation does not touch, so "
        "the bubble cannot be placed: " + "; ".join(offenders)
    )


def test_svg_element_ids_are_globally_unique():
    """Marker ids must not collide across the generated SVGs.

    bfd.svg uses bare ids (`arrow`, `warr`, `uarr`). The PFD pages inline seven more SVGs on the
    same site, and duplicate ids across inlined documents make `url(#arrow)` resolve to whichever
    came first - arrowheads silently repainted in another diagram's colour. The PFDs therefore
    namespace theirs per unit, and this keeps it that way.
    """
    seen = {}
    offenders = []
    for path in _generated_svgs():
        rel = os.path.relpath(path, ROOT)
        for ident in re.findall(r'\sid="([^"]+)"', open(path, encoding="utf-8").read()):
            if ident in seen:
                offenders.append(f"{ident!r} in both {seen[ident]} and {rel}")
            else:
                seen[ident] = rel
    assert not offenders, (
        "duplicate SVG element id(s) across generated diagrams; they collide when both are "
        "inlined on one page: " + "; ".join(offenders)
    )


def test_every_generated_svg_is_well_formed_xml():
    """Registered text reaches these drawings, and registered text contains ampersands.

    equipment.csv holds "Buffer preparation & hold suite". Interpolated raw that is not
    well-formed XML, and gen/flowsheet.py has no escaping helper at all - it escapes nothing and
    survives only because UNIT_LABELS happens to override every unit it draws. So this is a live
    defect the moment a generator puts a registered `name` on a drawing, not a hypothetical one.
    """
    import xml.etree.ElementTree as ET
    offenders = []
    for path in _generated_svgs():
        try:
            ET.fromstring(open(path, encoding="utf-8").read())
        except ET.ParseError as exc:
            offenders.append(f"{os.path.relpath(path, ROOT)}: {exc}")
    assert not offenders, (
        "generated SVG(s) that are not well-formed XML - check that every interpolated CSV "
        "field goes through an escape helper: " + "; ".join(offenders)
    )


def test_the_pfd_legend_describes_the_actual_styles():
    """Same guard as the BFD's at :364, for the same reason: a legend is a claim.

    The BFD's legend was inherited from a hand-drawn file and two of its three claims were
    false. These legends are generated from the start, so they get checked from the start.
    """
    from gen.pfd import UNITS, render_svg
    offenders = []
    for unit in UNITS:
        svg = render_svg(unit)
        if "dashed ring = withdrawn sample" not in svg:
            offenders.append(f"{unit}: legend no longer explains the dashed ring")
        bubw = re.search(r"\.bubw \{[^}]*\}", svg)
        if not bubw or "stroke-dasharray" not in bubw.group(0):
            offenders.append(f"{unit}: legend says DASHED ring, but .bubw is {bubw and bubw.group(0)}")
        act = re.search(r"\.act \{[^}]*\}", svg)
        if "Teal arrow to the unit box" in svg and (not act or "#00897b" not in act.group(0)):
            offenders.append(f"{unit}: legend says teal actuator, but .act is {act and act.group(0)}")
    assert not offenders, "PFD legend contradicts the emitted CSS: " + "; ".join(offenders)


def test_the_pfd_does_not_claim_a_standard_symbol_set():
    """The drawings must say whose symbols they are, because nobody's standard was read.

    ISO 10628-1:2014 is the standard that specifies BFD and PFD content and it is NOT retrieved
    (SRC-ISO-10628-1); DEXPI supplies the principle but its own section 6 says the presentation
    layer needs further work; ISA-5.1-2024 is unread and un-reproducible (Q-053). So a drawing
    that implied conformance would be asserting something nobody here has checked - the exact
    defect that produced the tag scheme's "ISA-style" failure message.
    """
    from gen.pfd import UNITS, render_svg
    src = open(os.path.join(ROOT, "gen", "pfd.py"), encoding="utf-8").read()
    for unit in UNITS:
        svg = render_svg(unit)
        assert "this project" in svg and "own" in svg, (
            f"{unit}: the drawing must state that the symbol set is this project's own")
        assert "Q-054" in svg, f"{unit}: the drawing must cite the symbol-set question Q-054"
        assert not re.search(r"\bISA[- ]?5\.1\b(?!.*not)", svg), (
            f"{unit}: the drawing must not present its symbols as ISA-5.1")
    assert "Q-055" in src and "Q-054" in src, (
        "gen/pfd.py must record the symbol-set and final-control-element gaps")


def test_csv_line_endings_match_the_declared_convention():
    """Line endings are a convention here, and an editing tool will silently rewrite them.

    Ten of the twelve CSVs are CRLF and two are LF. Nothing enforced it, so a generated or
    rewritten file could flip wholesale and show as a diff on every line - which buries the one
    row that actually changed, and is exactly how a real edit gets reviewed without being read.
    The rule is per-file, taken from the file itself: every line ends the same way.
    """
    lf_only = {"streams.csv", "scenarios.csv"}
    offenders = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "*.csv"))):
        name = os.path.basename(path)
        raw = open(path, "rb").read()
        lines = raw.count(b"\n")
        crs = raw.count(b"\r")
        if name in lf_only:
            if crs:
                offenders.append(f"{name}: expected LF only, found {crs} CR byte(s)")
        elif crs != lines:
            offenders.append(f"{name}: {crs} CR byte(s) for {lines} line(s) - mixed endings")
    assert not offenders, (
        "CSV line-ending convention broken (10 files CRLF, streams.csv and scenarios.csv LF); "
        "re-save preserving the file's own endings: " + "; ".join(offenders)
    )


def test_generator_symbols_named_in_the_registers_exist():
    """A register that cites a code symbol must cite one that is really there.

    Q-053 and two source rows pointed at `gen/controls.py TAG_LETTERS` for the whole slice-1
    cycle. No such name exists - it is TAG_FIRST_LETTERS - so a reader following the citation
    found nothing, and no guard noticed because nothing checked prose against code.
    """
    offenders = []
    for csv_name in ("questions", "sources", "parameters", "risks", "controls", "instruments"):
        for row in load_rows(csv_name):
            blob = " ".join(v or "" for v in row.values())
            for module, symbol in re.findall(r"gen/(\w+)\.py\s+([A-Z][A-Z0-9_]{3,})", blob):
                path = os.path.join(ROOT, "gen", module + ".py")
                if not os.path.exists(path):
                    offenders.append(f"{csv_name}: gen/{module}.py does not exist")
                elif not re.search(rf"^{symbol}\s*=", open(path, encoding="utf-8").read(), re.M):
                    offenders.append(
                        f"{csv_name}: cites gen/{module}.py {symbol}, which is not defined there")
    assert not offenders, (
        "register(s) citing a generator symbol that does not exist: " + "; ".join(sorted(set(offenders)))
    )


def test_the_unread_census_is_complete():
    """The census claims to cover EVERY unread source, so it has to.

    STRENGTHENS test_read_sources_are_not_in_the_unread_census (:696), which only ever checked
    one direction - that a source listed in the census really is unread. Nothing checked the
    direction the page's own prose promises: "it covers every source in the register whose
    `access` is abstract only, record only or not retrieved". That claim was FALSE when this
    guard was written. Three sources added in Tier-3 slice 1 - SRC-BHANGALE-2022 and the two
    ISA documents - were unread and absent from the census, and the page asserted their
    absence meant nothing was missing. A one-directional guard on a two-directional claim is
    how that shipped, which is the general lesson worth keeping.
    """
    unread = {
        r["source_key"] for r in load_rows("sources")
        if (r.get("access") or "").strip() in ACCESS_UNREAD
    }
    text = open(
        os.path.join(ROOT, "docs", "sources", "reading-list.md"), encoding="utf-8"
    ).read()
    m = re.search(r"##\s*What we have not actually read(.*?)(\n##\s|\Z)", text, re.S)
    assert m, "census section not found in reading-list.md"
    listed = set(re.findall(r"^\|\s*\[(SRC-[A-Z0-9-]+)\]", m.group(1), re.M))
    missing = sorted(unread - listed)
    assert not missing, (
        "unread source(s) absent from the census in docs/sources/reading-list.md, which claims "
        "to cover every one of them - add a row for each, or read it and correct its `access`: "
        + ", ".join(missing)
    )


def test_no_published_page_claims_the_tag_scheme_is_isa():
    """The ISA claim has to be refused on the SITE, not only inside gen/controls.py.

    test_the_declared_tag_scheme_does_not_claim_to_be_isa (:1096) reads gen/controls.py and
    nothing else, so it could not see that docs/techtransfer/index.md went on describing the
    register as carrying "an ISA-style tag" for the whole of slice 1 - the exact phrase that
    slice removed from the guard's own failure message, still published one directory away.
    A guard scoped to the file where a claim was FIXED cannot find the copies that survived,
    which is the general lesson: sweep for the marker everywhere it can publish.

    Naming ISA is fine and necessary - Q-053 and the source rows must be able to say what the
    scheme is NOT based on. What is refused is the claim of resemblance or conformance.
    """
    offenders = []
    for path in _doc_files():
        rel = os.path.relpath(path, ROOT)
        for n, line in enumerate(open(path, encoding="utf-8"), start=1):
            if re.search(r"ISA[- ]?(?:style|compliant|conformant|conforming)", line, re.I):
                offenders.append(f"{rel}:{n}")
            if re.search(r"(?:per|to|follows|following|according to)\s+ANSI/ISA-5\.1(?!\s*(?:is|edition))",
                         line, re.I):
                offenders.append(f"{rel}:{n}")
    assert not offenders, (
        "published page(s) presenting the instrument tag scheme as ISA's. It is this project's "
        "own and conformance to the current edition is unverified (Q-053); ISA-5.1-2024 and "
        "ISA-TR5.1.02-2024 are unread and may not be reproduced: " + ", ".join(offenders)
    )


# ---------------------------------------------------------------------------
# Tier-3 slice 3: the ligation design envelope (gen/envelope.py), added 2026-09-25.
#
# Three claims this repository was making could not be checked while they were prose, and every
# one of them had already failed silently:
#
#   * that a band's two endpoints were two INDEPENDENT citations. `parameters.csv` carries one
#     `source_key` per row, so a range whose ends came from one document looked identical to one
#     bracketed by two. `P-BLOCK-PUR` was that defect at its worst - both ends from one patent, one
#     of them a 6.00 g bench datum sitting inside a band labelled 145-258 g, and its point value a
#     YIELD misread as a purity.
#   * that a set of bands describes a REGION. Two parameters can each sit inside their band while
#     the corner they form together is unreachable.
#   * that an information requirement was ANCHORED. Almost none is, for an enzymatic step: `enzym`
#     and `biocatal` return zero hits across ICH Q11 and Q7.
#
# The acceptance panel then found the same class of defect in the slice that introduced the guards
# against it - four checklist rows citing an ICH Q11 "s4.3" that does not exist, and two envelope
# rows whose verdict claimed a measured endpoint their own notes denied. Both holes are now closed
# by the guards below, which is why several of them check a row against ITS OWN data rather than
# against a vocabulary.
# ---------------------------------------------------------------------------

def test_the_new_registers_pass_their_own_vocabularies():
    """One call, because gen/envelope.py raises with every problem it found rather than the first.

    Strict on vocabulary for the reason gen/controls.py gives: a typo must not fall through to a
    confident statement about the process. What makes this more than a spell-check is the set of
    cross-checks inside it - a verdict that contradicts its own endpoints, a point value with no
    argument behind it, an anchor clause its own source row never records reading.
    """
    from gen.envelope import validate
    validate()


def test_a_refused_bracket_is_not_written_as_a_range():
    """The user's standing rule, made mechanical.

    A bracket that fails the two-independent-endpoints test does not get written as a range: the
    parameter keeps a blank or a clearly-labelled single point, and the failure becomes a registered
    question naming what second source would fix it. So a `not_a_range` verdict in envelopes.csv and
    a numeric range in parameters.csv are a direct contradiction between two registers.

    The live case is the ligation concentration, whose two ends are a demonstrated SUCCESS and a
    reported FAILURE - different kinds of claim, so no width between them is a window of operation.
    """
    from gen.envelope import range_written_where_refused
    offenders = range_written_where_refused()
    assert not offenders, (
        "parameter(s) carrying a range that envelopes.csv rules is not one; blank the range and "
        "register the question instead: " + "; ".join(offenders)
    )


def test_every_band_has_an_endpoint_audit():
    """A number a reader can use must say whether its two ends are two claims or one.

    Added after the acceptance panel pointed out that `one_source_both_ends` was disclosed only in
    envelopes.csv, so the disclosure never reached whoever read the band off the parameter register.
    The fix is not a second column - carrying a relation on both sides lets the two disagree with
    nothing to detect it, which is why instruments.csv has no `control_loop` column. It is to
    require that the audit EXISTS and to render it beside the parameter at build time.

    One-directional on purpose: three envelope rows legitimately have no parameter counterpart, and
    two of them exist precisely to record spans that must NOT be written as ranges.
    """
    from gen.envelope import unaudited_bands
    offenders = unaudited_bands()
    assert not offenders, (
        "band(s) in parameters.csv with no endpoint audit in envelopes.csv: " + "; ".join(offenders)
    )


def test_no_design_intent_band_spans_an_unreachable_corner():
    """ICH Q8(R2) Appendix 2 sanctions an INSCRIBED box, never a circumscribed one.

    Where one parameter's acceptable range depends on another's, an applicant may report the true
    curved region or a smaller box - and every corner of that box has to be simultaneously
    attainable. A box drawn round the region claims operation at corners nobody has reached.

    No live row trips this, and that is expected rather than a weakness: the only `design_intent`
    band in the register is the evaporator's, which no coupling touches. Its evidence is the
    mutation case, the same standing as `not_measurable` in gen/controls.py - kept because the
    distinction is real and the next such case needs it.
    """
    from gen.envelope import corner_rule_offenders
    offenders = corner_rule_offenders()
    assert not offenders, (
        "design_intent band(s) spanning a corner a coupling declares unreachable: "
        + "; ".join(offenders)
    )


def test_no_published_page_presents_the_panel_as_qualified_signoff():
    """The panel is four reviews this project ran itself. It is not a sign-off, and no page may read
    as though it were.

    In the idiom of test_no_published_page_claims_the_tag_scheme_is_isa (:1893), and for the same
    reason: a claim fixed in one file survives one directory away, so the sweep has to run over
    everything that publishes. It matches claim SHAPES rather than vocabulary, and it carves out any
    line carrying a negation - because saying what the panel is NOT has to stay sayable, and a guard
    that refused the disclaimer would create pressure to delete it.

    Four independent REJECTs on four different questions are a publishable result. A package that
    reads as though it had been signed off is a misrepresentation, and a worse one than any single
    wrong number, because it invites a reader to stop checking.
    """
    from gen.envelope import signoff_claim_offenders
    offenders = signoff_claim_offenders(_doc_files())
    assert not offenders, (
        "published page(s) presenting the acceptance panel as qualified engineering sign-off. It is "
        "this project's own role-based review, run by four reviewers who could not see each other, "
        "and it approves nothing: " + "; ".join(os.path.relpath(o, ROOT) for o in offenders)
    )


def test_the_panel_publishes_disagreement_rather_than_a_consensus():
    """Disagreement is published, not reconciled - so the page must show every verdict.

    The failure mode is a summary that averages four reviews into a tone. Each reviewer's verdict,
    their single binding blocker and what would change it must all reach the page, and each blocker
    must resolve to a question this repository already tracks - otherwise the panel is generating
    new work rather than judging the register it was given.
    """
    from gen.envelope import render
    out = render()
    rows = load_rows("verdicts")
    assert rows, "the acceptance panel register is empty"
    qids = {r["question_id"] for r in load_rows("questions")}
    for r in rows:
        assert r["blocker_ref"] in qids, (
            f"{r['verdict_id']}: blocker {r['blocker_ref']} is not a registered question")
        assert r["blocker_ref"] in out, f"{r['verdict_id']}'s blocker is not rendered"
        assert r["verdict"] in out, f"{r['verdict_id']}'s verdict is not rendered"
        assert r["reviewer_role"] in out, f"{r['verdict_id']}'s role is not rendered"
    blockers = {r["blocker_ref"] for r in rows}
    assert len(blockers) > 1 or len(rows) == 1, (
        "every reviewer named the same blocker, which is a result worth stating explicitly rather "
        "than one to assert by accident - check the panel really ran independently")


# Not every CSV gets a register page: two are published as part of a wider page instead.
# Each entry says WHERE (the relpath gen/build.py writes), WHICH generator produces it (an
# attribute of gen.build), and WHICH column that generator actually prints. All three are
# checked, so an exemption is earned by the generator's output rather than granted by being
# listed here.
_PUBLISHED_ELSEWHERE = {
    # The overlay renders each impurity by NAME, not by id - so the column checked here is
    # the one the page actually shows. Checking `impurity_id` looked right and was wrong,
    # which is the argument for proving an exemption instead of listing it.
    "impurities": ("balance/impurities.md", "render_impurities", "name"),
    "scenarios": ("balance/results.md", "render_balance", "label"),
}


def test_every_data_csv_is_published_somewhere():
    """A register that exists as data and nowhere on the site is invisible, not private.

    Written because four CSVs were in exactly that state: `envelopes`, `couplings`,
    `infoneeds` and `verdicts` were committed, guarded and read by the generator, and a
    reader could not browse any of them - the envelope was in the repository and nowhere on
    the published site. Nothing caught it, because no test related the set of data files to
    the set of pages.

    The rule is derived from the two sets rather than enumerated: every `data/*.csv` must
    either have a register spec in gen/build.py, or be named in _PUBLISHED_ELSEWHERE with a
    generator that is wired to a page and demonstrably prints its rows.

    The evidence is the **generator's return value**, not a file on disk. The first version
    of this guard checked that the page existed under `docs/`, which passed locally and
    failed in CI: those pages are generated and gitignored, and CI runs pytest before
    `python -m gen.build`. A test that asserts on a build artefact is testing the order of
    the last two commands someone ran.
    """
    import gen.build as build
    src = open(os.path.join(ROOT, "gen", "build.py"), encoding="utf-8").read()
    spec_named = set(re.findall(r'^\s*\("([a-z]+)",\s*"registers/', src, re.M))
    offenders = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "*.csv"))):
        name = os.path.basename(path)[:-4]
        if name in spec_named:
            continue
        if name not in _PUBLISHED_ELSEWHERE:
            offenders.append(
                f"{name}.csv has no register spec in gen/build.py and is not declared in "
                f"_PUBLISHED_ELSEWHERE - it is committed data that no page shows")
            continue
        rel, fn, id_col = _PUBLISHED_ELSEWHERE[name]
        renderer = getattr(build, fn, None)
        if renderer is None:
            offenders.append(
                f"{name}.csv names generator {fn}(), which gen/build.py does not define")
            continue
        # The generator must be wired to the page the exemption claims, or it renders text
        # that reaches no reader.
        if f'_write("{rel}", {fn}())' not in src:
            offenders.append(
                f"{name}.csv claims to be published on {rel}, but gen/build.py does not "
                f"write that page from {fn}()")
            continue
        text = renderer()
        ids = [(r.get(id_col) or "").strip() for r in load_rows(name)]
        ids = [i for i in ids if i]
        if ids and not any(i in text for i in ids):
            offenders.append(
                f"{name}.csv claims to be published on {rel}, but {fn}() prints none of its "
                f"{id_col} values - the exemption is not earned")
    assert not offenders, (
        "committed data that no published page shows. Add a register spec in gen/build.py, or "
        "declare where it is published and make that true: " + "; ".join(offenders)
    )


def _nav_pages():
    """Every page path named in mkdocs.yml nav, relative to docs/."""
    cfg = open(os.path.join(ROOT, "mkdocs.yml"), encoding="utf-8").read()
    nav = cfg[cfg.index("\nnav:"):]
    return set(re.findall(r":\s*([A-Za-z0-9_\-/]+\.md)\s*$", nav, re.M))


def _generated_pages():
    """Every Markdown page gen/build.py writes, read from its source rather than from disk.

    Read from the source on purpose: these pages are gitignored, so globbing docs/ would make
    the answer depend on whether anyone had run the build - the defect that broke CI once.
    """
    src = open(os.path.join(ROOT, "gen", "build.py"), encoding="utf-8").read()
    written = set(re.findall(r'_write\(\s*f?"([^"{}]+\.md)"', src))
    written |= set(re.findall(r'\(\s*"[a-z]+",\s*"(registers/[a-z]+\.md)"', src))
    return written


def test_every_page_is_in_the_nav_and_every_nav_entry_is_a_real_page():
    """A page nothing links to and the sidebar does not list is not published, only present.

    Written after the ligation work landed four registers and two pages that were all correctly
    generated, correctly gitignored and correctly guarded - and one of which no page on the site
    linked to at all. `test_every_data_csv_is_published_somewhere` proves *data reaches a page*.
    Nothing proved *a page reaches a reader*, so the two properties drifted apart.

    Both directions, because each fails differently: a generated page missing from the nav is
    invisible, and a nav entry with no page behind it is a dead sidebar row that only shows up
    once someone runs `mkdocs build --strict`.
    """
    nav = _nav_pages()
    generated = _generated_pages()
    handwritten = set()
    for path in glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True):
        rel = os.path.relpath(path, os.path.join(ROOT, "docs")).replace(os.sep, "/")
        if rel not in generated:
            handwritten.add(rel)
    pages = generated | handwritten

    missing = sorted(pages - nav)
    dead = sorted(nav - pages)
    assert not missing, (
        "these pages exist but no mkdocs.yml nav entry lists them, so a reader can only reach "
        "them by search or by a link from elsewhere: " + ", ".join(missing))
    assert not dead, (
        "these mkdocs.yml nav entries name a page that nothing writes and no file provides: "
        + ", ".join(dead))


def test_every_generated_page_is_linked_from_a_hand_written_page():
    """The sidebar is not the only way in, and for a generated page it is the weakest one.

    A generated page reached only by scrolling the sidebar is buried: nothing in the prose tells
    a reader it exists or why they would want it. The narrow rule - *generated* pages need an
    inbound link from a *hand-written* one - has no exemptions, which is why it is drawn there.
    Hand-written section landing pages are excluded as link targets because they are reached as
    sections, and `index.md` is the way in rather than a destination.
    """
    generated = _generated_pages()
    inbound = {p: set() for p in generated}
    for path in glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True):
        rel = os.path.relpath(path, os.path.join(ROOT, "docs")).replace(os.sep, "/")
        if rel in generated:
            continue  # a generated page linking a generated page is code, not curation
        text = open(path, encoding="utf-8").read()
        here = os.path.dirname(rel)
        for m in re.finditer(r"\]\(([^)#\s]+\.md)", text):
            target = os.path.normpath(os.path.join(here, m.group(1))).replace(os.sep, "/")
            if target in inbound:
                inbound[target].add(rel)
    orphans = sorted(p for p, srcs in inbound.items() if not srcs)
    assert not orphans, (
        "these generated pages are reachable only from the sidebar - no hand-written page links "
        "to them, so nothing tells a reader they exist: " + ", ".join(orphans))


def test_the_access_legend_covers_the_whole_vocabulary():
    """A legend that omits a live label is worse than no legend: it reads as complete.

    `partial-text-read` was added to ACCESS_VOCAB during the ligation slice and eleven sources
    now carry it - every ICH document the information-requirement checklist is anchored to. The
    reading list's "How to read the access labels" table was not updated, so a reader consulting
    the legend to interpret the register found no entry for the label on eleven rows.

    Checked both ways against the vocabulary constant, never against a re-typed list.
    """
    page = os.path.join(ROOT, "docs", "sources", "reading-list.md")
    text = open(page, encoding="utf-8").read()
    legend = set(re.findall(r"^\|\s*\*\*([a-z ]+)\*\*\s*\|", text, re.M))
    expected = {v.replace("-", " ") for v in ACCESS_VOCAB}
    assert not (expected - legend), (
        "these access values are in ACCESS_VOCAB and absent from the reading-list legend: "
        + ", ".join(sorted(expected - legend)))
    assert not (legend - expected), (
        "the reading-list legend explains labels that are not in ACCESS_VOCAB, so it describes a "
        "vocabulary the register does not use: " + ", ".join(sorted(legend - expected)))
