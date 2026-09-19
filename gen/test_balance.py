"""Integrity + balance tests. Run: python -m pytest gen/ -q"""
import os
from gen.dataio import load_rows, load_params, param_value
from gen.balance import run_all, purity_floor


def test_all_source_keys_resolve():
    sources = {r["source_key"] for r in load_rows("sources")}
    # parameters, risks and impurities reference source_key; blanks allowed
    for name in ("parameters", "risks", "impurities"):
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
                 "streams", "sources", "impurities"):
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


def test_full_energy_duty_is_at_least_the_latent_minimum():
    """The Tier-2 full duty only ADDS sensible heat, gas heating and losses to the latent
    floor, so it can never fall below it. The dryer check also verifies the gas enthalpy drop
    can actually supply the latent load - a physical sanity check on the gas ratio and dT."""
    for r in run_all():
        assert r.evap_sensible_MJ >= 0
        assert r.drying_gas_kg >= 0
        assert r.evap_duty_full_MJ >= r.evap_duty_MJ
        assert r.dryer_duty_full_MJ >= r.dryer_evap_duty_MJ
        assert abs(r.evap_duty_full_MJ / 3.6 - r.evap_duty_full_kWh) < 1e-6
        assert abs(r.dryer_duty_full_MJ / 3.6 - r.dryer_duty_full_kWh) < 1e-6


def test_blanking_a_thermal_constant_refuses():
    """Every new energy-balance input obeys the blank-refusal rule: a gap raises, never
    silently defaults to a number (same invariant as P-H2O-LHV)."""
    import pytest
    from gen.balance import run_scenario
    scn = load_rows("scenarios")[0]
    for pid in ("P-CP-SOLN", "P-DRYGAS-CP", "P-EVAP-T-FEED", "P-EVAP-T-BOIL",
                "P-DRY-T-IN", "P-DRY-T-OUT", "P-DRYGAS-RATIO", "P-HEAT-LOSS-FRAC"):
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
        if "/registers/" in rel or rel.endswith(("balance/results.md", "balance/impurities.md",
                                                 "process/streams.md")):
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
    """A parameter that is a band must not hide as a bare point value (F-018, F-019).

    Convention: a band parameter flags itself with the token 'BAND:' in its notes and
    must then populate range_low/range_high; and any parameter carrying a range must
    keep its point value inside it.
    """
    params = load_params()
    offenders = []
    for r in load_rows("parameters"):
        pid = r["param_id"]
        notes = r.get("notes") or ""
        lo = (r.get("range_low") or "").strip()
        hi = (r.get("range_high") or "").strip()
        if "BAND:" in notes and not (lo and hi):
            offenders.append(f"{pid}: notes flag a BAND but range_low/range_high are empty")
            continue
        if lo or hi:
            if not (lo and hi):
                offenders.append(f"{pid}: only one of range_low/range_high is set")
                continue
            flo, fhi = float(lo), float(hi)
            if flo > fhi:
                offenders.append(f"{pid}: range_low {flo} > range_high {fhi}")
            v = param_value(params, pid)
            if v is not None and not (flo <= v <= fhi):
                offenders.append(f"{pid}: value {v} outside its range [{flo}, {fhi}]")
    assert not offenders, "band/range defect(s): " + "; ".join(offenders)


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
    """Physical fact (finding 1): block-internal n-1 is floored at the blocks, and the adenylylated
    dead-end is controlled at the reaction. Neither may be modelled as a downstream separation."""
    rows = {r["impurity_id"]: r for r in load_rows("impurities")}
    assert rows["IMP-N1"]["clearance_model"] == "block_floor", \
        "n-1 must be floored (block_floor), never modelled as cleared downstream"
    assert rows["IMP-APPN"]["clearance_model"] == "designed_out", \
        "the adenylylated dead-end must be controlled at the reaction (designed_out)"


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
