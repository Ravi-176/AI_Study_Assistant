from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
def get_or_create_user(
        db:Session,
        firebase_user:dict,
)->User:
    firebase_uid=firebase_user["uid"]
    email=firebase_user.get("email")
    if not email:
        raise HTTPException(
            status_code=400,
            detail="A valid email is required for this account."
        )
    #Looking at the existing firebase user
    user=(
        db.query(User).filter(User.firebase_uid==firebase_uid).first()
        )
    if user:
        return user
    #Do not automatically link accounts just because they have the same 
    #email address
    existing_email=(
        db.query(User).filter(User.email==email).first()
    )
    if existing_email:
        raise HTTPException(
            status_code=409,
            detail="This email already belongs to another application user.",
        )
    #Creating the application user
    name=firebase_user.get("name") or email.split("@")[0]
    user=User(
        firebase_uid=firebase_uid,
        name=name,
        email=email,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user