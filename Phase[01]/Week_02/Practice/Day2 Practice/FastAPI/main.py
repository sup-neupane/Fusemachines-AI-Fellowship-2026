from fastapi import FastAPI  #type:ignore
from models import Product

app = FastAPI()

@app.get("/hello")
def hello():
    return "Hello World"


products = [
    Product(id = 1,name = "Phone",description = "Smart Phone", price = 20000 ,quantity=  20)
]

@app.get("/product")
def get_all_products():
    return products


@app.post("/product")
def add_product(product : Product):
    products.append(product)
    return products


@app.put("/product")
def update_product(id: int , product : Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return products[i]
    return "No Product Found"