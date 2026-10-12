import sqlite3
from datetime import datetime, timezone

from models import Ticket, TicketInfo

TICKETS_DATABASE = "tickets.db"
TEST_DATABASE = "test_tickets.db"

def get_connection():
    return sqlite3.connect(TICKETS_DATABASE)


def initialize_database():
    connection = get_connection()

    print("Database connection established.")

    connection.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id INTEGER PRIMARY KEY,
        employee_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Open',
        created_at TEXT NOT NULL
    )
    ''')

    cursor = connection.execute('SELECT name FROM sqlite_master WHERE type="table"')
    print(cursor.fetchall())

    connection.close()

    print("Database connection closed.")
    
def create_ticket(ticket_info: TicketInfo) -> Ticket:
    created_at = datetime.now(timezone.utc).isoformat()
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute('''
                       INSERT INTO tickets (employee_id, category, description, created_at)
                       VALUES (?, ?, ?, ?)
                       ''', (ticket_info.employee_id, ticket_info.category, 
                             ticket_info.description, created_at)
                        )
    connection.commit()
    ticket_id = cursor.lastrowid
    connection.close()
    
    ticket = Ticket(ticket_id=ticket_id, employee_id=ticket_info.employee_id,
                    category=ticket_info.category, description=ticket_info.description,
                    status="Open", created_at=created_at)
    
    return ticket

def return_ticket_by_id(ticket_id: int) -> Ticket | None:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tickets WHERE ticket_id = ?', (ticket_id,))
    
    row = cursor.fetchone()
    connection.close()
    
    if row is not None:
        ticket = Ticket(ticket_id=row[0], employee_id=row[1], category=row[2],
                        description=row[3], status=row[4], created_at=row[5])
        return ticket
    else:
        return None
    
def return_all_tickets() -> list[Ticket]:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tickets')
    rows = cursor.fetchall()
    connection.close()
    
    tickets = []
    for row in rows:
        ticket = Ticket(ticket_id=row[0], employee_id=row[1], category=row[2],
                        description=row[3], status=row[4], created_at=row[5])
        tickets.append(ticket)
    return tickets

def update_ticket_status(ticket_id: int, new_status: str) -> Ticket | None:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        'UPDATE tickets SET status = ? WHERE ticket_id = ?', 
                   (new_status, ticket_id)                
    )
    affected_rows = cursor.rowcount
    connection.commit()
    
    connection.close()  
    
    if affected_rows == 0:
        return None  # No ticket found with the given ID

    return return_ticket_by_id(ticket_id)
    

    
if __name__ == "__main__":
    initialize_database()
    # ticket_info = TicketInfo(employee_id=1234567, category="VPN", description="Need access to VPN for remote work.")
    # new_ticket = create_ticket(ticket_info)
    # print(new_ticket)
    # ticket = return_ticket_by_id(1)
    # print(ticket.model_dump())
    # print(return_all_tickets())
    print(update_ticket_status(new_status="In progress", ticket_id=99))