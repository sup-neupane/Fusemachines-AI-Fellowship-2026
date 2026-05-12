from sqlalchemy.orm import Session  # type:ignore
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date, Text  # type:ignore
from sqlalchemy.orm import relationship  # type:ignore
from app.database import Base
from app.schemas import CustomerCreate, CustomerUpdate
from app.logger import get_logger
import logging

logger = logging.getLogger(__name__)


# ── ORM Models (Table Definitions) ─────────────────────────────────────────

class ProductLine(Base):
    __tablename__ = "productlines"

    productLine = Column(String(50), primary_key=True)
    textDescription = Column(String(4000), nullable=True)
    htmlDescription = Column(Text, nullable=True)
    image = Column(Text, nullable=True)


class Product(Base):
    __tablename__ = "products"

    productCode = Column(String(15), primary_key=True)
    productName = Column(String(70), nullable=False)
    productLine = Column(String(50), ForeignKey("productlines.productLine"), nullable=False)
    productScale = Column(String(10), nullable=False)
    productVendor = Column(String(50), nullable=False)
    productDescription = Column(Text, nullable=False)
    quantityInStock = Column(Integer, nullable=False)
    buyPrice = Column(Numeric(10, 2), nullable=False)
    MSRP = Column(Numeric(10, 2), nullable=False)


class Office(Base):
    __tablename__ = "offices"

    officeCode = Column(String(10), primary_key=True)
    city = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    addressLine1 = Column(String(50), nullable=False)
    addressLine2 = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    country = Column(String(50), nullable=False)
    postalCode = Column(String(15), nullable=False)
    territory = Column(String(10), nullable=False)


class Employee(Base):
    __tablename__ = "employees"

    employeeNumber = Column(Integer, primary_key=True)
    lastName = Column(String(50), nullable=False)
    firstName = Column(String(50), nullable=False)
    extension = Column(String(10), nullable=False)
    email = Column(String(100), nullable=False)
    officeCode = Column(String(10), ForeignKey("offices.officeCode"), nullable=False)
    reportsTo = Column(Integer, ForeignKey("employees.employeeNumber"), nullable=True)
    jobTitle = Column(String(50), nullable=False)


class Payment(Base):
    __tablename__ = "payments"

    customerNumber = Column(
        Integer, ForeignKey("customers.customerNumber"), primary_key=True
    )
    checkNumber = Column(String(50), primary_key=True)
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


class OrderDetail(Base):
    __tablename__ = "orderdetails"

    orderNumber = Column(Integer, ForeignKey("orders.orderNumber"), primary_key=True)
    productCode = Column(String(15), ForeignKey("products.productCode"), primary_key=True)
    quantityOrdered = Column(Integer, nullable=False)
    priceEach = Column(Numeric(10, 2), nullable=False)
    orderLineNumber = Column(Integer, nullable=False)


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
    salesRepEmployeeNumber = Column(Integer, nullable=True)
    creditLimit = Column(Numeric(10, 2), nullable=True)

    orders = relationship("Order", backref="customer", lazy="select")
    payments = relationship("Payment", backref="customer", lazy="select")


# ── Customer CRUD ───────────────────────────────────────────────────────────

def get_customers(db: Session, skip: int = 0, limit: int = 10) -> list[Customer]:
    logger.info(f"Fetching customers - skip={skip}, limit={limit}")
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
    db.refresh(new_customer)
    logger.info(f"Customer created successfully: #{new_customer.customerNumber}")
    return new_customer


def update_customer(
    db: Session, customer_number: int, update_data: CustomerUpdate
) -> Customer | None:
    logger.info(f"Updating customer: {customer_number}")
    customer = get_customer_by_number(db, customer_number)
    if customer is None:
        return None
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


# ── Count Functions ─────────────────────────────────────────────────────────

def count_customers(db: Session) -> int:
    logger.info("Querying count: customers")
    count = db.query(Customer).count()   # ← fixed: was missing ()
    logger.info(f"Count result — customers: {count}")
    return count


def count_orders(db: Session) -> int:
    logger.info("Querying count: orders")
    count = db.query(Order).count()
    logger.info(f"Count result — orders: {count}")
    return count


def count_products(db: Session) -> int:           
    logger.info("Querying count: products")
    count = db.query(Product).count()
    logger.info(f"Count result — products: {count}")
    return count


def count_employees(db: Session) -> int:
    logger.info("Querying count: employees")
    count = db.query(Employee).count()
    logger.info(f"Count result — employees: {count}")
    return count


def count_offices(db: Session) -> int:
    logger.info("Querying count: offices")
    count = db.query(Office).count()
    logger.info(f"Count result — offices: {count}")
    return count


def count_payments(db: Session) -> int:
    logger.info("Querying count: payments")
    count = db.query(Payment).count()
    logger.info(f"Count result — payments: {count}")
    return count


def count_orderdetails(db: Session) -> int:
    logger.info("Querying count: orderdetails")
    count = db.query(OrderDetail).count()
    logger.info(f"Count result — orderdetails: {count}")
    return count


def count_productlines(db: Session) -> int:
    logger.info("Querying count: productlines")
    count = db.query(ProductLine).count()
    logger.info(f"Count result — productlines: {count}")
    return count