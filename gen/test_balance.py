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
