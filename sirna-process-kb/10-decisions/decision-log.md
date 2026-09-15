# Decision log

A decision record is required for any choice that closes off an option or that would be
expensive to reverse. Use `TEMPLATE-decision-record.md`.

| ID | Decision | Status | Date | Blocked by | Record |
|---|---|---|---|---|---|
| DR-001 | Synthesis route: fully synthetic solid-phase or chemoenzymatic blockmer plus ligation | **Open** | | OQ-002, OQ-004, OQ-006 | Not yet written |
| DR-002 | DMT-on or DMT-off purification | **Open** | | OQ-013 | Not yet written |
| DR-003 | Single-product or multi-product facility | **Open** | | OQ-009 | Not yet written |
| DR-004 | Drug substance form: lyophilised solid or frozen liquid | **Open** | | OQ-018 | Not yet written |
| DR-005 | Drug substance handled as sterile or low-bioburden | **Open** | | OQ-017 | Not yet written |
| DR-006 | Solvent recovery in scope or out of scope | **Open** | | OQ-012 | Not yet written |
| DR-007 | Strand train segregation: spatial or temporal | **Open** | | OQ-022 | Not yet written |
| DR-008 | Ion-pair reagent strategy given supply and regulatory risk | **Open** | | OQ-011 | Not yet written |

## Decision sequence

These are not independent. A workable order:

1. **DR-001 route**, because it determines which unit operations exist at all. It depends
   on OQ-002, which is a laboratory question answerable quickly and cheaply, and it should
   be answered first rather than debated.
2. **DR-002 and DR-008**, which together define the purification train.
3. **DR-004 and DR-005**, which determine whether lyophilisation and classified areas are
   in the facility.
4. **DR-003 and DR-007**, which set floor area.
5. **DR-006**, which needs solvent volumes from the settled process.

Taking these out of order produces rework. In particular, **freezing facility layout before
DR-004 and DR-005 is the most common and most expensive sequencing error** in this kind of
project.
