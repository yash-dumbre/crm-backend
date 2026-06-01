from sqlalchemy import Column,Text,Integer,DateTime,String,Enum,create_engine,ForeignKey
from enum import Enum as PyEnum
from sqlalchemy.orm import sessionmaker,declarative_base,relationship
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")



engine=create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal=sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base=declarative_base()

class TicketStatus(str,PyEnum):
    OPEN="open"
    IN_PROGRESS="in_progress"
    CLOSED="closed"


class TicketTable(Base):
    __tablename__="TicketsTable"

    id=Column(Integer, primary_key=True,index=True)

    # GENERATE AN STRING ID FOR TICKET_ID USING HYBRID PROPERTY
    # @hybrid_property
    # def ticket_id(self) -> str:
    #     return f"TK-{self.id:03d}" if self.id else None
    
    ticket_id=Column(String,unique=True,index=True, nullable=False)
    customer_name=Column(String(100),nullable=False)
    customer_email=Column(String(100),nullable=False,index=True)
    subject=Column(Text)
    description=Column(Text)
    status=Column(Enum(TicketStatus),default=TicketStatus.OPEN,nullable=False)
    created_at=Column(DateTime(timezone=True) ,server_default=func.now())
    updated_at=Column(DateTime(timezone=True),onupdate=func.now())
    notes = relationship("NotesTable", back_populates="ticket")

class NotesTable(Base):
    __tablename__="NotesTable"
    id=Column(Integer,primary_key=True,index=True)
    ticket_id = Column(Integer, ForeignKey("TicketsTable.id", ondelete="CASCADE"))
    note_text=Column(Text)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    ticket = relationship("TicketTable", back_populates="notes")


Base.metadata.create_all(bind=engine)