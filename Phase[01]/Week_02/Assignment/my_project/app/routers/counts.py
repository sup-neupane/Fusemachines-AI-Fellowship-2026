from fastapi import APIRouter, Depends  # type:ignore
from sqlalchemy.orm import Session  # type:ignore
import logging

from app.database import get_db
import app.crud as crud

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Table Counts"])


@router.get("/customers/count")
def get_customer_count(db: Session = Depends(get_db)):
    logger.info("GET /customers/count — request received")
    count = crud.count_customers(db)
    logger.info(f"GET /customers/count — returning {count}")
    return {"table": "customers", "count": count}


@router.get("/orders/count")
def get_order_count(db: Session = Depends(get_db)):
    logger.info("GET /orders/count — request received")
    count = crud.count_orders(db)
    logger.info(f"GET /orders/count — returning {count}")
    return {"table": "orders", "count": count}


@router.get("/products/count")
def get_product_count(db: Session = Depends(get_db)):
    logger.info("GET /products/count — request received")
    count = crud.count_products(db)
    logger.info(f"GET /products/count — returning {count}")
    return {"table": "products", "count": count}


@router.get("/employees/count")
def get_employee_count(db: Session = Depends(get_db)):
    logger.info("GET /employees/count — request received")
    count = crud.count_employees(db)
    logger.info(f"GET /employees/count — returning {count}")
    return {"table": "employees", "count": count}


@router.get("/offices/count")
def get_office_count(db: Session = Depends(get_db)):
    logger.info("GET /offices/count — request received")
    count = crud.count_offices(db)
    logger.info(f"GET /offices/count — returning {count}")
    return {"table": "offices", "count": count}


@router.get("/payments/count")
def get_payment_count(db: Session = Depends(get_db)):
    logger.info("GET /payments/count — request received")
    count = crud.count_payments(db)
    logger.info(f"GET /payments/count — returning {count}")
    return {"table": "payments", "count": count}


@router.get("/orderdetails/count")
def get_orderdetail_count(db: Session = Depends(get_db)):
    logger.info("GET /orderdetails/count — request received")
    count = crud.count_orderdetails(db)
    logger.info(f"GET /orderdetails/count — returning {count}")
    return {"table": "orderdetails", "count": count}


@router.get("/productlines/count")
def get_productline_count(db: Session = Depends(get_db)):
    logger.info("GET /productlines/count — request received")
    count = crud.count_productlines(db)
    logger.info(f"GET /productlines/count — returning {count}")
    return {"table": "productlines", "count": count}