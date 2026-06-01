from fastapi import FastAPI ,Depends
from db.models import TicketStatus,TicketTable,SessionLocal,NotesTable
from schemas.ticket import CreateTicket,TicketResponse,UpdateTicket,UpdateTicketResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, cast,String
import re
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Customer CRM System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




def get_db():

    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get('/test')
def get_test():
    return{'message':'CRM Is Working'}



@app.post('/tickets',response_model=TicketResponse) # OUTGOING CONNECTION                                                                                       
def create_ticket(ticket_in:CreateTicket,db:Session = Depends(get_db)):# INCOMING CONNECTION 
    new_ticket=TicketTable(
        customer_name = ticket_in.customer_name,
        customer_email = ticket_in.customer_email,
        subject=ticket_in.subject,
        description=ticket_in.description
    )
    db.add(new_ticket)
    
    db.flush()
    new_ticket.ticket_id = f"TK-{new_ticket.id:03d}"
    db.commit()
    db.refresh(new_ticket)
    return new_ticket


@app.get("/tickets", response_model=list[TicketResponse])
def get_ticket(search: str | None = None,
               status: TicketStatus | None = None,
               db: Session = Depends(get_db)):

    query = db.query(TicketTable)

    if status:
        query = query.filter(TicketTable.status == status)

    


    if search:
        
        is_ticket_id_format = re.match(r'^(tk-)?\d+$', search.strip(), re.IGNORECASE)

        if is_ticket_id_format:
            
            search_clean = search.lower().replace("tk-", "").strip()
            search_numeric = search_clean.lstrip("0") if search_clean.isdigit() else search_clean
            
            query = query.filter(
                or_(
                    TicketTable.ticket_id.contains(search),
                    cast(TicketTable.id, String).contains(search_numeric) if search_numeric else False
                )
            )
        else:
            # --- STANDARD SEARCH LOGIC (Name, Email, Subject, Description) ---
            query = query.filter(
                or_(
                    TicketTable.customer_name.contains(search),
                    TicketTable.customer_email.contains(search),
                    TicketTable.subject.contains(search),
                    TicketTable.description.contains(search),
                )
            )
    tickets = query.all()

    result = []

    for t in tickets:
        result.append({
            "ticket_id": t.ticket_id or f"TK-{t.id:03d}",
            "customer_name": t.customer_name,
            "subject": t.subject,
            "status": t.status,
            "created_at": t.created_at,
            "description": t.description,
            "notes": t.notes
        })

    return result
    

@app.get('/tickets/{ticket_id}',response_model=TicketResponse) # OUTGOING CONNECTION 
def get_ticket_by_id(ticket_id:str, db:Session = Depends(get_db)):
    
    id_num = int(ticket_id.replace("TK-", ""))

    ticket = db.query(TicketTable).filter(TicketTable.id == id_num).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    
    
    return {
        "ticket_id": ticket.ticket_id or f"TK-{ticket.id:03d}",
        "customer_name": ticket.customer_name,
        "subject": ticket.subject,
        "description": ticket.description,
        "status": ticket.status,
        "created_at": ticket.created_at,
        "notes": ticket.notes
    }
      
    
    

@app.put('/tickets/{ticket_id}', response_model=UpdateTicketResponse)
def update_ticketid(
    ticket_id: str,
    data: UpdateTicket,
    db: Session = Depends(get_db)
):

    id_num = int(ticket_id.replace("TK-", ""))

    ticket = db.query(TicketTable).filter(TicketTable.id == id_num).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.status = data.status

    if data.note_text:
        new_note = NotesTable(
            ticket_id=ticket.id,
            note_text=data.note_text
        )
        db.add(new_note)

    db.commit()
    db.refresh(ticket)

    return {
        "success": True,
        "updated_at": ticket.updated_at
    }