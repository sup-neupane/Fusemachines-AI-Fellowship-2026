from fastapi import Depends , FastAPI  #type:ignore
from schemas import Product
from database import session , engine
import models
from sqlalchemy.orm import Session #type:ignore

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

products = [
    Product(id = 0 , name = "Pen", description = "2B" , price = 20, quantity = 1),
    Product(id = 1 , name = "Pen", description = "4B" , price = 20, quantity = 2),
    Product(id = 2 , name = "Pen", description = "6B" , price = 20, quantity = 5)
]

def get_db():
    db = session()
    try: 
        yield db
    finally:
        db.close()


def db_init():
    db = session()
    count = db.query(models.Product).count

    if count == 0:
        for product in products:
            db.add(models.Product(**product.model_dump()))
        db.commit()

db_init()

@app.get("/hello")
def hello():
    return "Hello World"


@app.get("/product")
def get_all_products(db :  Session = Depends(get_db)):
    return db.query(models.Product).all()



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