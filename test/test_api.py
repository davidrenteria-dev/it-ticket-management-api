from main import app
from fastapi.testclient import TestClient
from models import TicketInfo
import database


client = TestClient(app)

def test_get_nonexistent_ticket(test_database):
    response = client.get("/tickets/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket with ID 9999 not found"

def test_get_existent_ticket(test_database):
    ticket_info = TicketInfo(employee_id=1000001, category="VPN", description="This is a test from API")
    ticket = database.create_ticket(ticket_info=ticket_info)

    response = client.get(f"/tickets/{ticket.ticket_id}")

    assert len(database.return_all_tickets()) == 1
    assert response.status_code == 200
    assert response.json()["employee_id"] == 1000001
    assert response.json()["category"] == "VPN"
    assert response.json()["description"] == "This is a test from API"

def test_create_ticket_api(test_database):
    ticket_data = {
        "employee_id": 1000001,
        "category": "VPN",
        "description": "This is a test from API"
    }

    response = client.post("/tickets", json=ticket_data)


    assert response.status_code == 201
    assert response.json()["employee_id"]== 1000001

def test_create_ticket_invalid_fields(test_database):
    ticket_data = {
            "employee_id": 10000001,
            "category": "Internet",
            "description": "Help"
        }

    response = client.post("/tickets", json=ticket_data)

    errors = response.json()["detail"]
    invalid_fields = {error["loc"][1] for error in errors}

    response_get = client.get("/tickets")

    assert response.status_code == 422
    assert response_get.status_code == 200
    assert invalid_fields == {"employee_id", "category", "description"}
    assert response_get.json() == []

def test_get_all_tickets_api(test_database):
    ticket_1 = {
        "employee_id": 1000001,
        "category": "Network",
        "description": "This a test from API"
    }

    ticket_2 = {
        "employee_id": 1000002,
        "category": "Hardware",
        "description": "This a test from API"
    }
    tickets = [ticket_1, ticket_2]

    for ticket in tickets:
        client.post("/tickets", json=ticket)

    response = client.get("/tickets")
    employee_ids = {ticket["employee_id"] for ticket in response.json()}

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert employee_ids == {1000001, 1000002}

def test_update_status(test_database):
    ticket = {
            "employee_id": 1000001,
            "category": "Network",
            "description": "This a test from API"
        }

    response_post = client.post("/tickets", json=ticket)
    ticket_id = response_post.json()["ticket_id"]
    assert response_post.status_code == 201
    assert client.get("/tickets").json()[0]["status"] == "Open"

    response_patch = client.patch(f"/tickets/{ticket_id}", json={"status": "Resolved"})

    assert response_patch.status_code == 200
    assert client.get(f"/tickets/{ticket_id}").json()["status"] == "Resolved"

def test_invalid_status_api(test_database):
    ticket = {
                "employee_id": 1000001,
                "category": "Network",
                "description": "This a test from API"
            }

    response_post = client.post("/tickets", json=ticket)
    ticket_id = response_post.json()["ticket_id"]

    assert response_post.status_code == 201

    response_patch = client.patch(f"/tickets/{ticket_id}", json={"status": "P"})

    assert response_patch.status_code == 422
    assert client.get(f"/tickets/{ticket_id}").json()["status"] == "Open"

def test_update_nonexistent_ticket_api(test_database):
    response = client.patch("/tickets/9999", json={"status": "In progress"})

    assert response.status_code == 404
    assert response.json()["detail"] == 'Ticket with ID 9999 not found'

def test_numeric_description_api(test_database):
    ticket_info = {
        "employee_id": 1000001,
        "category": "Network",
        "description": 12345
    }
    response = client.post("/tickets", json=ticket_info)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Value error, Description must be a string"








