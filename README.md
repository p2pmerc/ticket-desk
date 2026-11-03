# ticket-desk

A minimal support ticket API built with FastAPI. Customers open tickets and follow their own; agents can see and close any ticket.

## Endpoints

| Method | Path | Who |
| --- | --- | --- |
| POST | `/tickets` | any account |
| GET | `/tickets` | customers see their own, agents see all |
| GET | `/tickets/{id}` | a single ticket |
| POST | `/tickets/{id}/close` | owner or agent |

Authenticate with `Authorization: Bearer <token>`. Demo tokens are defined at the top of `main.py`.

## Run

```sh
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt pytest
uvicorn main:app --reload
```

## Tests

```sh
pytest
```
