# Distributed Finance Processing Backend

An educational backend design for processing financial transactions with an auditable ledger, idempotency, validation, and clear service boundaries. The included API is an in-memory demo; it is **not production banking software**.

## Features in the reference demo
- Create a transaction with a client-supplied idempotency key.
- Validate positive amounts and supported currencies.
- Retrieve transaction status.
- Keep a simple in-memory ledger for local experimentation.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000/docs`.

## Design for a production-grade version
- Persist transactions and ledger entries in PostgreSQL using database transactions.
- Enforce a unique constraint on idempotency keys.
- Use an outbox pattern for reliable event publication.
- Model transaction states explicitly and make transitions auditable.
- Add authentication/authorization, structured logs, metrics, tracing, rate limits, secret management, and reconciliation.
- Use integer minor units or Decimal; never binary floating point for money.

## Layout
- `app/main.py` — FastAPI demo endpoints.
- `requirements.txt` — runtime dependency.
- `docs/architecture.md` — production design checklist.

## Important limitations
The demo resets on restart, uses no database, and does not move real money. Do not use it for real financial activity without a security, compliance, reliability, and correctness review.
