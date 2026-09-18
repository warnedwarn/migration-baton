# Migration Baton

## Service bulletin 00 — the route

This contract treats a migration as an ordered line, not a checkbox collection. The maintainer publishes three to eight distinct stations, nominates a separate operator, freezes a rollback anchor, and sets a bounded operating window.

```text
PLANNED ── begin ──> IN_PROGRESS ── each station in order ──> COMPLETED
                         │                                  │
                         ├── deadline ──> EXPIRED           └── justified evidence ──> ROLLED_BACK
                         └── justified evidence ─────────────────────────────────────> ROLLED_BACK
```

## Service bulletin 01 — no express trains

`pass_checkpoint` accepts only `next_index`. Each proof must use a fresh HTTPS origin, distinct from the rollback anchor and all earlier stations. Validators fetch both the frozen anchor and the new proof, then independently agree that the checkpoint passed *and* the anchor remained intact. The exact proof digest is appended to the route record.

## Service bulletin 02 — exits stay usable

The operator or maintainer may roll back only with validator-confirmed evidence of a failed checkpoint or violated invariant. If the operator disappears mid-route, expiry is permissionless after the deadline.

## Timetable inspection

```bash
genvm-lint contracts/contract.py
python -m pytest -q
```

Tests cover a complete ordered route, attempted station skipping, a forged anchor verdict, and permissionless expiry. Evidence files are operator-created technical fixtures, never described as independent authorities.

## Network terminus

StudioNet contract: [`0x034E9Eee99952623459016974dD9b97F35369e7D`](https://explorer-studio.genlayer.com/address/0x034E9Eee99952623459016974dD9b97F35369e7D). Live route `LIVE-1789762048` finalized `plan`, `begin`, and all three ordered checkpoint transactions, reaching `COMPLETED`. The five hashes and deployed-source digest are recorded in `deployment.json`; the public line is [warnedwarn.github.io/migration-baton](https://warnedwarn.github.io/migration-baton/).
