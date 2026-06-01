from pydantic import BaseModel,Field,EmailStr
from datetime import datetime
from typing import List
from db.models import TicketStatus


class CreateTicket(BaseModel):
    customer_name:str
    customer_email:EmailStr
    subject:str
    description:str
    class Config:
        from_attributes = True
        use_enum_values = True


class NotesSchema(BaseModel):
    id:int
    # ticket_id : str
    note_text:str
    created_at:datetime
    class Config:
        from_attributes=True


class UpdateTicket(BaseModel):
    status: TicketStatus
    note_text:str |None=None
    class Config:
        from_attributes = True
        use_enum_values = True

class UpdateTicketResponse(BaseModel):
    success: bool
    updated_at: datetime
    class Config:
        from_attributes = True
        use_enum_values = True

class TicketResponse(BaseModel):
    ticket_id:str
    status:TicketStatus
    created_at:datetime
    customer_name:str
    subject:str
    description:str
    
    notes: List[NotesSchema] = Field(default_factory=list)

    class Config:
        from_attributes=True
        use_enum_values = True