from dotenv import load_dotenv  # type:ignore
load_dotenv()

from fastapi import FastAPI  # type:ignore
import logging

from app.logger import setup_logging
from app.database import engine, Base
from app.routers import customers, counts, dashboard

import app.crud  # noqa: F401

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Customer API",
    description="Layered FastAPI application with concurrent dashboard.",
    version="2.0.0"
)


Base.metadata.create_all(bind=engine)

app.include_router(customers.router)
app.include_router(counts.router)
app.include_router(dashboard.router)

logger.info("Customer API started successfully.")


@app.get("/health", tags=["Health"])
def health_check():
    logger.info("Health check called.")
    return {"status": "ok", "message": "Customer API is running."}