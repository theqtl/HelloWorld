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
`SRC-ALMAC-2023` applies a heat treatment at 75 °C between the kinase and ligation steps, and it is
*preparative* — the treated supernatant is carried forward. The lower end came from
`SRC-ANCT4-2022`, whose **body was never retrievable**. Worse, one pass described that figure as a
melting temperature and another as an activity midpoint after a 60-minute hold, with no document
available to settle which. Four independent documents meanwhile chose 85–95 °C for the same duty.

A smaller correction to this page's own wording, made 2026-09-27: the hold was described here as
**"75 °C for 10–30 min"**, and it is not a range. The paper gives two discrete conditions keyed to
which feed is running — verbatim, *"75 °C for 10 min (initial reactions) or 30 min (crude
reactions)"* (`SRC-ALMAC-2023`). A hold time that depends on the feed is not an interval you may
operate anywhere inside, and writing it as one is the same error this page exists to catch,
committed by the page itself.

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

A clearance route was described as costing 71% of the yield. `SRC-DEVRIES-2018` says the opposite.
Verbatim: *"The shown purification process had a recovery yield of 29 (±7)%"* — the **whole**
downstream train, not the clearance step — and *"recovery yield was improved by 3%"* against the
earlier protein-only process (`SRC-DEVRIES-2018`). Most of the loss is elsewhere again: *"During
concentration with ultrafiltration nearly 50% of the produced polySia got lost"* — so the step read
as a 71% cost belongs to a train that **gained** 3 points (`SRC-DEVRIES-2018`), and the 71% was an
overall recovery mistaken for a step loss.

Reported figures that reverse the polarity of their source are the hardest class to catch, because
they are arithmetically consistent with themselves. What the correction itself rests on, stated so
it can be checked: that +3% belongs to the **redesigned process as a whole**, a weaker attribution
than "the step in question improved yield" — `SRC-DEVRIES-2018` credits the caustic treatment and
the membrane adsorbers together and never apportions the gain between them.

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

## What re-retrieving two documents turned up

The five sections below all came from one pass on 2026-09-27 that did nothing but fetch
`SRC-ALMAC-2023`, its supporting information and `SRC-USPTO-10640812` again and read them against what
the registers already said about them. Every document here had been read before — two of them are
graded `full-text-read` and quoted verbatim in the source register.

It produced a corrected void width, a contradiction inside a peer-reviewed paper, an unregistered
process step, a proposed correction that turned out to be wrong, and a note on a sentence this repo
had already quoted for the wrong reason. **None of it needed a source nobody had found.** That is the
argument for re-reading: the marginal cost of a second pass over a document you already have is close
to zero, and the failure mode it catches — a claim that hardened before anyone checked the sentence
next to it — is invisible to every test in the suite.

---

## A void whose width nobody had checked

`P-LIG-SEG-CONC` refuses to carry a range, and the reason has always been that its two ends are
different *kinds* of claim — a success at 1.5 mM and a failure at 10 mM. That refusal is sound and
stands. What was wrong is the number this repo put on the gap: **6.7×**, published flatly in four
registers and this page, as though the width were known.

The low end is **per segment**, and the mix carries a fourth oligonucleotide the register had never
mentioned. `SRC-USPTO-10640812` Example 13 lists its 5 mL charge line by line: 1.5 mM of the centre
segment, 1.5 mM of the 3′ segment, 1.5 mM of the 5′ segment — and *"750 μl 0.00387M Hub (Template)
(0.55 mM final)"*. Three segments at 1.5 mM is 4.5 mM; with the hub the total oligonucleotide loading
is **5.05 mM**.

That hub has no counterpart here, and not as a matter of judgement. It is, verbatim, *"A tri-template
hub (approximately 24 kDa) comprising a support material referred to as the hub and three template
sequences"*, each template *"covalently attached, at its own individual attachment point"*
(`SRC-USPTO-10640812`). `SRC-ALMAC-2023` needs no template species at all: the word "template"
appears **exactly once** in its entire main text, and it is the product's own overhang —
*"The overhang serves as a template for the next annealing step in the alternate strand."*

The high end states no basis whatsoever. *"Starting blockmer concentrations as high as 10 mM"*
(`SRC-ALMAC-2023`) does not say whether that is each blockmer or the sum, and the same paper says each
ligation step starts with three blockmers. So:

| If Almac's 10 mM is… | Comparable low figure | Void (`P-LIG-SEG-CONC`, arithmetic ours) |
|---|---|---|
| a total | 5.05 mM total | **≈2.0×** (`Q-064`) |
| per blockmer, two blockmers | 5.05 mM total | ≈4.0× (`Q-064`) |
| per blockmer, three blockmers | 5.05 mM total | ≈5.9× (`Q-064`) |
| per blockmer, hub excluded | 1.5 mM per segment | 6.7× (`Q-064`) |

