from sqlalchemy import create_engine  # type:ignore
from sqlalchemy.orm import sessionmaker, DeclarativeBase  # type:ignore
import os
import logging
from dotenv import load_dotenv  # type:ignore

load_dotenv()

logger = logging.getLogger(__name__)

# Read individual variables from .env
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# Validate all required variables are present
if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB]):
    raise ValueError("POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB must be set in .env")

# Build the connection URL from the individual parts
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL, echo=False)
logger.info("Database engine created successfully.")

session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = session()
    logger.debug("Database session opened.")
    try:
        yield db
    except Exception as e:
        logger.error(f"Session error, rolling back: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        logger.debug("Database session closed.")