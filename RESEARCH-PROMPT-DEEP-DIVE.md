# Deep research dive: prompt for a new session

Paste everything inside the fenced block below into a fresh Claude Code session on this
repository. It is self-contained. Nothing else needs to be carried over.

---

```text
You are running a deep literature and evidence dive on an existing siRNA drug-substance
knowledge base. Read this whole brief before you touch anything.

## 0. What this is, and what it is NOT

This repository already contains a Tier-1 knowledge base for an enzymatic-ligation siRNA drug
substance process and its greenfield cGMP facility. The site is live at
https://theqtl.github.io/HelloWorld/ and builds from `main`.

Your job is to go DEEPER on the process concepts already in the site, and to bring back
evidence. Your job is NOT to redesign anything.

NON-GOALS, and these are hard:
- Do not propose a different process. Enzymatic ligation, filtration-led purification,
  evaporation, spray drying and microbial control are settled decisions. Do not relitigate
  them. Do not suggest lyophilisation.
- Do not add or remove unit operations, streams, equipment or equations.
- Do not edit the findings, process, equations, balance, facility, development, tech-transfer
  or diagram pages. Do not edit the mass balance code or any parameter, risk, question,
  stream, equipment, buffer or utility register.
- Do not invent, round, extrapolate or "tidy" a number. Ever. See section 4.

## 1. Files you may write. Everything else is read-only.

You may modify exactly three files:

1. `data/sources.csv` — append newly discovered sources. You may also correct the
   `reachability`, `notes` or `verified` fields of an EXISTING row if, and only if, your
   research proves the current entry wrong. Do not delete rows. Do not change `source_key`
   values, because the documents link to them.
2. `docs/sources/reading-list.md` — rewrite into the expert curriculum described in section 6.
3. `RESEARCH-QUEUE.md` at the repository root — create this. It is the flagged-findings
   handover described in section 7. It is deliberately outside `docs/` so it does not become
   a site page and cannot affect the strict site build.

If you believe something else must change, do not change it. Write it into RESEARCH-QUEUE.md
as a proposed action for a future session. That is the entire point of the queue.

## 2. Orient yourself first

Before searching anything, read these, in this order:

- `docs/sources/reading-list.md` — what has already been prioritised
- `data/sources.csv` — 35 registered sources, with `reachability`, `scale_system` and a
  `verified` column recording what was checked and when
- `data/questions.csv` — 21 open questions, Q-001 through Q-039. These are your targets.
- `data/risks.csv` — 12 risks, R-001 through R-012
- `docs/findings/filtration.md` and `docs/findings/spray-drying.md` — the two headline findings
- `docs/adr/0001-information-architecture.md` — why the site is built the way it is
- `README.md` — the provenance discipline you must follow
- `gen/test_balance.py` — the 23 tests, four of which police citations. Read these before you
  write a single CSV row, because they will fail your build if you get it wrong.

Rows in `data/sources.csv` carrying a `verified` date of 2026-09-17 were checked against the
actual works during a citation audit. Do not redo that work. Three things that audit could NOT
settle are explicitly yours to close if you can:
- Which membrane molecular-weight cut-offs were tested in the siRNA ultrafiltration study
  (Q-035). The abstract does not enumerate them.
- The real bioburden and endotoxin limits for oligonucleotide drug substance (Q-037). The
  oligonucleotide-specific paper was paywalled and unread, and the ladder currently on the
  microbial page is known to reproduce a mammalian cell-culture article.
- The ~193 g/L concentration figure attributed to the 2025 ligand-density paper. Unverified.

## 3. The failure mode you are here to avoid repeating

An audit of this repository on 2026-09-17 found that roughly one claim in eight had a real,
on-topic source attached to a number that does not appear in it. The specific failures:

- A glass transition stated as ~117 C, cited to a paper that measured 38 to 53 C. The error
  survived because the source was labelled "paywalled (abstract only)" when it was in fact
  open access at PubMed Central, so nobody opened it.
- A concentration ceiling of ">190 g/L" cited to a paper that reports 52 to >180 mg/mL. The
  higher figure belongs to a different paper by the same group.
- A rule about ultrafiltration resolution cited to a patent about microdialysis for mass
  spectrometry, which says nothing on the subject.
- A purity rule attributed to a European assessment report that contains no numeric criteria
  at all. It is in fact an FDA recommendation, and it applies to guide RNA, not to siRNA.
- Two papers credited to authors who are not on them.
- Numbers with no traceable source at all: a vendor titre, an RNA recovery figure.

Every one of these was plausible. None was fabricated out of nothing. They are what happens
when a real source is read as an abstract and a number is remembered from somewhere else.

Assume you will make the same class of error unless you actively prevent it.

## 4. Evidence rules. These are not negotiable.

1. **Quote or it did not happen.** Every numeric or factual claim you record must be
   accompanied by a verbatim quotation from the source, stored in the `notes` field. If you
   cannot quote it, you have not verified it.
2. **Check reachability before you believe it.** Before marking anything paywalled, check:
   PubMed Central, Europe PMC, Unpaywall, the publisher's own open-access flag, institutional
   repositories (ScholarSphere, Pure, DiVA, EThOS, TU Delft, university theses), preprint
   servers (bioRxiv, ChemRxiv, SSRN, arXiv), the corresponding author's personal or lab page,
   and any conference proceedings version. The 117 C error is entirely attributable to
   skipping this step.
3. **Record scale and system for every number.** A bench result on unmodified RNA does not
   transfer to kilograms of modified phosphorothioate siRNA. Food and dairy evaporation data
   does not transfer to an oligonucleotide duplex without saying so. Put it in `scale_system`.
4. **Separate what the source says from what you concluded.** If the source says X and you
   infer Y, record X and label Y as inference. Do not blend them.
5. **A gap stays a gap.** If you cannot source a value, it is blank and it is a registered
   finding. A plausible fabricated range is worse than a blank, because it will be designed
   against and nobody will remember where it came from.
6. **Attribution matters.** Verify the author list, year, volume and identifier of every
   source you add, against Crossref or the publisher record, not against a search snippet.
7. **Do not trust automated extraction of mathematics.** Two independent automated reads of a
   spray-drying paper during the audit returned dimensionally impossible forms of the same
   equation. If you extract a formula, check its dimensions by hand.
8. **Check for retractions and corrections** on any source that will carry weight. Retraction
   Watch, PubPeer, the publisher's erratum list. One source in the register already has a
   known erratum.

## 5. The research programme

Run this as parallel teams with their own context. Use the deep-research skill if it is
available to you; otherwise spawn parallel agents with the Agent tool and give each one its
own stream. Do not run them sequentially, and do not do it all yourself in one context.

Each stream below names the questions it is trying to close. Go after those specifically.
Breadth for its own sake is not useful here. Depth on a named gap is.

### Stream A — Enzymatic ligation, at scale
Targets: Q-010 (conversion), Q-016 (reactor concentration), Q-032 (enzyme clearance),
Q-034 (titre), R-002, R-010.
Dig into: engineered dsRNA ligase patent families and their worked examples; adenylylated
dead-end (AppN) formation and its suppression by ATP control, enzyme choice and reaction
staging; immobilised and solid-phase ligase systems and any measured residual-protein
clearance in ppm or log reduction; ATP cost, recycle and regeneration at kilogram scale;
kinase phosphorylation as a telescoped step; GMP enzyme supply, cell-free extract versus
purified enzyme, and the regulatory expectations for a residual enzyme as a process-related
impurity.

### Stream B — Block chemistry and how purity propagates
Targets: Q-011 (block purity), Q-033 (DS specification), R-001.
Dig into: convergent and liquid-phase oligonucleotide synthesis at kilogram scale; measured
fragment purities and yields; mechanisms and rates of n-1 formation in modified RNA;
depurination, desulfurisation and the P=O impurity; 5'-phosphate installation chemistry and
its completeness; how fragment-internal impurity is actually measured; and what a block
specification looks like in practice.

### Stream C — Membrane science for a concentrated polyanion
Targets: Q-017 (UF concentration limit), Q-020 (diavolumes), Q-035 (cut-offs), Q-036 (flux
and recovery), R-011.
Dig into: the full Penn State membrane corpus on siRNA ultrafiltration, including theses,
which typically contain the data the papers compress; charged and surface-modified membranes;
Donnan exclusion and ionic-strength effects on apparent size; real versus nominal retention;
concentration polarisation and gel models applied to nucleic acids rather than proteins;
viscosity and osmotic pressure of concentrated polyelectrolyte solutions; membrane cascade
design; hold-up volume and recovery; single-use versus reusable flow paths and cleaning
validation. A specific task: the four governing equations on the site currently lean on an
anonymous secondary website whose domain is six months old. Find primary sources for
diafiltration clearance, gel-polarisation flux, area sizing and sieving, and register them.

### Stream D — Evaporation of a heat and shear sensitive biomolecule
Targets: Q-018 (evaporator outlet concentration and viscosity limit), R-004.
Dig into: falling-film, wiped-film and thin-film residence time distributions and how they are
actually measured; film thickness and wetting rate limits; boiling-point elevation in
concentrated salt and polyelectrolyte solutions; fouling and foaming; mechanical vapour
recompression energy as a function of temperature lift rather than as a single number;
overall heat transfer coefficients for viscous biological streams; and any precedent at all
for evaporating a nucleic acid solution. If there is no precedent, that is a finding worth
stating plainly.

### Stream E — Spray drying a duplex
Targets: Q-019 (feed solids), Q-021 (excipient ratio and matrix), Q-030 (duplex Tm),
Q-039 (glass transition at achieved moisture), R-003, R-008.
Dig into: nearest-neighbour thermodynamic parameters for 2'-OMe, 2'-F and phosphorothioate
modified duplexes, because the melting temperature gap may be closable by calculation from
published parameters rather than by measurement; measured glass transitions of sugar glasses
as a function of residual moisture; excipient screening for nucleic acids; atomiser selection
and shear on duplexes; outlet temperature and particle temperature relationships at pilot
versus bench scale; cyclone and wall losses at scale; residual moisture specification and
storage stability; and dryer cleaning and containment for a low-bioburden product.

### Stream F — Microbial control, endotoxin and the contamination control strategy
Targets: Q-031 (nuclease control), Q-037 (bioburden and endotoxin limits), R-007, R-009,
R-012.
Dig into: the oligonucleotide-specific microbiological control literature, which is the single
most important unread source in the register; pharmacopoeial chapters and their actual limits;
endotoxin clearance by charged adsorbers with a polyanionic product competing for sites; hold
time studies; water quality per process step; and whether chemical modification genuinely
makes aggressive nuclease control unnecessary, with evidence rather than assertion.

### Stream G — Regulatory and specification reality
Targets: Q-033 (DS purity specification), and the scoping of every regulatory claim on the
site.
Dig into: what is actually disclosed about approved siRNA drug substance specifications, and
where. The European assessment reports redact numbers. Other jurisdictions do not always
redact the same things. Look at Japanese review reports, Health Canada summary basis of
decision documents, Australian public assessment reports, and United States chemistry
reviews, for the same molecules. Approved product labels disclose formulation composition,
which bears directly on the excipient question. Also: draft and final oligonucleotide-specific
guidance, pharmacopoeial expert panel stimuli articles, and the distinction between a
recommendation, a guideline and a specification. Be precise about which is which, because the
site has already been burned once by treating a guide-RNA recommendation as an siRNA
specification.

### Stream H — Process development, scale-up and the engineering package
Targets: Q-012 (step yields), and the development and tech-transfer pages.
Dig into: scale-down model qualification for tangential flow filtration, evaporation and
spray drying; what actually breaks first on scale-up for each; design-of-experiments
strategies used in oligonucleotide process development; process analytical technology
genuinely deployed on these unit operations; and the engineering standards that bind a
package of this kind.

## 5a. Think outside the obvious sources

Journal articles and vendor blogs are the shallow end. The following classes have repeatedly
held the data that papers omit, and the previous research pass barely touched them:

- **Theses and dissertations.** A doctoral thesis usually contains the full data set behind
  three papers, including the failed conditions, and is almost always open access. For the
  membrane work in particular this is likely the highest-yield single move available to you.
- **Patent families, not patents.** Follow the family and the continuations, read the worked
  examples rather than the claims, and check the cited-by list. Opposition and third-party
  observation filings often contain experimental data submitted to argue a point.
- **Non-English regulatory reviews.** Japanese and Chinese review documents for the same
  approved products sometimes disclose chemistry and manufacturing detail that is redacted
  elsewhere.
- **Conference proceedings and posters.** The oligonucleotide therapeutics meetings, membrane
  society meetings, and engineering society sessions carry process data years before it is
  published, if it is ever published.
- **Vendor application notes and technical reports** from membrane, evaporator and dryer
  suppliers. These often contain the only real flux, duty and yield numbers in existence.
  Treat them as vendor claims and tag them as such, but do not ignore them.
- **Grant abstracts and award databases.** Public funding records reveal what companies and
  groups are actively trying to solve, which tells you where the real gaps are.
- **Approved product labels and their formulation sections.**
- **Citation chasing in both directions** from the sources already registered, plus
  "related article" and citation-graph tools. The single most reliable way to find the paper
  you need is to look at who cited the one you have.
- **Adjacent industries.** Messenger RNA and plasmid DNA tangential flow filtration, dairy and
  food evaporation, inhaled biologic powders, and industrial enzyme immobilisation. Transfer
  is a judgement call, so record the scale and system and let the reader decide.

## 6. Deliverable one: the reading list becomes an expert curriculum

Rewrite `docs/sources/reading-list.md` so that a competent engineer who reads it top to bottom
finishes able to hold their own with a specialist. Structure it as a curriculum, not a pile:

- **Tier 0, orientation.** A handful of items that give the vocabulary and the shape of the
  field. Short. Open access only.
- **Tier 1, the load-bearing sources.** The ones the site's conclusions actually rest on.
- **Tier 2, depth by unit operation.** Grouped by ligation, blocks, filtration, evaporation,
  drying, microbial control.
- **Tier 3, regulatory and standards.** What you must be able to cite by name.

Every entry carries: the full citation, a working access route with the open-access mirror
named explicitly where one exists, an honest reachability note, an estimated reading time,
the question or risk identifier it unblocks, and one or two sentences on what the reader will
take away from it.

Add two sections that do not exist today:

- **"What you must be able to say."** Fifteen to twenty statements that constitute fluency in
  this process, each with the source that backs it. This is the section that makes someone
  credible in a room.
- **"Claims to not repeat."** Numbers and rules that circulate in this field but that you have
  established are unsupported, mis-scoped or misattributed, with what is actually true. Being
  able to correct a confident wrong number is worth more than knowing ten right ones. Seed it
  with the six failures listed in section 3 and add whatever you find.

## 7. Deliverable two: the findings queue

Create `RESEARCH-QUEUE.md` at the repository root. This is a handover to a future session that
WILL be allowed to edit the rest of the site. Every finding gets an entry in this form:

    ### F-001 — one-line statement of the finding
    - Stream: C (membranes)
    - Type: new-number | contradiction | closes-gap | new-risk | new-question | source-upgrade
    - Affects: docs/process/filtration.md, UF/DF design basis; Q-017; P-CONC-UF
    - Source: SRC-XXXX-YYYY (registered in data/sources.csv)
    - Verbatim: "the exact sentence from the source"
    - Scale/system: bench scale, modified siRNA duplex
    - Confidence: read in full | abstract only | inferred
    - Why it matters: one or two sentences
    - Proposed action: what a future session should change, and where

Order the queue by impact, highest first. Call out separately, at the top:
- any finding that CONTRADICTS something currently on the site
- any finding that CLOSES an open question, with the question identifier
- any finding that opens a NEW question or risk that is not yet registered

Do not make those edits yourself. Queue them.

## 8. Verify your own team's work before you write anything

This is the step the previous pass skipped, and it cost a day of rework.

Subagents make the same class of error as anyone else. In the audit that prompted this brief,
two of the criticisms raised against the repository did not survive contact with the actual
text, and a third was an artifact of a badly constructed test.

So: after your research streams report, run an independent verification pass over every
finding that will be written. Give the verifier the claim and the source, not the researcher's
reasoning, and have it answer confirmed, unverifiable, contradicted or misattributed, with a
quotation. Anything that does not come back confirmed goes into the queue flagged as such, or
does not go in at all.

Then sanity-check yourself: pick three of your own new claims at random and personally open
the source.

## 9. Finish clean

- Run `python -m pytest gen -q`. All tests must pass. Note in particular that a test lints
  prose citations: any patent number or digital object identifier that appears in
  `docs/sources/reading-list.md` must also exist in `data/sources.csv`, or the build fails.
  Another test asserts that no source is marked paywalled when an open-access identifier
  exists for it.
- Run `python -m gen.build` and then `mkdocs build --strict`. Both must be clean.
- Commit to this session's designated branch and push. Do not open a pull request unless
  asked. Do not merge to main.
- Report back in chat, not in the repository, with: how many sources you added and how many
  you could not reach; which open questions you closed, with the answer; which you could not
  and why; the three findings most likely to change the design; and anything currently on the
  site that you believe is wrong.

## 10. What good looks like

The owner should finish reading your curriculum and be able to walk into a room with a
contract manufacturer and an engineering firm, ask the right questions, recognise a wrong
number when they hear one, and know precisely which facts are established, which are
inferred, and which are still open. Nothing you write should require them to take your word
for it.
```