**6.7× is the width in exactly one of four readings**, and it was published as if it were the only
one. The honest statement is that the void is somewhere between about 2× and about 6× wide and the
documents do not say which (`Q-064`).

Note which direction this cuts. It does **not** narrow the gap or make the endpoints comparable — it
adds a second unknown on top of the first. The interval's two ends were already different kinds of
claim; now its width is unknown too. The refusal to write a range is better founded than when it
rested on a number.

## A document that contradicts itself, and what that does to a register

Everything above is a claim of ours that failed. This one is different: the **published record is
internally inconsistent**, and no amount of care on our side resolves it.

`SRC-ALMAC-2023`'s main text says the telescoped phosphorylation ran at **5 mM**. Its own supporting
information says **2 mM**. Verbatim, the paper:

> Reaction parameter investigation allowed for final phosphorylation at 5 mM blockmer concentration,
> with a one-pot phosphorylation of 1.2 and 1.3 (5′OH) with PNK-101.

Verbatim, the SI of the same paper (`SRC-ALMAC-2023`):

> Phosphorylation of the 5’-OH blockmers at 2 mM concentration was telescoped into the ligation
> reaction at 1 mM concentration by sequential ligation of 1.4 to form the antisense strand and
> following ligation of 1.1 to yield the full-length duplex as shown in Figure S5.

It is the **same experiment** by every identifier either document offers: the same one-pot
phosphorylation of 1.2 and 1.3, the same sequential ligation of 1.4 then 1.1, the same Figure S5.
Both were retrieved and extracted twice with independent tools; the two figures never co-occur, and
there is no erratum, footnote or "corrected to" anywhere in either document (`SRC-ALMAC-2023`).

**Neither number is carried, and the contradiction is registered instead** — `Q-071`. That is the
only honest move available. Preferring the SI on the usual grounds that it is the more detailed
record runs into the fact that the main text's sentence is the more *specific* of the two, reading as
the outcome of an optimisation; preferring the main text discards the document written to record
exactly this kind of condition. A reader who picks one is guessing, and a register that picks one
hides the guess.

It is not a bookkeeping detail. Both documents agree the ligation itself runs at 1 mM
(`SRC-ALMAC-2023`, `P-CONC-LIG`), so the
charge concentration **is** the dilution the handoff imposes: 2 mM means one volume becomes two in a
single vessel, 5 mM means one becomes five. Those size `U01-LIG` differently by a factor of 2.5, and
the larger one arrives at the top fill where the 65 °C anneal already has a jacket-area problem
(`Q-065`).

!!! warning "Do not confuse this with the contradiction in `Q-059`"
    That one is inside `SRC-CN119265174` and is about **enzyme inactivation** — 80 °C/5 min in one
    example, 85 °C/15 min in another, and centrifugal removal with no thermal step at all in four
    more. This one is inside `SRC-ALMAC-2023` and is about the **phosphorylation charge**. Two
    documents, two unrelated defects. Reported together they would read as one paper with both.

## A process step that was read for its punctuation

The worst near-miss in this slice was not a wrong number. It was a sentence this register had already
quoted, for the wrong reason.

`P-CONC-LIG` and `Q-016` both rest on a count: the whole main text of `SRC-ALMAC-2023` contains
**exactly one** percent sign, in *"100% v/v methanol"*, which is how we know the paper reports no
conversion, yield or purity anywhere. That count is correct and was re-verified. But the sentence it
was counted in reads, verbatim (`SRC-ALMAC-2023`):

> Reactions were incubated at 25 °C at 400 rpm with samples taken at various time points and quenched
> by addition of 100% v/v methanol (MeOH), shaken and centrifuged to pellet any precipitation, and
> supernatants were analyzed by UPLC

The register read that sentence for its punctuation while `Q-059` was recording that nothing
retrieved stopped a reaction chemically. **The quench was in hand and was counted rather than read.**

Two lessons, and the second is the transferable one. First, a source read for one property should be
read for its content at the same time; the marginal cost was zero. Second, and more uncomfortable:
the count was *right*. A verification pass that confirms the claim it set out to check can still walk
past the answer to a different open question, and nothing in a green test suite will say so.

## A correction that did not survive re-retrieval

The three findings above all came from re-reading a document the register had already read. A fourth
came from the same pass and **failed**, which is worth as much page space as the ones that held.

It was put that `SRC-WO2025262452`'s quote in the source register stops one sentence early, and that
the next sentence shows the reaction being stopped chemically rather than thermally — which would
have made the register's *"Termination is a heat kill"* wrong. Retrieved and read, the full passage
is (`SRC-WO2025262452`):

> The reactions were quenched by heating to 95 °C for 20 min to inactivate the enzyme. The inactivated
> reactions were subsequently diluted 400-fold in 10 mM EDTA pH 7.0 and analyzed via HPLC as described
> below.

