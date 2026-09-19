# Tech transfer & engineering package (Tier 3 — sketch)

Full tech-transfer and engineering package is Tier 3. This lists what the package will contain and
what already exists here.

## Already in this knowledge base

- Block flow diagram with numbered streams ([diagrams](../diagrams/index.md)).
- Executable mass balance across scenarios ([balance](../balance/results.md)).
- Governing equations with terms, assumptions, and transferability notes ([equations](../equations/index.md)).
- Equipment, stream, buffer, utility, risk, and question registers.
- A cited source log with reachability and scale/system tags.

## To be produced

- **Process flow diagrams (PFDs)** with instrument tags and control loops.
- **Full mass & energy balance** with sensible heat, gas loads, and species-resolved impurity
  tracking.
- **Equipment specifications and sizing basis** per item (the [equipment register](../registers/equipment.md)
  carries sizing-basis, MOC, and turndown columns as stubs).
- **Instrumentation and PAT** per unit operation (e.g. in-line UV/conductivity on UF/DF, outlet
  temperature and residual moisture on the dryer).
- **Control strategy** linking critical process parameters to critical quality attributes.
- **Standards:** ICH Q8–Q11 (development, risk, quality systems, development/manufacture of DS),
  ICH Q6/Q7 (specs, GMP), and the relevant engineering codes at **current editions** — ASME BPE-2026,
  ASTM E2500-25, NFPA 660-2025 and IEC 60079-10-2:2026 (<span class="prov-fact">fact</span>;
  [SRC-STANDARDS-CURRENT](../registers/sources.md)); oligonucleotides sit outside ICH Q3A/Q6A impurity
  guidance ([SRC-ICH-Q3A-SCOPE](../registers/sources.md)), so specs are justified case-by-case.

## Named gaps against WHO TRS 1044 Annex 4

The transfer guideline covers active pharmaceutical ingredients directly, and its Appendix 1 is the
itemised list a contract manufacturer works from (<span class="prov-fact">fact</span>;
[SRC-WHO-TRS1044](../registers/sources.md)). Measured against it, the concrete gaps in this package are:

- **No scale-up protocol or report** — the largest real ligation scale today is ~1 L.
- **No hold-time protocols** for the aqueous intermediates (Q-043, R-009).
- **No cleaning-validation master plan with a health-based exposure limit** for shared filtration and
  drying equipment (R-015) — a potent, highly water-soluble polyanion on hard-to-clean surfaces (R-008).
- **No forced-degradation stability data.**
- **No side-by-side comparison** of premises, equipment, instruments, materials, procedures and
  methods between the sending and receiving units.
- **No acceptance criteria for a successful transfer, and no gap analysis.**

## Control strategy anchor points (from the findings)

- Purity is controlled **at the block stage** and the **ligation reaction**, not by downstream
  polishing — so incoming-block specs and in-reaction controls (ATP, enzyme, temperature/time) are
  critical.
- Duplex integrity is controlled first by the **moisture-shifted glass transition** (the binding
  limit, on drying and storage), then by the **spray-dryer outlet temperature** below Tm (the looser
  limit), and by the **final matrix**.
- Enzyme clearance depends on **immobilisation** performance.
