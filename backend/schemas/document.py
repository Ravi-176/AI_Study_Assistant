from pydantic import BaseModel
from datetime import datetime
class DocumentCreate(BaseModel):
    file_name:str
    file_path:str
class DocumentResponse(BaseModel):
    id:int
    user_id:int
    file_name:str
    file_path:str
    uploaded_at:datetime
    processing_status:str
    class Config:
        from_attributes=True    