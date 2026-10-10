from pydantic import BaseModel, Field, field_validator
from datetime import datetime

ALLOWED_CATEGORIES = {"VPN", "Network", "Tool Access", "Password", "Account", "Hardware", "Software", "Other"}

class TicketInfo(BaseModel):
    employee_id: int = Field(ge=1000000, le=9999999, description="Employee ID must be 7 digits")
    category: str = Field(min_length=3, max_length=50, description="Category of the ticket")
    description: str = Field(min_length=10, max_length=500, description="Description of the ticket")

    @field_validator("description", mode="before")
    def validate_description(cls, value) -> str:
        if not value.strip():
            raise ValueError("Description cannot be empty or whitespace")
        return value.strip()
    
    @field_validator("category", mode="before")
    def validate_category(cls, value) -> str:
        if not value.strip():
            raise ValueError("Category cannot be empty or whitespace")
        if value.strip() not in ALLOWED_CATEGORIES:
            raise ValueError(f"Category must be one of {ALLOWED_CATEGORIES}")
        return value.strip()    
    
    

class Ticket(BaseModel):
    ticket_id: int = Field(gt= 0, description="Unique identifier for the ticket")
    employee_id: int = Field(ge=1000000, le=9999999, description="Employee ID must be 7 digits")
    category: str = Field(min_length=3, max_length=50, description="Category of the ticket")
    description: str = Field(min_length=10, max_length=500, description="Description of the ticket")
    status: str = Field(default="Open", description="Status of the ticket")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp when the ticket was created")
    