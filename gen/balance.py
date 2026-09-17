"""Executable mass and energy balance for the siRNA DS train.

Every numeric input is pulled from data/parameters.csv. Inputs flagged there as
`assumption` are illustrative placeholders (registered as gaps / open questions),
so ALL outputs of this module are assumption-driven until real values are supplied.
The module never invents a number: if a required input is blank it raises, so a
gap cannot silently become a fabricated result.

Boundary: received purified 5'-phosphorylated blocks -> ligation -> clarification
-> UF/DF -> evaporation -> spray drying -> DS powder. Fully aqueous, no solvents.

CONCENTRATION BASIS (stated because the two halves of the train differ):
  * Ligation and UF concentrations are on an siRNA (active) basis, matching the cited
    literature, which reports siRNA concentrations rather than total solids.
  * The evaporator outlet concentration is on a TOTAL DISSOLVED SOLIDS basis, because a
    viscosity limit constrains everything in solution, not just the active.
  * How much excipient is in solution at the evaporator is itself a process choice, carried
    explicitly as P-EXCIP-FRAC-PRE-EVAP (0 = all excipient added after evaporation, the base
    case; 1 = the full load present from the final diafiltration). See Q-038.
Basis: DS demand is taken as siRNA active mass (API); powder also carries excipient.
"""
from dataclasses import dataclass, asdict
from .dataio import load_params, load_rows, param_value


def _require(params, pid):
    v = param_value(params, pid)
    if v is None:
        raise ValueError(f"Required parameter {pid} is blank; cannot run balance "
                         f"(register it as a gap rather than inventing a value).")
    return v


@dataclass
class ScenarioResult:
    scenario_id: str
    label: str
    annual_ds_api_kg: float
    campaigns_per_yr: float
    ds_api_per_campaign_kg: float
    powder_per_campaign_kg: float
    overall_yield_frac: float
    api_at_ligation_kg: float
    ligation_volume_L: float
    uf_retentate_volume_L: float
    df_buffer_volume_L: float
    evap_water_removed_L: float
    dryer_feed_mass_kg: float
    dryer_water_evaporated_kg: float
    excip_frac_pre_evap: float
    evap_outlet_solids_kg: float
    wfi_approx_L: float
    aqueous_waste_approx_L: float
    evap_duty_MJ: float
    evap_duty_kWh: float
    dryer_evap_duty_MJ: float
    dryer_evap_duty_kWh: float


def run_scenario(scn, params):
    # yields (fractions)
    y_lig = _require(params, "P-YLD-LIG") / 100.0
    y_ufdf = _require(params, "P-YLD-UFDF") / 100.0
    y_evap = _require(params, "P-YLD-EVAP") / 100.0
    y_dry = _require(params, "P-YLD-DRY") / 100.0
    overall = y_lig * y_ufdf * y_evap * y_dry

    r = _require(params, "P-EXCIPIENT-RATIO")
    c_lig = _require(params, "P-CONC-LIG")          # g/L
    c_uf = _require(params, "P-CONC-UF")            # g/L
    c_evap = _require(params, "P-CONC-EVAP")        # g/L
    dryfeed_pct = _require(params, "P-CONC-DRYFEED")  # %w/w solids
    diavol = _require(params, "P-DF-DIAVOL")
    lhv = _require(params, "P-H2O-LHV")  # kJ/kg
    f_pre = _require(params, "P-EXCIP-FRAC-PRE-EVAP")  # 0..1 excipient present at evaporator

    annual = float(scn["annual_ds_demand_kg_yr"])
    camp = float(scn["campaigns_per_yr"])
    ds_api_camp = annual / camp
    powder_camp = ds_api_camp * (1.0 + r)

    # back-calculate API needed at ligation input from overall yield
    api_lig = ds_api_camp / overall  # kg

    # forward volumes (g = kg*1000)
    lig_vol = (api_lig * 1000.0) / c_lig  # L
    api_after_lig = api_lig * y_lig
    uf_vol = (api_after_lig * 1000.0) / c_uf  # L retentate
    df_buffer = diavol * uf_vol  # L
    api_after_ufdf = api_after_lig * y_ufdf

    # Evaporator outlet is sized on TOTAL dissolved solids: the active plus whatever share of
    # the excipient load is already in solution at this point (P-EXCIP-FRAC-PRE-EVAP).
    evap_solids = api_after_ufdf * (1.0 + f_pre * r)  # kg total dissolved solids
    evap_out_vol = (evap_solids * 1000.0) / c_evap  # L
    evap_water = max(uf_vol - evap_out_vol, 0.0)  # L ~ kg
    api_after_evap = api_after_ufdf * y_evap

    # dryer: solids = API + excipient carried from final matrix
    dry_solids = api_after_evap * (1.0 + r)  # kg
    dryer_feed = dry_solids / (dryfeed_pct / 100.0)  # kg total feed
    dryer_water = max(dryer_feed - dry_solids, 0.0)  # kg
    # (powder_camp already computed from spec; api_after_dry consistency check in tests)

    wfi = df_buffer + lig_vol  # dominant clean-water demand (buffer prep + DF)
    aq_waste = df_buffer + max(lig_vol - uf_vol, 0.0) + evap_water  # permeate + condensate

    evap_MJ = evap_water * lhv / 1000.0
    dry_MJ = dryer_water * lhv / 1000.0

    return ScenarioResult(
        scenario_id=scn["scenario_id"], label=scn["label"],
        annual_ds_api_kg=annual, campaigns_per_yr=camp,
        ds_api_per_campaign_kg=ds_api_camp, powder_per_campaign_kg=powder_camp,
        overall_yield_frac=overall, api_at_ligation_kg=api_lig,
        ligation_volume_L=lig_vol, uf_retentate_volume_L=uf_vol,
        df_buffer_volume_L=df_buffer, evap_water_removed_L=evap_water,
        dryer_feed_mass_kg=dryer_feed, dryer_water_evaporated_kg=dryer_water,
        excip_frac_pre_evap=f_pre, evap_outlet_solids_kg=evap_solids,
        wfi_approx_L=wfi, aqueous_waste_approx_L=aq_waste,
        evap_duty_MJ=evap_MJ, evap_duty_kWh=evap_MJ / 3.6,
        dryer_evap_duty_MJ=dry_MJ, dryer_evap_duty_kWh=dry_MJ / 3.6,
    )


def run_all():
    params = load_params()
    scns = load_rows("scenarios")
    return [run_scenario(s, params) for s in scns]


def purity_floor(block_full_length_pct=None, n_blocks=3):
    """Internal-limited full-length ceiling = product of per-block FL fractions.

    This is the purity that block-internal n-1 fixes and that no size-based
    filtration can improve (see finding 1). Returns percent.

    block_full_length_pct defaults to the registered P-BLOCK-PUR so the figure quoted in
    the documents and the figure used in code cannot drift apart.
    """
    if block_full_length_pct is None:
        block_full_length_pct = _require(load_params(), "P-BLOCK-PUR")
    f = block_full_length_pct / 100.0
    return (f ** n_blocks) * 100.0


if __name__ == "__main__":
    for res in run_all():
        d = asdict(res)
        print(f"\n[{d['scenario_id']}] {d['label']}")
        for k, v in d.items():
            if isinstance(v, float):
                print(f"  {k}: {v:,.2f}")
