# Process overview

The drug-substance train is fully aqueous and runs from received, purified, 5'-phosphorylated
blocks to a dried DS powder.

1. **[Enzymatic ligation](ligation.md)** — dsRNA ligase joins blocks into the strand(s),
   with annealing interleaved so the duplex is co-assembled.
2. **Clarification / enzyme separation** — remove particulates and, with an immobilised
   ligase, the enzyme.
3. **[Filtration & UF/DF](filtration.md)** — desalt, exchange buffer, concentrate, and clear
   whole-block and particulate impurities.
4. **[Evaporation](evaporation.md)** — concentrate further toward the dryer feed.
5. **[Spray drying](spray-drying.md)** — produce the DS powder.
6. **[Microbial control](microbial.md)** — spans the whole train.

See the [block flow diagram](../diagrams/index.md) and the [stream table](streams.md).

## The architecture-critical unknown (Q-001)

Enzymatic evidence says dsRNA nick-sealing ligases require a duplex nick, so annealing is
interleaved with ligation and the material is a **duplex** through the downstream train
([enzymatic ligation](ligation.md)). This favours handling and drying the duplex, but it sits in
tension with the brief's "roughly seven kilodalton" single-strand basis for membrane selection.
Whether the process purifies single strands and anneals at the end, or handles the duplex
throughout, changes UF membrane selection, the filtration analysis, and the drying form. This is
the top open question, **Q-001**.

## Throughput is the driver

All sizing is a function of annual demand, which is not yet given (Q-002). The
[mass balance](../balance/results.md) carries illustrative scenarios so every result re-runs when
the real number arrives.
