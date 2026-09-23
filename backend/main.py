from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from schemas import CustomerCreate, OrderCreate
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Auftragsverwaltung API läuft"}

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.post("/customers")
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
): 
    new_customer = models.Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer

@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()

    return customers

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Kunde nicht gefunden"
        )

    return customer

@app.put("/customers/{customer_id}")
def put_customer(customer_id: int, customer_data: CustomerCreate, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Kunde nicht gefunden"
            )

    customer.name=customer_data.name
    customer.email=customer_data.email
    customer.phone=customer_data.phone
    customer.address=customer_data.address

    db.commit()
    db.refresh(customer)
        
    return customer

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Kunde nicht gefunden"
        )

    if customer.orders:
        raise HTTPException(
            status_code=403,
            detail="Kunde hat noch Orders"
        )

    db.delete(customer)
    db.commit()

    return customer

@app.post("/orders")
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):

    customer = db.query(models.Customer).filter(
        models.Customer.id == order_data.customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Kunde nicht gefunden"
        )

    new_order = models.Order(
        title=order_data.title,
        description=order_data.description,
        status=order_data.status,
        priority=order_data.priority,
        due_date=order_data.due_date,
        customer_id=customer.id
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()

    return orders

@app.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order nicht gefunden"
        )

    return order

@app.put("/orders/{order_id}")
def put_order(order_id: int, order_data: OrderCreate, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order nicht gefunden"
        )

    customer = db.query(models.Customer).filter(
        models.Customer.id == order_data.customer_id
    ).first()
    
    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Kunde nicht gefunden"
        )
    
    order.title=order_data.title
    order.description=order_data.description
    order.status=order_data.status
    order.priority=order_data.priority
    order.due_date=order_data.due_date
    order.customer_id=customer.id

    db.commit()
    db.refresh(order)
        
    return order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order nicht gefunden"
        )

    db.delete(order)
    db.commit()

    return order
    