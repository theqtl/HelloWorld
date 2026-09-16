# Audit — session "siRNA process and facility design" (2026-09-16)

Audited: branch `claude/sirna-process-facility-design-jfoyxt`, commits `1380305` and `10cef38`.
Brief audited against: `RESEARCH-PROMPT.md` on branch `claude/repo-contents-gi4yvu`.
Auditor re-ran every check below in a clean checkout of the branch.

## Verdict

The Tier-1 deliverable is real, internally consistent, and honest about its gaps. The work is
about a third of the brief by scope, which it states plainly rather than overclaiming. Two
things need the author's attention: continuous integration is red on both commits, and the
information architecture is the one the brief said had already been rejected.

## What was verified to work

| Check | Result |
|---|---|
| `python -m pytest gen -q` | 9 passed |
| `python -m gen.build` | regenerates all 10 generated pages |
| Mass-balance arithmetic, scenario S1 | reproduced by hand end to end |
| `docs/diagrams/bfd.svg` | parses as well-formed XML |
| All 9 `data/*.csv` | parse; 85 rows total |
| Internal Markdown links | 0 broken |
| Identifier integrity (Q-, R-, P-, SRC-, EQ-, stream, equipment, buffer) | all referenced ids are defined |
| `mkdocs.yml` nav | all 27 targets exist after generation |
| CI `build` job | succeeded on both commits |
| Pull request | none opened, as the brief instructed |

## Findings

### 1. CI is red on both commits; the site has never published

The `build` job passes (tests, generation, `mkdocs build`, artifact upload all green). The
`deploy` job fails after about two seconds on both runs, so the whole workflow is red and no
site was ever deployed. The job logs have since expired (HTTP 404), so the cause is not
directly retrievable. It is consistent with GitHub Pages still being set to the legacy
branch-build source rather than "GitHub Actions" — the repository's older Pages runs are all
of the `dynamic/pages/pages-build-deployment` kind. The README does document enabling this as
a manual step, but the effect is a red branch and an unpublished site.

Related: `.github/workflows/pages.yml` lists the feature branch alongside `main` as a deploy
trigger, so merging as-is would let a feature branch publish to production Pages.

### 2. The architecture is the one the brief called rejected

The brief states that a previous attempt using "markdown files and CSV registers in a folder
tree" was rejected as not user friendly, specifically for diagrams and equations. What was
built is Markdown files and CSV registers in a folder tree, wrapped in MkDocs Material.

The wrapper does answer the two stated objections: the block flow diagram is hand-authored
vector SVG with stream numbers tied to the balance, and equations are typeset through MathJax.
Search, sortable tables and cross-links are present. So the rejection may well be satisfied in
substance. But it is close enough to the rejected form that the author should confirm it, and
the brief also required weighing five named architecture options and justifying the rejects.
No such decision record exists in the repository.

### 3. An uncited source supports two claims flagged as fact

The rule that ultrafiltration needs roughly a tenfold molecular-weight ratio, and that the
resolution band is about plus or minus half the cut-off, is attributed to "Sigma / USPTO
6187190" in both the filtration finding and equation EQ-UFRULE, and is marked **fact**. That
reference is not in `data/sources.csv` and has no source key. The reading list also names patent
US12275983, which is likewise unregistered.

This matters more than its size: the argument that no filtration mode can resolve n-1 rests on
that rule, and it is the central finding. The test suite validates `source_key` columns in the
CSVs but cannot see citations written in prose, so this class of gap is invisible to CI.

### 4. Wrong question id on every throughput scenario

All three rows of `data/scenarios.csv` say the governing open question for annual demand is
Q-001. Q-001 is the annealing and product-form question. Demand is Q-002, which the index and
the balance method page both cite correctly.

### 5. Scope delivered against the brief

Delivered: the information architecture and build, the executable scenario mass balance, both
headline findings, seven process pages, ten governing equations, the block flow diagram, and
nine seeded registers with reachability and scale tags on every source.

Not delivered, and mostly marked as such in the pages themselves:

- The energy balance is the latent-heat minimum only. Sensible heat, drying-gas load and real
  duties are deferred to a later tier, so utility sizing cannot yet be done from it.
- Three equations the brief asked for by name are absent: membrane cascade staging,
  boiling-point elevation, and droplet drying kinetics. Boiling-point elevation and droplet
  kinetics are discussed in prose but never given as equations with terms and validity.
- No process flow diagram with instrument tags; the block flow diagram is the only flowsheet.
- Facility concept, process development and tech transfer are one-page sketches.
- Research streams B, D, G, H, I and J from the brief are present only at sketch depth.

### 6. Balance model defects

- Evaporator outlet volume is computed from the active ingredient concentration alone and
  ignores excipient already in solution, so evaporation water removed is overstated. Excipient
  is counted later at the dryer, so the two stages use different bases without saying so.
- Six declared parameters are never read by the balance: the four molecular weights, the
  ligation conversion and the block purity. Conversion in particular is flagged as a balance
  assumption in the register but does not affect any balance output.
- `run_scenario` opens with a dead local variable `conv = 1.0`.
- A hard-coded latent-heat fallback of 2400 kJ/kg sits behind the parameter lookup, which
  slightly undercuts the stated guarantee that a blank input always raises rather than
  silently producing a number.

None of these change the direction of any conclusion. All are cheap to fix.

### 7. Repository hygiene

- Both commit messages carry a `Co-Authored-By` trailer naming a model that is not the model
  the session ran on, and model identifiers should not be written into repository artifacts at
  all.
- The second commit deletes the two uploaded JPEGs and `config.yml` that are still on `main`.
  This matches the intent of the separate "clear repository" commit on the other branch, but
  merging this branch would remove those files from `main`.

### 8. The session terminated before Tier 2

The last commit landed at 03:36 UTC. The session ran until 15:17 UTC and ended on a policy
error, with no further commits. Whatever was produced in those eleven and a half hours is not
in this repository and cannot be recovered from it.

## Recommended order of work

1. Switch Pages to the GitHub Actions source, or drop the deploy job until it is switched, and
   remove the feature branch from the deploy trigger.
2. Register the ultrafiltration resolution source properly, or downgrade the two claims that
   rest on it from fact to inference.
3. Fix the Q-001 / Q-002 reference in `data/scenarios.csv`.
4. Confirm with the author that the MkDocs architecture is accepted before building Tier 2 on
   top of it, and record the architecture decision and the rejected options.
5. Correct the excipient basis in the evaporation step and either use or retire the six unused
   parameters.
