from sqlalchemy.orm import Session  #type:ignore
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date, Text  #type:ignore
from sqlalchemy.orm import relationship   #type:ignore
from app.database import Base
from app.schemas import CustomerCreate, CustomerUpdate
from app.logger import get_logger

logger = get_logger(__name__)

class Payment(Base):
    __tablename__ = "payments" 
    customerNumber = Column(
        Integer, ForeignKey("customers.customerNumber"), primary_key = True
    )
    checkNumber = Column(String, primary_key = True)
    paymentDate = Column(Date, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

class Order(Base):
    __tablename__ = "orders"

    orderNumber = Column(Integer, primary_key=True, index=True)
    orderDate = Column(Date, nullable=False)
    requiredDate = Column(Date, nullable=False)
    shippedDate = Column(Date, nullable=True)
    status = Column(String(15), nullable=False)
    comments = Column(Text, nullable=True)
    customerNumber = Column(
        Integer, ForeignKey("customers.customerNumber"), nullable=False
    )


class Customer(Base):
    __tablename__ = "customers"

    customerNumber = Column(Integer, primary_key=True, index=True)
    customerName = Column(String(50), nullable=False)
    contactLastName = Column(String(50), nullable=False)
    contactFirstName = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    addressLine1 = Column(String(50), nullable=False)
    addressLine2 = Column(String(50), nullable=True)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=True)
    postalCode = Column(String(15), nullable=True)
    country = Column(String(50), nullable=False)
    salesRepEmployeeNumber = Column(
        Integer, ForeignKey("employees.employeeNumber"), nullable=True
    )
    creditLimit = Column(Numeric(10, 2), nullable=True)

    orders = relationship("Order", backref="customer", lazy="select")
    payments = relationship("Payment", backref="customer", lazy="select")

# CRUD Functions

def get_customers(db: Session, skip: int = 0, limit: int = 10) -> list[Customer]:
    logger.info(f"Fetching customers - skip = {skip} , limit = {limit}")
    customers = db.query(Customer).offset(skip).limit(limit).all()
    logger.info(f"Returned {len(customers)} records")
    return customers

def get_customer_by_number(db: Session, customer_number: int) -> Customer | None:
    logger.info(f"Looking up customer: {customer_number}")
    customer = (
        db.query(Customer)
        .filter(Customer.customerNumber == customer_number)
        .first()
    )
    if customer is None:
        logger.warning(f"Customer not found: {customer_number}")
    else:
        logger.info(f"Customer found: {customer.customerName}")
    return customer


def create_customer(db: Session, customer_data: CustomerCreate) -> Customer:
    logger.info(f"Creating customer: {customer_data.customerName}")

    new_customer = Customer(**customer_data.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)  # Reload from DB to get any DB-generated values

    logger.info(f"Customer created successfully: #{new_customer.customerNumber}")
    return new_customer


def update_customer(
    db: Session, customer_number: int, update_data: CustomerUpdate) -> Customer | None:
    logger.info(f"Updating customer: {customer_number}")
    customer = get_customer_by_number(db, customer_number)

    if customer is None:
        return None

    # exclude_none=True means fields not provided by the user are skipped
    changes = update_data.model_dump(exclude_none=True)

    for field, value in changes.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)

    logger.info(f"Customer #{customer_number} updated. Fields changed: {list(changes.keys())}")
    return customer


def delete_customer(db: Session, customer_number: int) -> bool:
    logger.info(f"Attempting to delete customer: {customer_number}")
    customer = get_customer_by_number(db, customer_number)

    if customer is None:
        return False

    db.delete(customer)
    db.commit()

    logger.info(f"Customer #{customer_number} deleted successfully.")
    return True