The document calls the **heat kill** the quench, and applies the EDTA to the *already-inactivated*
reaction as HPLC sample preparation (`SRC-WO2025262452`). The register's reading was right; the
proposed correction was wrong. What the sentence does add is real but smaller — an EDTA dilution used
to hold a finished reaction stable for analysis — and it is now carried as that.

The reason this is on the page rather than quietly dropped: the correction was plausible, specific,
and cited a real sentence. Three of four proposed corrections in this pass survived re-retrieval and
one did not, and a register that only records the survivors will overstate how reliable a
well-argued correction is.

## A solids rejection nobody had registered

The same paragraph carries a step the flowsheet does not have. Verbatim (`SRC-ALMAC-2023`):

> Prior to reactions being used for ligations, the samples were heat treated at 75 °C for 10 min
> (initial reactions) or 30 min (crude reactions), then centrifuged to pellet any precipitated
> material and supernatant used for ligations.

The thermal half was already registered as the kinase kill. The **centrifugation** was not, anywhere:
before this was written, this page contained zero mentions of centrifugation, and every
`centrifug*` in `data/` referred to `SRC-CN119265174` removing an *immobilised enzyme* — a different
duty on a different material at a different point in the route.

What makes it a finding rather than a detail is which centrifugation it is. The paper has three. Two
follow a methanol quench and feed UPLC vials, which is sample preparation. This one's **supernatant
is what goes into the ligation** — a phase separation on the product path, between phosphorylation
and ligation, where no unit operation in the equipment register removes solids.

**No unit operation was added, deliberately.** Two reasons, and the scale one is the real one. The
sentence sits inside the *PNK Screening Reaction* methods paragraph, whose stated format is 96-well
plates — a plate spin is not evidence for a disc stack. And `pfd.UNITS` is derived from
`equipment.csv`, so a new unit cannot be kept off the drawing: it would force a flowsheet width fix
and an SVG re-baseline on the strength of a plate observation. Registered as `Q-072`, which also
records what is genuinely unknown: the paper says only *"any precipitated material"*, and whether
that is denatured cell-free-extract protein (an enzyme-removal duty, bearing on `Q-050` and `Q-032`)
or precipitated oligonucleotide (an unquantified yield loss) decides which equipment it needs.

---

## Every bracket, with a verdict

A range is only a range if its two ends are independent claims. Where they are not, the parameter
carries a blank or a single labelled point and the failure becomes a question — see `Q-057` for the
worked case.

| Bracket | Verdict |
|---|---|
| Concentration, 1.5–10 mM | Two independent documents, **but a success point and a failure point, not a range** — and the two ends are quoted on **different bases**, so the interval's own width is unknown (≈2× to ≈6×, not the 6.7× once published). The low end also crosses cofactor and buffer |
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

- **Characters that are not the character you typed:** the same paper writes the 5′ position with a
  **prime (U+2032)** in its main text and a **right single quotation mark (U+2019)** in its SI, and
  one source prints `Tris–HCl` with an **en dash**. A quote transcribed with the wrong codepoint
  matches nothing, and the failure looks exactly like the claim being absent from the document.
- **A host that was reachable last time:** PubMed Central served a reCAPTCHA challenge page to every
  route tried this session, for a source this register records as reachable. The paper was retrieved
  through the Europe PMC REST service instead. A `reachability` grade is a fact about a date.

The practical consequence is that **a negative result from a single tool is not a negative result**.
Two independent extractors on the same PDF, and a second host for the same document, are the cheapest
insurance available; every quote added on 2026-09-27 was taken that way.

---

## What is deliberately still blank

These are not oversights and should not be filled to make the page look finished.

- **`P-LIG-ENZ-LOAD`** — a loading cannot be written even within one enzyme branch, because the
  candidate loadings are quoted in mutually inconvertible units and the bridging quantities are
  absent from every source read.
- **`P-ENZ-CLEARANCE-LRV`** — no achieved clearance figure exists for either enzyme branch. The
  clearance *duty* is a different quantity and is kept out of this field. See `Q-032`.
- **The quench agent and its charge** — `Q-060`. Still blank, but the reason narrowed on 2026-09-27:
  a chemical stop **is** in the retrieved record after all, and `Q-059` now carries three verified
  instances. Every one of them is at an **analytical sampling point** — a stop solution halting a
  bench ligation time course (`SRC-PBCV1-2014`), an EDTA/SDS quench on capping reactions rather than
  ligations (`SRC-NEB-WO2023173098`), methanol into UPLC vials (`SRC-ALMAC-2023`). None is a
  process-scale termination of a modified-siRNA ligation, so the field stays empty and the question
  stays open on a narrower gap than before.
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
