from fastapi import FastAPI,Depends,HTTPException,UploadFile,File
from database import engine,Base,SessionLocal
from models.user import User
from models.document import Document
from schemas.user import UserCreate,UserResponse,UserUpdate,MessageResponse
from sqlalchemy.orm import Session
from schemas.document import DocumentCreate,DocumentResponse
from services.pdf_service import extract_text_from_pdf
from services.user_service import get_or_create_user
from firebase_auth import get_current_user
import os
import uuid
from pathlib import Path
import logging
app=FastAPI()

Base.metadata.create_all(bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close() 
@app.get("/auth/me")   
def read_current_user(
    current_user:dict=Depends(get_current_user),
    db:Session=Depends(get_db),
):
    user=get_or_create_user(db,current_user)     
    return {
        "id":user.id,
        "uid":user.firebase_uid,
        "name":user.name,
        "email":user.email,
    }
@app.post("/users",response_model=UserResponse)       
def create_user(
                user:UserCreate,
                db:Session=Depends(get_db)
             ):    
    new_user=User(
        firebase_uid=user.firebase_uid,
        name=user.name,
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
        
@app.get("/users",response_model=list[UserResponse])
def get_users(db:Session=Depends(get_db)):
    users=db.query(User).all()
    return users
@app.get("/users/{user_id}",response_model=UserResponse)
def get_user(user_id:int,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==user_id).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
        
    return user
@app.put("/users/{user_id}",response_model=UserResponse)
def update_user(user_id:int,
                user_data:UserUpdate,
                db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==user_id).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    user.name=user_data.name
    user.email=user_data.email
    db.commit()
    db.refresh(user)
    return user
@app.delete("/users/{user_id}",response_model=MessageResponse)
def delete_user(user_id:int,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==user_id).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    db.delete(user)
    db.commit()
    return {
        "message":"User deleted successfully"
    }
@app.post("/documents",response_model=DocumentResponse)    
def create_document(document:DocumentCreate,
                    current_user:dict=Depends(get_current_user),
                    db:Session=Depends(get_db)):
    user=get_or_create_user(db,current_user)
    new_document=Document(
        user_id=user.id,
        file_name=document.file_name,
        file_path=document.file_path
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document
@app.post("/documents/upload",response_model=DocumentResponse)
def upload_document(
                    file:UploadFile=File(...),
                    current_user:dict=Depends(get_current_user),
                    db:Session=Depends(get_db)
                    ):
    #we only accept pdf files for this endpoint
    if not file.filename or Path(file.filename).suffix.lower()!=".pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a file in PDF format"
        )
    #get the owner from the verified firebase identity
    user=get_or_create_user(db,current_user)
    #Give each upload a unique filename to avoid over writing on other files
    os.makedirs("uploads",exist_ok=True)
    safe_filename=Path(file.filename).name
    stored_filename=f"{uuid.uuid4().hex}_{safe_filename}"
    file_path=os.path.join("uploads",stored_filename)
    try:
        with open(file_path,"wb") as buffer:
            buffer.write(file.file.read())
        extracted_text=extract_text_from_pdf(file_path)
        print(extracted_text[:2000])
        new_document=Document(
            user_id=user.id,
            file_name=file.filename,
            file_path=file_path,
            processing_status="processed"
        )   
        db.add(new_document) 
        db.commit()
        db.refresh(new_document)
        return new_document
    except Exception:
        db.rollback()
        if(os.path.exists(file_path)):
            os.remove(file_path)
        logging.exception("PDF upload failed!")    
        raise HTTPException(
            status_code=500,
            detail="PDF could not be processed"
        )   
@app.get("/documents",response_model=list[DocumentResponse])
def get_documents(current_user:dict=Depends(get_current_user),
                  db:Session=Depends(get_db)):
    user=get_or_create_user(db,current_user)
    documents=db.query(Document).filter(Document.user_id==user.id).order_by(Document.uploaded_at.desc()).all()
    return documents

    