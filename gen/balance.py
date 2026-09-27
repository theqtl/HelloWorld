"""Executable mass and energy balance for the siRNA DS train.

Every numeric input is pulled from data/parameters.csv. Inputs flagged there as
`assumption` are illustrative placeholders (registered as gaps / open questions),
so ALL outputs of this module are assumption-driven until real values are supplied.
The module never invents a number: if a required input is blank it raises, so a
gap cannot silently become a fabricated result.

AND IT CANNOT READ AN EDUCATED ESTIMATE. `provenance = judgement` rows carry their
number in `est_value` with `value` blank, and every read here goes through
`param_value`, which reads `value`. So an estimate reaching a computed figure is not
a thing anyone has to remember not to do - `_require` raises on the blank instead.
That is the whole structural claim of the fourth provenance, and it is a property of
which column this module reads rather than a rule written down somewhere.

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
from .dataio import load_params, load_rows, param_value, equip_ids


def _require(params, pid):
    v = param_value(params, pid)
    if v is None:
        raise ValueError(f"Required parameter {pid} is blank; cannot run balance "
                         f"(register it as a gap rather than inventing a value).")
    return v


def _require_realisable_yield(y, terms):
    """A composed yield outside (0, 1] is a DATA error, so raise rather than publish it.

    Found by execution in slice 4 phase 5, not by reading. `y_ufdf` is a membrane-passage yield
    with two ADDITIVE loss terms subtracted from it, and nothing bounded the result: setting
    P-UFDF-HOLDUP-LOSS to 1.2 gave y_ufdf = -0.2917, a ligation volume of MINUS 30,483 L and a
    negative WFI demand, and `python -m gen.build` published all of it. At 0.85 the yield is
    +0.0583 and the same scenario asks for a 152,578 L ligation vessel - physically absurd, but
    positive, so no sign check would catch it either.

    This is the hold-up/area coupling the plan asked for a consistency guard on, in the only form
    the data supports. The plan wanted the loss fraction checked against a membrane area implied by
    a specific hold-up of 1-2 L/m2 - but NO specific hold-up figure is registered anywhere in this
    repository (measured: no parameter, source or register row carries L/m2), so that check would
    rest on an unregistered number and could not be written honestly. What CAN be checked is that
    the loss terms do not consume the whole step, which is the same defect one level up and was
    genuinely open.

    Deliberately the same shape as `_require_above`: legitimate process states pass, physically
    impossible data raises, and the fix is in the registered values rather than in the code.
    """
    if not (0.0 < y <= 1.0):
        raise ValueError(
            f"Composed UF/DF yield is {y:.4f}, outside (0, 1]. The additive loss terms "
            f"({terms}) consume the whole step, so every volume downstream of it is a "
            f"back-calculation through a non-positive number - which publishes as a negative or "
            f"absurd tank size rather than as an error. Fix the registered loss fractions."
        )


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
    cip_water_approx_L: float
    cip_circuits: int
    ufdf_holdup_volume_L: float
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
    anneal_topfill_duty_MJ: float
    anneal_topfill_duty_kWh: float


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
    t_anneal = _require(params, "P-LIG-ANNEAL-T")  # degC - the ligation anneal setpoint
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
    _require_realisable_yield(
        y_ufdf,
        f"membrane {membrane_yield:.4f} - hold-up {holdup_loss} - adsorption {adsorp_loss}")
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

    # CLEANING DEMAND, which was ZERO LITRES until slice 4 phase 5. The `wfi` line below read
    # `df_buffer + lig_vol` and nothing else, so the figure that sizes U00-BUF and UT-WFI contained
    # no cleaning water at all while U06-CIP sat in the equipment register contributing nothing to
    # any number. Now that BUF-CIP and BUF-MEMBRANE-CLEAN exist as registered recipes, the volume
    # per wash and the washes per campaign are what make them cost something.
    #
    # THE CIRCUIT COUNT IS DERIVED, NOT WRITTEN. Every unit operation in this train is wetted and
    # therefore cleaned, and `cip_coverage_offenders()` in gen/envelope.py proves that every
    # `equip_id` is named by one of the registered cleaning solutions - so the number of circuits IS
    # the number of equipment rows, and adding a unit operation raises the cleaning demand without
    # anyone remembering to. That is the same "derive the vocabulary from its owner" move phase 4
    # made for `risk_unit_ops()`, applied to a quantity instead of a vocabulary.
    #
    # THE RESULT IS A FLOOR AND IS PUBLISHED AS ONE (Q-076). P-CIP-WASH-VOL carries 400 L from a
    # facility whose circuits average 200 L of hold-up while our ligation vessel is 3,301-13,202 L;
    # only the caustic wash is counted, because caustic is the only chemistry registered; and no
    # rinse is counted, although PIC/S requires the caustic itself be rinsed out and WHO expresses a
    # carryover limit in rinse water. Three reasons it is low, none of them hidden.
    cip_wash_vol = _require(params, "P-CIP-WASH-VOL")               # L per circuit per wash
    cip_washes = _require(params, "P-CIP-WASHES-PER-CAMPAIGN")      # per circuit per campaign
    cip_circuits = len(equip_ids())
    cip_water = cip_circuits * cip_washes * cip_wash_vol  # L per campaign

    # The hold-up loss as a VOLUME, published because the fraction hides what it means. 0.10 of a
    # 227 L retentate is ~23 L, and of a 907 L retentate ~91 L - the same fraction standing for four
    # times the hardware. It is also the term whose own source measured 30-40% at 20-80 mL, so the
    # scale dependence is real and carrying a flat fraction across the scenarios is a modelling
    # choice rather than a measurement (Q-036, P-UFDF-HOLDUP-LOSS).
    ufdf_holdup_vol = holdup_loss * uf_vol  # L

    wfi = df_buffer + lig_vol + cip_water  # clean-water demand (buffer prep + DF + cleaning)
    aq_waste = (df_buffer + max(lig_vol - uf_vol, 0.0) + evap_water
                + cip_water)  # permeate + condensate + spent wash to drain

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
    # THE ANNEAL JACKET DUTY AT TOP FILL - the sizing consequence of the published contradiction
    # ENV-020 refuses to resolve. Telescoping phosphorylation into ligation fills the vessel from V
    # to 2V or to 5V depending on which of SRC-ALMAC-2023's two figures is right, and the 65 C
    # anneal (P-LIG-ANNEAL-T) has to be delivered at whatever the top fill turns out to be. Computed
    # on the FULL ligation volume because that is the top fill under either reading, from ambient
    # because the buffer is made up cold. This is a sensible duty only: the registered 15 minute
    # anneal hold adds a loss term, not a phase change, so unlike the evaporator there is no latent
    # floor to exceed. (The hold parameter is deliberately NOT named here. `used_by` is policed by
    # bare substring over this file, so naming a docs-only id in a COMMENT reads as consuming it -
    # and the honest fix is the comment, since the balance really does not read the hold.)
    #
    # AND IT IS THE ONLY STEAM DUTY PHASE 5 COULD COMPUTE. The plan asked for CIP steam as well, and
    # CIP steam is NOT here - not by oversight. The only wash temperature in the register is
    # BUF-CIP's "ambient to 50 C", which is an ESTIMATE and therefore lives in `est_value`, and every
    # read in this module goes through `param_value`, which reads `value`. So the fourth provenance
    # blocks the calculation exactly as designed, and the honest outcome is a missing duty with a
    # named reason rather than a duty resting on an estimate. Adding an `assumption` placeholder for
    # the same temperature would give that number two homes, which is the defect ESTIMATE_REGISTERS
    # exists to prevent. See Q-074.
    anneal_topfill_MJ = (lig_vol * rho * cp_soln
                         * max(t_anneal - t_amb, 0.0) / 1000.0) * (1.0 + loss_frac)

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
        wfi_approx_L=wfi, cip_water_approx_L=cip_water,
        cip_circuits=cip_circuits, ufdf_holdup_volume_L=ufdf_holdup_vol,
        aqueous_waste_approx_L=aq_waste,
        evap_duty_MJ=evap_MJ, evap_duty_kWh=evap_MJ / 3.6,
        dryer_evap_duty_MJ=dry_MJ, dryer_evap_duty_kWh=dry_MJ / 3.6,
        evap_feed_mass_kg=evap_feed_mass_kg, evap_sensible_MJ=evap_sensible_MJ,
        evap_duty_full_MJ=evap_full_MJ, evap_duty_full_kWh=evap_full_MJ / 3.6,
        dryer_feed_sensible_MJ=dryer_feed_sensible_MJ,
        dryer_process_duty_MJ=dryer_process_MJ, dryer_process_duty_kWh=dryer_process_MJ / 3.6,
        drying_gas_kg=drying_gas_kg,
        dryer_heater_duty_MJ=dryer_heater_MJ, dryer_heater_duty_kWh=dryer_heater_MJ / 3.6,
        anneal_topfill_duty_MJ=anneal_topfill_MJ,
        anneal_topfill_duty_kWh=anneal_topfill_MJ / 3.6,
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
