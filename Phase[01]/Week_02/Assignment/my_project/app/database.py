from sqlalchemy import create_engine, text #type:ignore
from sqlalchemy.orm import sessionmaker, DeclarativeBase #type:ignore
from dotenv import load_dotenv #type:ignore
import os

from app.logger import get_logger

# Load variables from .env into the environment
load_dotenv()

logger = get_logger(__name__)


def get_database_url() -> str:
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db = os.getenv("POSTGRES_DB")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")

    if not all([user, password, db]):
        logger.error("Missing required database environment variables.")
        raise ValueError(
            "POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB must be set in .env"
        )

    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return url


# --- Engine ---
try:
    DATABASE_URL = get_database_url()
    engine = create_engine(DATABASE_URL, echo=False)
    logger.info("Database engine created successfully.")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# --- Base Class ---
# All your ORM models (table definitions) will inherit from this.
# SQLAlchemy uses it to know which classes represent database tables.
class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    logger.debug("Database session opened.")
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session encountered an error: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        logger.debug("Database session closed.")