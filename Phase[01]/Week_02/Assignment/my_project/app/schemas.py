from pydantic import BaseModel, field_validator, model_validator #type: ignore
from typing import Optional
from decimal import Decimal
from app.logger import get_logger

logger = get_logger(__name__)


from datetime import date

class PaymentOut(BaseModel):
    checkNumber: str
    paymentDate: date
    amount: Decimal

    model_config = {"from_attributes": True}


from datetime import date

class OrderOut(BaseModel):
    orderNumber: int
    orderDate: date
    status: str
    comments: Optional[str] = None

    model_config = {"from_attributes": True}



class CustomerCreate(BaseModel):
    customerNumber: int
    customerName: str
    contactLastName: str
    contactFirstName: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[Decimal] = None

    @field_validator("customerName")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        """
        Validates that customerName is not an empty string.
        Pydantic calls this automatically before creating the object.
        """
        if not value.strip():
            logger.warning("Validation failed: customerName is empty.")
            raise ValueError("customerName must not be empty or whitespace.")
        return value

    @field_validator("phone")
    @classmethod
    def phone_must_not_be_empty(cls, value: str) -> str:
        """Validates that phone is not blank."""
        if not value.strip():
            logger.warning("Validation failed: phone is empty.")
            raise ValueError("phone must not be empty.")
        return value



class CustomerUpdate(BaseModel):
    customerName: Optional[str] = None
    contactLastName: Optional[str] = None
    contactFirstName: Optional[str] = None
    phone: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[Decimal] = None

    @model_validator(mode="after")
    def at_least_one_field(self) -> "CustomerUpdate":
        """
        Ensures the user sends at least one field to update.
        If everything is None, the update is meaningless.
        """
        values = self.model_dump(exclude_none=True)
        if not values:
            logger.warning("Validation failed: CustomerUpdate has no fields.")
            raise ValueError("At least one field must be provided for update.")
        return self


class CustomerOut(BaseModel):
    customerNumber: int
    customerName: str
    contactLastName: str
    contactFirstName: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[Decimal] = None
    orders: list[OrderOut] = []
    payments: list[PaymentOut] = []

    model_config = {"from_attributes": True}