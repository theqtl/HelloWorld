"""Generation layer: reads data/*.csv (single source of truth), computes the
mass and energy balance from flagged assumption inputs, and emits Markdown
pages under docs/. Run `python -m gen.build` from the repo root before mkdocs.

`provenance` has four values (gen/dataio.py PROVENANCE_VOCAB). The balance's
inputs can only ever be `fact`, `inference` or `assumption`: an educated
estimate is carried in `est_value` and `param_value` reads `value`, so the
fourth value cannot reach a computed number at all.
"""
