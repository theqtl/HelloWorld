# siRNA modality notes

## What makes siRNA manufacturing distinct

1. **Two strands, two trains, one product.** Sense and antisense are synthesised and
   purified independently, then annealed. The facility must accommodate two parallel
   campaigns plus a joining step, and the annealing step is where two separately released
   intermediates become one drug substance.
2. **Purification is resolution-limited, not capacity-limited.** Unlike protein capture,
   where binding capacity drives sizing, oligonucleotide chromatography is sized by the
   load at which n-1 still resolves from full-length product. **[SEED]**
3. **Heavy organic solvent duty.** Solid-phase synthesis consumes large volumes of
   acetonitrile. Ion-pair reverse phase purification consumes more, along with ion-pair
   reagents. This drives flammable-solvent area classification, solvent recovery, and
   environmental permitting in a way that biologics facilities do not experience.
4. **Amidite supply is the critical raw material risk.** Modified amidites, particularly
   2'-F and conjugate building blocks, have concentrated supply chains and long lead
   times, and they dominate cost of goods.
5. **Scale is intermediate.** Commercial siRNA demand sits between small molecule tonnage
   and biologics kilogram scale, which means equipment is often at the top of the
   pharmaceutical range and at the bottom of the fine-chemical range.

## The two candidate routes

| | Fully synthetic solid-phase | Chemoenzymatic blockmer plus ligation |
|---|---|---|
| Strand assembly | Stepwise phosphoramidite to full length | Short blocks synthesised, then enzymatically joined |
| Best fit length | Suits siRNA length well | Advantage grows with length, so more compelling above roughly 40 nt |
| Amidite consumption | Full length per strand | Same total, but shorter synthesis columns and better stepwise yield per block |
| Added impurities | None beyond synthesis | Splint, ligase, adenylylated species, unligated blocks |
| Added unit operations | None | Ligation reaction, splint digestion, protein clearance |
| Regulatory familiarity | Well established | Less established for this modality |
| Where it wins | Standard siRNA duplexes | Long or highly modified constructs, or where a shared blockmer library serves several products |

**Honest assessment for siRNA specifically:** at typical siRNA strand lengths of 19 to 23
nucleotides, stepwise solid-phase synthesis is not yield-limited in the way that long RNA
synthesis is. The classic argument for blockmer plus enzymatic ligation, escaping the
compounding of stepwise yield over many cycles, is much weaker here. **[SEED]**

Blockmer approaches still have a real case for siRNA, but it is usually a *different*
case, and it is worth being precise about which one is being pursued:

- **Block amidites**, meaning dimer or trimer phosphoramidites coupled chemically, reduce
  cycle count and can control phosphorothioate stereochemistry. This is a chemistry
  strategy, not an enzymatic one.
- **Enzymatic ligation** of blocks is most compelling if a platform library of common
  blocks can be shared across multiple products, or if specific modification patterns are
  inaccessible by direct synthesis.

See `03-process/upstream/blockmer-prep.md` and
`03-process/upstream/enzymatic-ligation.md`, and record the route rationale as a decision
record. Do not let the route be decided implicitly by whichever folder gets filled in first.

## Heavily modified backbone constrains ligation

A fully modified siRNA has few or no unmodified riboses. Enzymatic ligation generally
requires near-native chemistry at the junction. If the target modification pattern leaves
no viable junction, the enzymatic route is closed regardless of its other merits. This
should be checked **first**, before any process design effort is spent on it. Recorded as
open question OQ-002.
