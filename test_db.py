from backend.db.models import TicketTable,SessionLocal

db=SessionLocal()
table=TicketTable


def create_ticket():
    new_ticket=table(
        customer_name= 'Yash',
        customer_email ='yash@test.com',
        subject= 'Login Issue',
        description=' Cannot login',
        status= 'open')


    
    return (new_ticket)
    

new_ticket = create_ticket()
db.add(new_ticket)
db.commit()


tickets = db.query(TicketTable).filter(TicketTable.id==5)

for ticket in tickets:
    print(ticket.id)
    print(ticket.ticket_id)
    print(ticket.customer_name)
    print(ticket.customer_email)
    print(ticket.subject)
    print(ticket.description)
    print(ticket.status)


# print(new_ticket)




