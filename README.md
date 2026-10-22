# IT Ticket Management API

A RESTful API developed with Python and FastAPI to manage IT support tickets.

The application allows users to create support tickets, retrieve existing tickets, list all tickets, and update ticket statuses.

Ticket information is stored in a SQLite database, while Pydantic handles request validation and data modeling.

## Tech Stack

- **Python** — Backend programming language
- **FastAPI** — REST API framework
- **Pydantic** — Data validation and modeling
- **SQLite** — Relational database
- **pytest** — Automated testing
- **Git & GitHub** — Version control

## Features

- Create IT support tickets
- Retrieve tickets by ID
- List all existing tickets
- Update ticket statuses
- Validate incoming request data
- Handle invalid requests and nonexistent tickets
- Store tickets persistently in SQLite
- Run automated tests for models, database operations, and API endpoints

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Returns a welcome message |
| POST | `/tickets` | Creates a new IT support ticket |
| GET | `/tickets` | Retrieves all tickets |
| GET | `/tickets/{ticket_id}` | Retrieves a ticket by ID |
| PATCH | `/tickets/{ticket_id}` | Updates the status of an existing ticket |

### Create a Ticket

**Endpoint:** `POST /tickets`

Example request:

```json
{
  "employee_id": 1234567,
  "category": "Network",
  "description": "Unable to connect to the company network."
}
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/davidrenteria-dev/it-ticket-management-api.git
cd it-ticket-management-api
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate the virtual environment.

**Linux / macOS:**

```bash
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 4. Initialize the Database

```bash
python3 database.py
```

This creates the SQLite database and the tickets table if they do not already exist.

### 5. Start the API

```bash
python3 -m uvicorn main:app --reload
```

The API will be available at:

http://127.0.0.1:8000

Interactive API documentation (Swagger UI):

http://127.0.0.1:8000/docs

### 6. Run Automated Tests

```bash
python3 -m pytest -v
```

The automated tests cover data validation, database operations, and API endpoints.