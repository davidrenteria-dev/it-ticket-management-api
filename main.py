from fastapi import FastAPI, HTTPException
from database import return_ticket_by_id, return_all_tickets, update_ticket_status

from database import create_ticket
from models import TicketInfo, Ticket, TicketStatusUpdate

app = FastAPI()

@app.get("/")
def get_message():
    message = {"message": "IT Ticket Management API"}
    return message

@app.post("/tikets")
def submit_ticket(ticketinfo: TicketInfo):
    create_ticket(ticketinfo)

@app.get("/tickets", response_model=list[Ticket])
def get_all_tickets():
    tickets = return_all_tickets()
    return tickets

@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_tickt(ticket_id: int):
    ticket = return_ticket_by_id(ticket_id)
    if ticket is None:
        http_exception = HTTPException(status_code=404, 
                                       detail=f"Ticket with ID {ticket_id} not found")
        raise http_exception
    return ticket

@app.patch("/tickets/{ticket_id}", response_model=Ticket)
def update_status(ticket_id: int, new_status: TicketStatusUpdate):
    ticket = update_ticket_status(ticket_id=ticket_id, new_status=new_status.status)
    if ticket == None:
        raise HTTPException(status_code=404, detail=f"Ticket ID {ticket_id} was not found")
    return ticket
