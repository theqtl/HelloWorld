# Regulatory landscape

> **[SEED]**. Verify currency of every reference before relying on it. Guidance in the
> oligonucleotide space is actively evolving.

## Core ICH guidance

| Reference | Relevance here |
|---|---|
| ICH Q7 | GMP for active pharmaceutical ingredients. The governing GMP standard for drug substance |
| ICH Q8 | Pharmaceutical development, QTPP and CQA framework |
| ICH Q9 | Quality risk management, the basis for the risk register |
| ICH Q10 | Pharmaceutical quality system, and the source of the knowledge management concept this repository implements |
| ICH Q11 | Development and manufacture of drug substances. Starting material designation and control strategy |
| ICH Q12 | Lifecycle management, post-approval change |
| ICH Q13 | Continuous manufacturing, if any step is run continuously |
| ICH Q14 | Analytical procedure development |
| ICH Q2(R2) | Analytical procedure validation |
| ICH Q3A and Q3B | Impurities in new drug substances and products |
| ICH Q3C | Residual solvents. Directly binding given acetonitrile use |
| ICH Q3D | Elemental impurities |
| ICH M7 | Mutagenic impurities. Assess reagents and by-products |
| ICH Q6A | Specifications |

## Oligonucleotide-specific position

There is **no dedicated ICH guideline for oligonucleotide drug substances**. The field
operates on a combination of small-molecule guidance, health authority feedback, and
industry consensus positions. Two consequences for a greenfield project:

1. **Precedent matters more than usual.** Approved oligonucleotide products and their public
   assessment reports are a primary source, and reading them is time well spent.
2. **Engage regulators early**, particularly on starting material designation, impurity
   qualification thresholds for sequence-related impurities, and the control strategy for
   impurities that cannot be resolved analytically.

Industry bodies working in this space, including the oligonucleotide safety and CMC working
groups, publish consensus positions that carry weight in discussions even without formal
guideline status. **[SEED]** Track their current output rather than relying on this note.

## Impurity qualification, the genuinely hard problem

Sequence-related impurities such as n-1 and n+1 are structurally similar to product and are
present at low levels as a family of many individual species. Qualifying them individually
is impractical. The accepted approach is generally a **family or group-based control**
supported by a scientific rationale, but the specifics are negotiated rather than
prescribed. This should be a named topic in early regulatory interaction. Tracked as OQ-023.

## Facility and systems

| Reference | Relevance |
|---|---|
| EU GMP Annex 1 | Sterile manufacture, if OQ-017 resolves to sterile |
| EU GMP Annex 11 and 21 CFR Part 11 | Computerised systems, data integrity |
| EU GMP Annex 15 | Qualification and validation |
| 21 CFR 210 and 211 | US GMP |
| ASTM E2500 | Verification of manufacturing systems |
| GAMP 5 | Computerised system validation approach |

## Non-GMP obligations that bind the design

Environmental permitting, solvent emission limits, fluorinated compound restrictions, and
occupational exposure regulation are jurisdiction-specific and can be as constraining as
GMP. Site selection should account for them explicitly. See the hexafluoroisopropanol
discussion in `04-materials/raw-material-strategy.md`.
