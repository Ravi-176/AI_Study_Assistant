import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
load_dotenv()
#Establishing the connection
database_url=os.getenv("DATABASE_URL")
engine=create_engine(database_url)
SessionLocal=sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)
Base=declarative_base()