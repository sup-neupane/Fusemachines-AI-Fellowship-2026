from fastapi import APIRouter  # type:ignore
from sqlalchemy.orm import Session  # type:ignore
import asyncio
import time
import logging

from app.database import session
import app.crud as crud

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Dashboard"])


@router.get("/overall_counts")
async def overall_counts():
    logger.info("GET /overall_counts — starting all 8 count queries concurrently")
    start_time = time.perf_counter()

    def run_count(count_func):
        db: Session = session()
        try:
            return count_func(db)
        except Exception as e:
            logger.error(f"Count query failed in thread: {e}")
            return 0
        finally:
            db.close()

    (
        customers,
        orders,
        products,
        employees,
        offices,
        payments,
        orderdetails,
        productlines,
    ) = await asyncio.gather(
        asyncio.to_thread(run_count, crud.count_customers),
        asyncio.to_thread(run_count, crud.count_orders),
        asyncio.to_thread(run_count, crud.count_products),
        asyncio.to_thread(run_count, crud.count_employees),
        asyncio.to_thread(run_count, crud.count_offices),
        asyncio.to_thread(run_count, crud.count_payments),
        asyncio.to_thread(run_count, crud.count_orderdetails),
        asyncio.to_thread(run_count, crud.count_productlines),
    )

    elapsed = round((time.perf_counter() - start_time) * 1000, 2)
    logger.info(f"asyncio.gather() completed — all 8 queries done in {elapsed}ms")

    result = {
        "customers": customers,
        "orders": orders,
        "products": products,
        "employees": employees,
        "offices": offices,
        "payments": payments,
        "orderdetails": orderdetails,
        "productlines": productlines,
    }

    logger.info(f"GET /overall_counts — response: {result}")
    return result