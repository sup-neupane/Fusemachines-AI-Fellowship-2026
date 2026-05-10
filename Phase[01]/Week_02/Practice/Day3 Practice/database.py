from sqlalchemy import create_engine #type:ignore
from sqlalchemy.orm import sessionmaker #type:ignore
import os
from dotenv import load_dotenv #type:ignore

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

if not DATABASE_URL:
    raise ValueError("DB_URL is not set. Check your .env file.")

engine = create_engine(DATABASE_URL, echo=True)  # echo=True logs SQL to console

session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)