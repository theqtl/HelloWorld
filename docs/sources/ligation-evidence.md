# Ligation evidence: how well we know each number

This page is the audit trail behind the ligation step's register rows. The registers say **what** a
number is; this page says **how well it is known** — whether it was checked against a document,
reported by a research pass and never re-checked, or computed here from other people's figures.

It exists because that distinction does not survive in a CSV cell. `data/sources.csv` carries the
quotes and `access` grades, and the [reading list](reading-list.md) carries the census of what
nobody has opened. What neither carries is the *history*: which claims were made, which were
overturned before they reached a row, and which reached a row and had to be taken back out.

!!! warning "This is not a literature review, and it is not evidence of quality"
    It records the state of a research pass, including its mistakes. Several claims below were
    **withdrawn** after checking. Read the withdrawals before quoting anything from the earlier
    material — they are not footnotes, they are corrections.

## The three grades, and why the middle one matters most

| Grade | Meaning |
|---|---|
| **Verified** | Re-checked against the document, by extracting its text and matching the claim to it |
| **Reported** | A research pass asserted it and nothing re-checked it. **Not the same as true** |
| **Derived** | Arithmetic performed here on other people's figures. Only as good as its inputs |

The middle grade is the one that caused every problem in this slice. A *reported* figure reads
exactly like a verified one in a register cell, and four of the defects below were reported claims
that a later pass demolished. Where a row rests on a reported figure, the row now says so.

---

## Claims that were withdrawn

These were believed, written down, and then found wanting. Each is listed because the withdrawal is
more informative than the claim.

### The enzyme inactivation band was withdrawn entirely

A bracket of 45–75 °C was proposed for inactivating the ligase. The upper end is sound and verified:
`SRC-ALMAC-2023` applies a heat treatment at 75 °C for 10–30 min between the kinase and ligation
steps, and it is *preparative* — the treated supernatant is carried forward. The lower end came from
`SRC-ANCT4-2022`, whose **body was never retrievable**. Worse, one pass described that figure as a
melting temperature and another as an activity midpoint after a 60-minute hold, with no document
available to settle which. Four independent documents meanwhile chose 85–95 °C for the same duty.

**The bracket is not in the register.** The claim that "neither 85 nor 95 °C is needed" is not
supported, and `SRC-ANCT4-2022` is registered `abstract-only` with an instruction to attribute
nothing from its body. See `Q-061`.

### An endotoxin comparison that compared two different proteins

A ~2.7 log reduction in endotoxin clearance duty was attributed to choosing a purified enzyme over a
crude extract, presented as one paper's controlled comparison. It is not: the two figures are
different proteins, in different tables, from different vectors, and the difference they demonstrate
is between **host strains**, not between purified and crude preparations. On the reported spreads the
ratio spans roughly 1.8–4.1 log rather than a single value. The direction survives — `R-017` still
holds that a cell-free extract raises the clearance burden — but the number does not, and the
quantified form was not written into a row.

### A yield-cost claim that inverted its source

A clearance route was described as costing 71% of the yield. The source says the opposite: its
overall recovery was 29 ± 7% **for the whole process**, and the step in question *improved* yield by
about 3%, with most of the loss occurring in a separate ultrafiltration. Reported figures that
reverse the polarity of their source are the hardest class to catch, because they are arithmetically
consistent with themselves.

### A block-count "sign error" that was not one

`P-N-BLOCKS` carries the claim that more blocks means a lower purity floor, and that was challenged
as a sign error on the strength of `EQ-SPOS`. Re-checked, the register is right: restoring a junction
purity term flips the sign only when junction purity exceeds per-cycle yield, which is not the case
at any realistic ligation purity. `EQ-PURITY` is `f` to the power of the block count and is
monotonically decreasing in it, exactly as the note says.

**What is legitimate is narrower:** the model freezes `f` while varying the block count without
saying so, and `f` depends on block length. That is `Q-058`, and it is a gap in what the model
admits rather than an error in its conclusion.

---

## Defects that were verified, and are fixed

### A yield read as a purity

`SRC-WO2020227618` reads, verbatim, `deoxy-TTACC 5mer (145.5 g, 57.8 mmol, 92.4% yield, 93.6%
purity)`. `P-BLOCK-PUR` took the yield. Because that value is the exponent base of `EQ-PURITY`, the
published drug-substance ceiling was wrong — 77.9% where the source supports 82.0%.

Two further defects in the same row: its lower bound of 89 was a **6.00 g bench** figure sitting
inside a band advertised as hectogram scale, and its note asserted these blocks carry a purity handle
that a 5′-phosphate block lacks, which is false. The chromatography-free hectogram values are exactly
three: 93.6%, 94.8% and 95.6%. See `Q-057`.

### A classifier that classified nothing

The band guard keyed on the literal token `BAND:` in free-text notes. Ten parameters carried a range
and only **nine** carried the token, because one writes `BAND (vendor-published):`. The guard checked
only "flagged but unranged", never the reverse. `range_kind` replaced it as a column, checked both
ways.

