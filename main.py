from fastapi import FastAPI

from database import create_ticket
from models import TicketInfo

app = FastAPI()

@app.get("/")
def get_message():
    message = {"message": "IT Ticket Management API"}
    return message

@app.post("/tikets")
def submit_ticket(ticketinfo: TicketInfo):
    create_ticket(ticketinfo)


