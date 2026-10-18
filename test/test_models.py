from models import TicketStatusUpdate
import pytest

def test_valid_ticket_status():
    ticket = TicketStatusUpdate(status="Open")
    assert ticket.status == "Open"

def test_invalid_ticket_status():
    with pytest.raises(ValueError):
        TicketStatusUpdate(status="Banana")
        
def test_status_whitespaces():
    ticket = TicketStatusUpdate(status="     Resolved     ")
    assert ticket.status == "Resolved"