### Two parameters that crossed scale silently

`P-LIG-ENZ-LOAD` and `P-LIG-ATP` both attributed conditions from `SRC-ALMAC-2023` to 1 L scale. Those
conditions are from its 96-well plate screening at 0.1 mM blockmer — a tenth of the demonstrated
titre. The paper reports neither figure for its 1 L run.

### A source dismissed as irrelevant that was the best available

`SRC-NEB-WO2023173098` was recorded as "not a ligase". Its Example 3 is titled *"Immobilized T4 DNA
ligase displays stability including thermostability"* and carries the only public reuse and
head-to-head thermal data for an immobilised ligase.

---

## Every bracket, with a verdict

A range is only a range if its two ends are independent claims. Where they are not, the parameter
carries a blank or a single labelled point and the failure becomes a question — see `Q-057` for the
worked case.

| Bracket | Verdict |
|---|---|
| Concentration, 1.5–10 mM | Two independent documents, **but a success point and a failure point, not a range**. The low end also crosses cofactor and buffer |
| `P-LIG-TIME` | Two documents; one measurement plus one unverifiable |
| Inactivation temperature | **Withdrawn** — one verified endpoint for the wrong enzyme and step, one unverifiable |
| Turndown | **One source both ends**, same example, and one end calculated where the other is measured |
| Clearance duty | Measured loading at each end, but both titres are derived here and one endpoint is a construction |
| Depth-filter throughput | Unverifiable here, and the wrong system at both ends |
| Nickel leaching | **One source both ends**, plus a system crossing: both are elution conditions, and the process never elutes |
| Endotoxin assay floor | One measurement plus one figure absent from its cited document. **Not written** |
| Bioburden | **One source both ends**, adjacent sentences, and the two ends are different process stages |
| Conversion assay floor | A reporting threshold plus an unverified figure; both the wrong matrix |
| Enzyme-to-product mass ratio | **Not a bracket** — one computation with the denominator switched between ends |
| `P-N-BLOCKS` | **Two genuinely independent endpoints**, better sourced than first claimed |
| `P-BLOCK-PUR` | Both measurements from one document, **plus** an independent first-principles reproduction of the same span |
| `P-DS-TM` | One source both ends, already flagged in the register |
| `P-EPS-260` | An argued bracket with no source at either end, correctly registered as such |

Of fifteen, **five have both ends from one source**, one is not a bracket at all, two could not be
checked, and one was not written. That is the bracketing discipline applied to its own output.

---

## Retrieval reality

Reproducing this research is not a matter of following the citations. Several hosts blocked
programmatic access, and the tooling was asymmetric in ways that produced wrong answers rather than
error messages.

- **Long patents:** `curl` on the patent host worked and the fetch tool **silently truncated**,
  returning a confident "no data" for a document that contained the data. One such false negative was
  caught only because a second pass used a different route.
- **Publisher PDFs:** the reverse — the fetch tool reported a well-formed regulatory PDF as corrupt
  while `curl` retrieved it intact.
- **Hard blocks:** two patent offices, two large publishers and one vendor site returned 403 to every
  route tried. `SRC-OPRD-2025` remains unretrieved for this reason and, per its own note, nothing is
  attributed to it.
- **Image-only tables:** `SRC-CN119265174` carries its per-condition numbers in image tables absent
  from the text layer, so its conversion and endotoxin figures are prose assertions rather than
  retrievable tables. The register says so.

The practical consequence is that **a negative result from a single tool is not a negative result**.

---

## What is deliberately still blank

These are not oversights and should not be filled to make the page look finished.

- **`P-LIG-ENZ-LOAD`** — a loading cannot be written even within one enzyme branch, because the
  candidate loadings are quoted in mutually inconvertible units and the bridging quantities are
  absent from every source read.
- **`P-ENZ-CLEARANCE-LRV`** — no achieved clearance figure exists for either enzyme branch. The
  clearance *duty* is a different quantity and is kept out of this field. See `Q-032`.
- **The quench agent and its charge** — `Q-060`.
- **A duplex melting temperature for our own sequence** — `Q-030`.
- **The enzyme form itself** — `Q-050`, which is why no denature unit appears in the equipment
  register.

## Where the numbers themselves live

| Register | What it holds |
|---|---|
| [`envelopes`](../registers/envelopes.md) | each bracket, with a separate source and scale note per endpoint |
| [`couplings`](../registers/couplings.md) | which variables are not independent, and which corners are unreachable |
| [`infoneeds`](../registers/infoneeds.md) | the information a designer needs, with its anchor clause and disposition |
| [`verdicts`](../registers/verdicts.md) | the acceptance panel, one row per reviewer |
| [`sources`](../registers/sources.md) | every document, its `access` grade and its verbatim quotes |
| [`questions`](../registers/questions.md) | every gap this page names |

The readable synthesis is the [ligation design envelope](../process/ligation-envelope.md), generated
from those registers. This page is its provenance.
