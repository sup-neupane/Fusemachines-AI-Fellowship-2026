from pydantic import BaseModel #type:ignore

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int