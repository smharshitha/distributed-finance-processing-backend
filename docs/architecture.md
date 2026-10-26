# Architecture notes

## Suggested service boundaries
- API / authentication: validates caller identity and request shape.
- Transaction service: owns transaction state and idempotency.
- Ledger service: appends balanced debit/credit entries atomically.
- Event publisher: publishes committed events using a transactional outbox.
- Reconciliation worker: compares internal ledger with external statements.

## Invariants
1. Every posted transfer has equal total debits and credits.
2. A request with the same idempotency key and same payload does not post twice.
3. Reusing a key with a different payload returns a conflict.
4. State changes are recorded with timestamps and actor/service identity.
5. Database constraints backstop application-level validation.

The in-memory starter does not implement these production guarantees; add PostgreSQL schema, migrations, integration tests, and fault-injection tests before describing them as implemented.
