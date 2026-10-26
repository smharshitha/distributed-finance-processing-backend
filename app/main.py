"""Minimal in-memory transaction API; educational only."""
from datetime import datetime, timezone
from decimal import Decimal
from threading import Lock
from uuid import uuid4
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Finance Processing Demo", version="0.1.0")
_lock = Lock()
_transactions: dict[str, dict] = {}
_idempotency: dict[str, str] = {}

class TransactionIn(BaseModel):
    source_account: str = Field(min_length=1, max_length=64)
    destination_account: str = Field(min_length=1, max_length=64)
    amount: Decimal
    currency: str = Field(min_length=3, max_length=3)

    @field_validator("amount")
    @classmethod
    def positive_amount(cls, value: Decimal) -> Decimal:
        if not value.is_finite() or value <= 0:
            raise ValueError("amount must be a positive finite decimal")
        return value

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value: str) -> str:
        return value.upper()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/transactions", status_code=201)
def create_transaction(payload: TransactionIn, idempotency_key: str = Header(min_length=8)):
    if payload.source_account == payload.destination_account:
        raise HTTPException(422, "source and destination must differ")
    with _lock:
        if idempotency_key in _idempotency:
            return _transactions[_idempotency[idempotency_key]]
        transaction_id = str(uuid4())
        record = {
            "id": transaction_id, "status": "accepted",
            "source_account": payload.source_account,
            "destination_account": payload.destination_account,
            "amount": str(payload.amount), "currency": payload.currency,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        _transactions[transaction_id] = record
        _idempotency[idempotency_key] = transaction_id
        return record

@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str):
    record = _transactions.get(transaction_id)
    if not record:
        raise HTTPException(404, "transaction not found")
    return record
