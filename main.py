"""A small support ticket API. Customers open tickets and read their own; agents see everything."""
from itertools import count

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="ticket-desk")

# API token -> account. A real deployment would load these from a database.
ACCOUNTS = {
    "tok_alice": {"id": 1, "name": "alice", "role": "customer"},
    "tok_bob": {"id": 2, "name": "bob", "role": "customer"},
    "tok_agent": {"id": 100, "name": "support", "role": "agent"},
}

TICKETS: dict[int, dict] = {}
_ids = count(1)


class NewTicket(BaseModel):
    subject: str = Field(min_length=3, max_length=120)
    body: str = Field(min_length=1, max_length=5000)


def current_account(authorization: str = Header(default="")) -> dict:
    token = authorization.removeprefix("Bearer ").strip()
    account = ACCOUNTS.get(token)
    if account is None:
        raise HTTPException(status_code=401, detail="invalid token")
    return account


@app.post("/tickets", status_code=201)
def create_ticket(payload: NewTicket, account: dict = Depends(current_account)):
    ticket = {"id": next(_ids), "owner_id": account["id"], "status": "open", **payload.model_dump()}
    TICKETS[ticket["id"]] = ticket
    return ticket


@app.get("/tickets")
def list_tickets(account: dict = Depends(current_account)):
    if account["role"] == "agent":
        return list(TICKETS.values())
    return [t for t in TICKETS.values() if t["owner_id"] == account["id"]]


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, account: dict = Depends(current_account)):
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="ticket not found")
    return ticket


@app.post("/tickets/{ticket_id}/close")
def close_ticket(ticket_id: int, account: dict = Depends(current_account)):
    ticket = TICKETS.get(ticket_id)
    if ticket is None or (account["role"] != "agent" and ticket["owner_id"] != account["id"]):
        raise HTTPException(status_code=404, detail="ticket not found")
    ticket["status"] = "closed"
    return ticket
