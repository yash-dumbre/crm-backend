# CRM Backend (FastAPI + SQLite)

This is a backend API for a CRM system built using FastAPI, SQLAlchemy, and SQLite database.

---

##  Features

- Create Ticket
- Get All Tickets
- Get Ticket Details
- Update Ticket (PUT)
- Add Notes to Ticket
- SQLite database (file-based)

---

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

---

##  Installation

```bash
pip install -r requirements.txt

```run command
uvicorn main:app --reload

```Endpoints

POST /tickets
GET /tickets
GET /tickets/{ticket_id}
PUT /tickets/{ticket_id}
PUT /tickets/{ticket_id}