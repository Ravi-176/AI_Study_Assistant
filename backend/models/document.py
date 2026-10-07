from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Text
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
class Document(Base):
    __tablename__="documents"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    file_name=Column(String,nullable=False)
    file_path=Column(String,nullable=False)
    uploaded_at=Column(DateTime,default=datetime.utcnow)
    processing_status = Column(String,default="uploaded",nullable=False)
    user=relationship("User",back_populates="documents")