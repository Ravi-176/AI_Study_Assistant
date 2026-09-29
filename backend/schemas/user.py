from pydantic import BaseModel
from datetime import datetime
class UserCreate(BaseModel):
    firebase_uid:str
    name:str
    email:str
class UserResponse(BaseModel):
    id:int
    firebase_uid:str
    name:str
    email:str
    created_at:datetime

    class Config:
        from_attributes=True 
class UserUpdate(BaseModel):
    name:str
    email:str        
class MessageResponse(BaseModel):
    message:str    