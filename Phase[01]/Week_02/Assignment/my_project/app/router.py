from fastapi import APIRouter, Depends, HTTPException, Query  #type:ignore
from sqlalchemy.orm import Session  #type:ignore

from app.database import get_db
from app.schemas import CustomerCreate, CustomerOut, CustomerUpdate
from app import crud
from app.logger import get_logger

logger = get_logger(__name__)

# APIRouter groups related endpoints together.
# prefix means all routes here start with /customers
# tags groups them in the Swagger UI docs
router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/", response_model=list[CustomerOut])
def list_customers(
    skip: int = Query(default=0, ge=0, description="Records to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    logger.info(f"GET /customers — skip={skip}, limit={limit}")
    customers = crud.get_customers(db, skip=skip, limit=limit)
    logger.info(f"Returning {len(customers)} customers.")
    return customers


@router.get("/{customer_number}", response_model=CustomerOut)
def get_customer(customer_number: int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customer_number}")
    customer = crud.get_customer_by_number(db, customer_number)

    if customer is None:
        logger.warning(f"404 — Customer not found: {customer_number}")
        raise HTTPException(
            status_code=404,
            detail=f"Customer with number {customer_number} not found."
        )

    logger.info(f"Returning customer: {customer.customerName}")
    return customer


@router.post("/", response_model=CustomerOut, status_code=201)
def create_customer(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    logger.info(f"POST /customers — creating: {customer_data.customerName}")

    # Check if customer number already exists
    existing = crud.get_customer_by_number(db, customer_data.customerNumber)
    if existing:
        logger.warning(f"Conflict: Customer #{customer_data.customerNumber} already exists.")
        raise HTTPException(
            status_code=409,
            detail=f"Customer with number {customer_data.customerNumber} already exists."
        )

    new_customer = crud.create_customer(db, customer_data)
    logger.info(f"Created customer #{new_customer.customerNumber}")
    return new_customer


@router.patch("/{customer_number}", response_model=CustomerOut)
def update_customer(
    customer_number: int,
    update_data: CustomerUpdate,
    db: Session = Depends(get_db),
):
    logger.info(f"PATCH /customers/{customer_number}")
    updated = crud.update_customer(db, customer_number, update_data)

    if updated is None:
        logger.warning(f"404 — Cannot update, customer not found: {customer_number}")
        raise HTTPException(
            status_code=404,
            detail=f"Customer with number {customer_number} not found."
        )

    logger.info(f"Customer #{customer_number} updated successfully.")
    return updated


@router.delete("/{customer_number}", status_code=204)
def delete_customer(customer_number: int, db: Session = Depends(get_db)):
    logger.info(f"DELETE /customers/{customer_number}")
    success = crud.delete_customer(db, customer_number)

    if not success:
        logger.warning(f"404 — Cannot delete, customer not found: {customer_number}")
        raise HTTPException(
            status_code=404,
            detail=f"Customer with number {customer_number} not found."
        )

    logger.info(f"Customer #{customer_number} deleted.")