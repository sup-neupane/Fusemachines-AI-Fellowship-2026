from fastapi import FastAPI  #type:ignore
from app.router import router
from app.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Customer API",
    description="A layered FastAPI application for managing customer data.",
    version="1.0.0",
)

# Register the customers router with the main application
app.include_router(router)

logger.info("Customer API application started.")


@app.get("/health", tags=["Health"])
def health_check():
    """
    Simple endpoint to verify the API is running.
    Returns 200 OK with a status message.
    """
    logger.info("Health check requested.")
    return {"status": "ok", "message": "Customer API is running."}