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
  ICH Q6/Q7 (specs, GMP), and the relevant engineering codes; oligonucleotides sit outside ICH
  impurity guidance, so specs are justified case-by-case.

## Control strategy anchor points (from the findings)

- Purity is controlled **at the block stage** and the **ligation reaction**, not by downstream
  polishing — so incoming-block specs and in-reaction controls (ATP, enzyme, temperature/time) are
  critical.
- Duplex integrity is controlled by the **spray-dryer outlet temperature** (below Tm) and the
  **final matrix**.
- Enzyme clearance depends on **immobilisation** performance.
