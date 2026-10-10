import sqlite3
from datetime import datetime
from models import Ticket, TicketInfo

def initialize_database():
    connection = sqlite3.connect("tickets.db")

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
    created_at = datetime.now().isoformat()
    connection = sqlite3.connect("tickets.db")
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
    
if __name__ == "__main__":
    initialize_database()
    ticket_info = TicketInfo(employee_id=1234567, category="VPN", description="Need access to VPN for remote work.")
    new_ticket = create_ticket(ticket_info)
    print(new_ticket)