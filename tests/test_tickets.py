from fastapi.testclient import TestClient

import main

client = TestClient(main.app)
ALICE = {"Authorization": "Bearer tok_alice"}
BOB = {"Authorization": "Bearer tok_bob"}
AGENT = {"Authorization": "Bearer tok_agent"}


def setup_function():
    main.TICKETS.clear()


def test_requires_token():
    assert client.get("/tickets").status_code == 401


def test_customer_lists_only_own_tickets():
    client.post("/tickets", json={"subject": "Refund", "body": "please"}, headers=ALICE)
    client.post("/tickets", json={"subject": "Login", "body": "help"}, headers=BOB)
    assert [t["subject"] for t in client.get("/tickets", headers=ALICE).json()] == ["Refund"]
    assert len(client.get("/tickets", headers=AGENT).json()) == 2


def test_close_is_limited_to_owner():
    tid = client.post("/tickets", json={"subject": "Refund", "body": "please"}, headers=ALICE).json()["id"]
    assert client.post(f"/tickets/{tid}/close", headers=BOB).status_code == 404
    assert client.post(f"/tickets/{tid}/close", headers=ALICE).json()["status"] == "closed"
