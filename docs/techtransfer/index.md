# Tech transfer & engineering package (Tier 3 — sketch)

Full tech-transfer and engineering package is Tier 3. This lists what the package will contain and
what already exists here.

## Already in this knowledge base

- Block flow diagram with numbered streams ([diagrams](../diagrams/index.md)).
- Executable mass **and energy** balance across scenarios, with the full evaporator and drying-gas
  duties (`EQ-ENERGY`) and a species-resolved [impurity-fate overlay](../balance/impurities.md)
  ([balance](../balance/results.md)).
- Governing equations with terms, assumptions, and transferability notes ([equations](../equations/index.md)).
- Equipment, stream, buffer, utility, risk, and question registers.
- A cited source log with reachability and scale/system tags.
- An [instrument register](../registers/instruments.md) — every instrument the concept implies, control-enforcing and monitoring-only alike, each with a tag from [this project's own declared letter scheme](../registers/instruments.md) — conformance to the current ANSI/ISA-5.1 edition is **unverified** and registered as Q-053, so the scheme is not presented as ISA's — and, crucially, its **measurement mode** (in-line / on-line / at-line / off-line).
- A generated [CPP → CQA control strategy matrix](../process/controls.md): each control names the registered parameter it acts on, the instrument that could enforce it, and the open question that blocks it — including the controls that **cannot exist**, which are rendered as registered gaps rather than omitted.

- **[Process flow diagrams](../diagrams/pfd.md)**, one per unit operation, generated from the registers above: each instrument drawn at its sensing point, with closed control loops distinguished from withdrawn-sample measurements by a rule over the measurement mode and the declared tag letters rather than by assertion. What they do **not** carry is registered rather than silent: the final control element each loop manipulates is not in any register (Q-055), no standard this project has read specifies the symbol set (Q-054), and seven tags declaring a control function appear in no control row (Q-056).

## To be produced

- **A P&ID, equipment layout and a stream table on the drawings.** The PFDs stop short of all three. Piping, valve specification and line numbering are P&ID-level work; layout and a plot plan are a facility exercise tied to Q-002; stream quantities stay in the [balance](../balance/results.md) rather than being copied onto an SVG where they could drift.
- **Measured inputs for the mass & energy balance.** The balance now computes the full evaporator and
  drying-gas duties and the species-resolved impurity fate, but on assumption-flagged inputs; the
  package still needs measured thermal (Q-045, Q-046) and clearance (Q-036) data to replace them.
- **Equipment specifications and sizing basis** per item (the [equipment register](../registers/equipment.md)
  now carries a sizing basis, materials of construction, and a turndown basis per item; absolute sizes
  remain a function of demand, Q-002).
- **Instrumentation and PAT** per unit operation. The register above now names them; what is still
  missing is vendor selection, loop tuning and qualification. **One correction belongs here:** earlier
  tiers of this page advertised *in-line* UV on UF/DF as PAT, while Q-042 recorded the opposite in the
  same repository. In-line UV saturates on a 21-mer at process concentration, so retentate
  concentration is read **at-line** by variable-pathlength slope spectroscopy (`AI-0306`, Q-042).
  In-line **conductivity** is unaffected and remains the diafiltration endpoint (`AI-0305`, `EQ-DIAF`);
  dryer outlet temperature is in-line (`TIC-0502`) and residual moisture is at-line (`MI-0507`, Q-039).
- **Control strategy** linking critical process parameters to critical quality attributes. The
  structure now exists and is generated from data; what is missing is the data to fill it. Almost
  every acceptance basis in the matrix is an assumption tied to an open question, and two rows have
  no acceptance basis at all because no public figure exists for either (`P-ENZ-CLEARANCE-LRV`, Q-032).
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
  The derivation method and the registered HBEL gap are now on the
  [microbial page](../process/microbial.md) (`P-HBEL-DS`, Q-047); the value stays blank until
  toxicology data exists.
- **No forced-degradation stability data.**
- **No side-by-side comparison** of premises, equipment, instruments, materials, procedures and
  methods between the sending and receiving units. *Partly addressable since Tier 3:* the
  **instruments** column of that comparison now has a receiving-unit side to it (the
  [instrument register](../registers/instruments.md)), and the equipment column has had one since
  Tier 2. There is still no sending unit to compare against, and premises, materials, procedures
  and methods are untouched — so this gap narrows, it does not close.
- **No acceptance criteria for a successful transfer, and no gap analysis.**

## Control strategy anchor points (from the findings)

These three bullets are the argument in narrative form. Each one is now also **generated as data**,
row by row, in the [control strategy matrix](../process/controls.md) — with the registered
parameter, the enforcing instrument, the acceptance basis (or the registered gap standing in for
one) and the question that blocks it. Read them here; check them there.

- Purity is controlled **at the block stage** and the **ligation reaction**, not by downstream
  polishing — so incoming-block specs and in-reaction controls (ATP, enzyme, temperature/time) are
  critical (`C-001`–`C-007`).
- Duplex integrity is controlled first by the **moisture-shifted glass transition** (the binding
  limit, on drying and storage), then by the **spray-dryer outlet temperature** below Tm (the looser
  limit), and by the **final matrix** (`C-008`–`C-010`).
- Enzyme clearance has **no chosen route**, and this bullet used to say it depended on
  immobilisation performance. That presupposed the answer to a question nobody has answered: the
  enzyme form is open (Q-050), so clearance is carried as **two branches, neither selected** —
  denature-then-filter for a soluble enzyme, retention on the carrier for an immobilised one
  (`C-011`, `C-012`). Both have a **blank** acceptance basis, because no clearance figure exists
  publicly for either (`P-ENZ-CLEARANCE-LRV`, Q-032). The soluble branch is not the cheap way out:
  its 85 °C denature hold sits above any plausible duplex melting band, trading an enzyme-clearance
  gap for a product-integrity risk (R-021, Q-030), and it needs a heated vessel that is not in the
  equipment register at all.
