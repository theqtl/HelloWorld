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
import math
from dataclasses import dataclass, asdict
from .dataio import load_params, load_rows, param_value


def _require(params, pid):
    v = param_value(params, pid)
    if v is None:
        raise ValueError(f"Required parameter {pid} is blank; cannot run balance "
                         f"(register it as a gap rather than inventing a value).")
    return v


def _require_above(hi, lo, hi_id, lo_id):
    """An inconsistent operating point is a DATA error, so raise rather than clamp.

    The previous model wrapped its temperature differences in max(..., 0), which turned an
    inverted pair into a silent 0 MJ duty - the same defect-masking the blank-refusal rule
    exists to prevent. Legitimate process states are still clamped (see the dryer feed term);
    only physically impossible data raises.
    """
    if hi <= lo:
        raise ValueError(
            f"{hi_id} ({hi}) must be above {lo_id} ({lo}); the energy balance has no "
            f"physical meaning otherwise. Fix the registered values rather than the code."
        )


@dataclass
class ScenarioResult:
    scenario_id: str
    label: str
    annual_ds_api_kg: float
    campaigns_per_yr: float
    ds_api_per_campaign_kg: float
    powder_per_campaign_kg: float
    overall_yield_frac: float
    ufdf_yield_frac: float
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
    evap_feed_mass_kg: float
    evap_sensible_MJ: float
    evap_duty_full_MJ: float
    evap_duty_full_kWh: float
    dryer_feed_sensible_MJ: float
    dryer_process_duty_MJ: float
    dryer_process_duty_kWh: float
    drying_gas_kg: float
    dryer_heater_duty_MJ: float
    dryer_heater_duty_kWh: float


