from fastapi import FastAPI,Depends,HTTPException
from database import engine,Base,SessionLocal
from models.user import User
from schemas.user import UserCreate,UserResponse,UserUpdate,MessageResponse
from sqlalchemy.orm import Session
app=FastAPI()
Base.metadata.create_all(bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close() 
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
    
    