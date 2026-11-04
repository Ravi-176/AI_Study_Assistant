import os
import firebase_admin
from firebase_admin import auth,credentials
from fastapi import Depends,HTTPException
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from dotenv import load_dotenv
import logging
load_dotenv()
#Initialize firebase-admin once
try:
    firebase_admin.get_app()
except ValueError:
    service_account_path=os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")  
    if not service_account_path:
        raise RuntimeError("FIREBASE_SERVICE_ACCOUNT_PATH is missing from .env")  
    credential=credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(credential)
security=HTTPBearer()
def get_current_user(
        credentials_data:HTTPAuthorizationCredentials=Depends(security),
):
    try:
        decoded_token=auth.verify_id_token(
            credentials_data.credentials
        )
        return {
            "uid":decoded_token["uid"],
            "email":decoded_token.get("email"),
        }
    except Exception as e:
        logging.exception("Firebase ID token verification failed")
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired ID Token",
            headers={"WWW-Authenticate": "Bearer"},
        )