def run_scenario(scn, params):
    # yields (fractions)
    y_lig = _require(params, "P-YLD-LIG") / 100.0
    y_evap = _require(params, "P-YLD-EVAP") / 100.0
    y_dry = _require(params, "P-YLD-DRY") / 100.0

    r = _require(params, "P-EXCIPIENT-RATIO")
    c_lig = _require(params, "P-CONC-LIG")          # g/L
    c_uf = _require(params, "P-CONC-UF")            # g/L
    c_evap = _require(params, "P-CONC-EVAP")        # g/L
    dryfeed_pct = _require(params, "P-CONC-DRYFEED")  # %w/w solids
    diavol = _require(params, "P-DF-DIAVOL")
    lhv = _require(params, "P-H2O-LHV")  # kJ/kg
    f_pre = _require(params, "P-EXCIP-FRAC-PRE-EVAP")  # 0..1 excipient present at evaporator

    # Full-energy-balance inputs (Tier 2): sensible heat, drying-gas heating, losses.
    cp_soln = _require(params, "P-CP-SOLN")        # kJ/kg/K
    cp_gas = _require(params, "P-DRYGAS-CP")       # kJ/kg/K
    t_feed = _require(params, "P-EVAP-T-FEED")     # degC
    t_boil = _require(params, "P-EVAP-T-BOIL")     # degC
    t_dry_in = _require(params, "P-DRY-T-IN")      # degC
    t_dry_out = _require(params, "P-DRY-T-OUT")    # degC
    t_amb = _require(params, "P-DRY-T-AMBIENT")    # degC
    rho = _require(params, "P-SOLN-DENSITY")       # kg/L
    loss_frac = _require(params, "P-HEAT-LOSS-FRAC")  # fraction added for losses

    # Operating points that are physically impossible are data errors, not something to clamp.
    _require_above(t_boil, t_feed, "P-EVAP-T-BOIL", "P-EVAP-T-FEED")
    _require_above(t_dry_in, t_dry_out, "P-DRY-T-IN", "P-DRY-T-OUT")
    _require_above(t_dry_out, t_amb, "P-DRY-T-OUT", "P-DRY-T-AMBIENT")

    # UF/DF yield is NOT a flat constant (F-019). Membrane-passage loss follows the diafiltration
    # relation yield = exp(-(1-R)(ln VCF + N)) reproduced from the three worked points in
    # SRC-MILLIPORE-TFF (R=0.99 -> 9.5% loss; R=0.999 -> 1.0% loss at ln VCF + N = 10). Two further
    # loss terms are ADDITIVE and were absent from the old model: unrecoverable hold-up in tubing and
    # filters (dominant at small batch, SRC-NOURAFKAN-2024) and membrane adsorption (SRC-MILLIPORE-TFF).
    # See EQ-UFYIELD on the equations page.
    retention = _require(params, "P-UFDF-RETENTION")        # fraction (~0.99)
    holdup_loss = _require(params, "P-UFDF-HOLDUP-LOSS")    # fraction
    adsorp_loss = _require(params, "P-UFDF-ADSORP-LOSS")    # fraction
    vcf = c_uf / c_lig                                      # volume concentration factor
    membrane_yield = math.exp(-(1.0 - retention) * (math.log(vcf) + diavol))
    y_ufdf = membrane_yield - holdup_loss - adsorp_loss
    overall = y_lig * y_ufdf * y_evap * y_dry

    annual = float(scn["annual_ds_demand_kg_yr"])
    camp = float(scn["campaigns_per_yr"])
    ds_api_camp = annual / camp
    powder_camp = ds_api_camp * (1.0 + r)

    # back-calculate API needed at ligation input from overall yield
    api_lig = ds_api_camp / overall  # kg

    # forward volumes (g = kg*1000)
    lig_vol = (api_lig * 1000.0) / c_lig  # L
    api_after_lig = api_lig * y_lig
    # The retentate is what SURVIVES UF/DF, so its volume is sized on api_after_ufdf, not on the
    # API entering the step. Sizing it on api_after_lig overstated the retentate (and therefore
    # the evaporator feed and its duty) by 1/y_ufdf, and made the reported "UF retentate volume"
    # a quantity that never exists in the process.
    api_after_ufdf = api_after_lig * y_ufdf
    uf_vol = (api_after_ufdf * 1000.0) / c_uf  # L retentate leaving UF/DF
    df_buffer = diavol * uf_vol  # L

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

    # Full energy balance (EQ-ENERGY). The latent minima above are a strict floor, and every
    # term added below is non-negative, so that ordering holds BY CONSTRUCTION rather than as a
    # consequence of the chosen placeholder values.
    #
    # Evaporator: raise the feed MASS to the vacuum boiling point, evaporate, then uplift once
    # for heat loss. The feed mass needs a density (P-SOLN-DENSITY); using litres as kilograms
    # smuggled an unregistered number into the balance.
    # If ultrafiltration already meets the evaporator target there is nothing to remove, the unit
    # is bypassed, and it costs nothing - so the sensible term is gated on there being water to
    # evaporate. (Generating the excipient-sensitivity table exposed this: the old model charged
    # sensible heat to an evaporator that was doing no work.)
    evap_feed_mass_kg = uf_vol * rho
    evap_sensible_MJ = (evap_feed_mass_kg * cp_soln * (t_boil - t_feed) / 1000.0
                        if evap_water > 0 else 0.0)
    evap_full_MJ = (evap_MJ + evap_sensible_MJ) * (1.0 + loss_frac)
    #
    # Dryer, in two reported quantities that are different things:
    #  * PROCESS duty - what drying actually requires: evaporate the water, raise the feed to the
    #    outlet temperature, plus losses. The feed arrives from the evaporator at its boiling
    #    point, so a feed hotter than the outlet needs no heating; that clamp is a legitimate
    #    process state, unlike an inverted inlet/outlet, which raises above.
    #  * HEATER duty - the utility load, which is what UT-DRYGAS actually is: inlet gas heating
    #    from ambient. The gas MASS is derived from the process duty, so no tuned gas:water ratio
    #    is needed, and the result stays scale-parametric (it scales with the water evaporated).
    dryer_feed_sensible_MJ = dryer_feed * cp_soln * max(t_dry_out - t_boil, 0.0) / 1000.0
    dryer_process_MJ = (dry_MJ + dryer_feed_sensible_MJ) * (1.0 + loss_frac)
    drying_gas_kg = dryer_process_MJ * 1000.0 / (cp_gas * (t_dry_in - t_dry_out))
    dryer_heater_MJ = drying_gas_kg * cp_gas * (t_dry_in - t_amb) / 1000.0

    return ScenarioResult(
        scenario_id=scn["scenario_id"], label=scn["label"],
        annual_ds_api_kg=annual, campaigns_per_yr=camp,
        ds_api_per_campaign_kg=ds_api_camp, powder_per_campaign_kg=powder_camp,
        overall_yield_frac=overall, ufdf_yield_frac=y_ufdf, api_at_ligation_kg=api_lig,
        ligation_volume_L=lig_vol, uf_retentate_volume_L=uf_vol,
        df_buffer_volume_L=df_buffer, evap_water_removed_L=evap_water,
        dryer_feed_mass_kg=dryer_feed, dryer_water_evaporated_kg=dryer_water,
        excip_frac_pre_evap=f_pre, evap_outlet_solids_kg=evap_solids,
        wfi_approx_L=wfi, aqueous_waste_approx_L=aq_waste,
        evap_duty_MJ=evap_MJ, evap_duty_kWh=evap_MJ / 3.6,
        dryer_evap_duty_MJ=dry_MJ, dryer_evap_duty_kWh=dry_MJ / 3.6,
        evap_feed_mass_kg=evap_feed_mass_kg, evap_sensible_MJ=evap_sensible_MJ,
        evap_duty_full_MJ=evap_full_MJ, evap_duty_full_kWh=evap_full_MJ / 3.6,
        dryer_feed_sensible_MJ=dryer_feed_sensible_MJ,
        dryer_process_duty_MJ=dryer_process_MJ, dryer_process_duty_kWh=dryer_process_MJ / 3.6,
        drying_gas_kg=drying_gas_kg,
        dryer_heater_duty_MJ=dryer_heater_MJ, dryer_heater_duty_kWh=dryer_heater_MJ / 3.6,
    )


def run_all():
    params = load_params()
    scns = load_rows("scenarios")
    return [run_scenario(s, params) for s in scns]


def purity_floor(block_full_length_pct=None, n_blocks=None):
    """Internal-limited full-length ceiling = product of per-block FL fractions.

    This is the purity that block-internal n-1 fixes and that no size-based
    filtration can improve (see finding 1). Returns percent.

    block_full_length_pct defaults to the registered P-BLOCK-PUR so the figure quoted in
    the documents and the figure used in code cannot drift apart.
    """
    params = None
    if block_full_length_pct is None or n_blocks is None:
        params = load_params()
    if block_full_length_pct is None:
        block_full_length_pct = _require(params, "P-BLOCK-PUR")
    if n_blocks is None:
        # The block count is a registered design choice (P-N-BLOCKS), not a code default: it is
        # the exponent of the purity floor, so a hardcoded 3 put the published full-length
        # ceiling on an unregistered number with no provenance.
        n_blocks = _require(params, "P-N-BLOCKS")
    f = block_full_length_pct / 100.0
    return (f ** n_blocks) * 100.0


if __name__ == "__main__":
    for res in run_all():
        d = asdict(res)
        print(f"\n[{d['scenario_id']}] {d['label']}")
        for k, v in d.items():
            if isinstance(v, float):
                print(f"  {k}: {v:,.2f}")
