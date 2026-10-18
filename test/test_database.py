import database
from models import TicketInfo
import pytest

def test_initialize_database(tmp_path, monkeypatch):
    test_db = tmp_path / "test_tickets.db"
    monkeypatch.setattr(database, "TICKETS_DATABASE", str(test_db))
    
    database.initialize_database()
    
    connection = database.get_connection()
    cursor = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='tickets'"
    )
    
    result = cursor.fetchone()
    connection.close()
    
    assert result == ("tickets",)
    
def test_create_ticket(tmp_path, monkeypatch):
    test_db = tmp_path / "test_tickets.db"
    monkeypatch.setattr(database, "TICKETS_DATABASE", str(test_db))
    
    database.initialize_database()
    
    ticket_input = TicketInfo(employee_id=1000001, category="Network", description="This is a database test")
    
    ticket = database.create_ticket(ticket_input)
    created_ticket = database.return_ticket_by_id(ticket_id=ticket.ticket_id)
    assert created_ticket is not None
    assert created_ticket.description == "This is a database test"
    assert created_ticket.employee_id == 1000001
    
def test_return_all_tickets(tmp_path, monkeypatch):
    test_db = tmp_path / "test_tickets.db"
    monkeypatch.setattr(database, "TICKETS_DATABASE", str(test_db))
    
    database.initialize_database()
    
    ticket_1 = TicketInfo(employee_id=1000001, category="VPN", description="Return all tickets test employee 1000001")
    ticket_2 = TicketInfo(employee_id=1000002, category="Network", description="Return all tickets test employee 1000002")
    tickets_info_list = [ticket_1, ticket_2]
    
    for ticket in tickets_info_list:
        database.create_ticket(ticket)
        
    tickets_list = database.return_all_tickets()
    
    employee_ids = {ticket.employee_id for ticket in tickets_list}
    
    assert len(tickets_list) == 2
    assert employee_ids == {1000001, 1000002}
    
def test_update_ticket_status(tmp_path, monkeypatch):
    test_db = tmp_path / "test_tickets.db"
    monkeypatch.setattr(database, "TICKETS_DATABASE", str(test_db))
    
    database.initialize_database()
    
    ticket_info = TicketInfo(employee_id=1000001, category="Network", description="This a update status test")
    ticket = database.create_ticket(ticket_info)
    created_ticket = database.return_ticket_by_id(ticket_id=ticket.ticket_id)
    assert created_ticket is not None
    assert created_ticket.employee_id == 1000001
    assert created_ticket.status == "Open"
    
    database.update_ticket_status(ticket.ticket_id, "In progress")
    
    updated_ticket = database.return_ticket_by_id(ticket_id=ticket.ticket_id)
    
    assert updated_ticket is not None
    assert updated_ticket.employee_id == 1000001
    assert updated_ticket.status == "In progress"
    
def test_update_nonexistent_ticket(tmp_path, monkeypatch):
    test_db = tmp_path / "test_tickets.db"
    monkeypatch.setattr(database, "TICKETS_DATABASE", str(test_db))
    
    database.initialize_database()
    
    updated_ticket = database.update_ticket_status(9999, "Resolved")
    assert updated_ticket is None
    
def test_return_nonexistent_ticket_by_id(tmp_path, monkeypatch):
    test_db = tmp_path / "test_tickets.db"
    monkeypatch.setattr(database, "TICKETS_DATABASE", str(test_db))
    
    database.initialize_database()
    
    ticket = database.return_ticket_by_id(ticket_id=9999)
    
    assert ticket is None
    
    
    
    
    
    
    
    
    
    
    

    
    