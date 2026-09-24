from fastapi.testclient import TestClient

import pytest
from datetime import date

import models
from main import app, get_db
from test_database import override_get_db, TestSessionLocal

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_get_customers():
    response = client.get("customers")

    assert response.status_code == 200

def test_get_customers_with_id(test_data):
    customer_with_order, _, _ = test_data

    response = client.get(f"/customers/{customer_with_order.id}")
    assert response.status_code == 200

def test_get_customers_who_not_exist():

    response = client.get("/customers/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Kunde nicht gefunden"

def test_create_customer():
    customer_data = {
        "name":"Test",
        "email":"mein@test.com",
        "phone":"111222333",
        "address":"teststrasse. 10"
    }
    response = client.post("/customers", json=customer_data)
    assert response.status_code == 200
    assert response.json()["id"] > 0

def test_update_customer(test_data):
    customer_with_order, _, _ = test_data
    customer_data = {
        "name":"Neuer Name",
        "email":customer_with_order.email,
        "phone":customer_with_order.phone,
        "address":customer_with_order.address
    }
    response = client.put(f"/customers/{customer_with_order.id}", json=customer_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Neuer Name"


def test_delete_customer_with_order(test_data):
    customer_with_order, _, _ = test_data

    response = client.delete(f"/customers/{customer_with_order.id}")

    assert response.status_code == 403
    assert response.json()["detail"] == "Kunde hat noch Orders"

def test_delete_customer_without_order(test_data):
    _, customer_without_order, _ = test_data

    response = client.delete(f"/customers/{customer_without_order.id}")
    assert response.status_code == 200

    response = client.get(f"/customers/{customer_without_order.id}")
    assert response.status_code == 404

def test_delete_order(test_data):
    _, _, order = test_data

    response = client.delete(f"/orders/{order.id}")
    assert response.status_code == 200

    response = client.get(f"/orders/{order.id}")
    assert response.status_code == 404

def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200

def test_get_order(test_data):
    _, _, order = test_data
    response = client.get(f"/orders/{order.id}")
    assert response.status_code == 200

def test_create_order(test_data):
    customer_with_order, _, _ = test_data

    order_data = {
        "title":"Webseite erstellen",
        "description":"ist zum Testen",
        "status":"NEW",
        "priority":"HOCH",
        "due_date":"2030-05-09",
        "customer_id":customer_with_order.id
    }

    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    assert response.json()["customer_id"] == customer_with_order.id

def test_create_order_with_unknown_customer():
    order_data = {
        "title":"Order ohne Customer",
        "description":"ist zum Testen",
        "status":"NEW",
        "priority":"NIEDRIG",
        "due_date":"2030-01-10",
        "customer_id":"666"
    }

    response = client.post("/orders", json=order_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Kunde nicht gefunden"

def test_update_order(test_data):
    _, _, order = test_data

    order_data = {
        "title": "Neuer Titel der Order",
        "description":order.description,
        "status":order.status,
        "priority":order.priority,
        "due_date":"2030-01-01",
        "customer_id":order.customer_id
    }

    response = client.put(f"/orders/{order.id}", json=order_data)
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Neuer Titel der Order"
    assert data["due_date"] == "2030-01-01"

def test_update_order_with_unknown_customer(test_data):
    _, _, order = test_data

    order_data = {
        "title": "Neuer Titel der Order",
        "description":order.description,
        "status":order.status,
        "priority":order.priority,
        "due_date":"2030-01-01",
        "customer_id":"666"
    }

    response = client.put(f"/orders/{order.id}", json=order_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Kunde nicht gefunden"

def test_update_unknown_order():

    order_data = {
        "title": "Order die es nicht gibt",
        "description":"Test",
        "status":"NEW",
        "priority":"NIEDRIG",
        "due_date":"2030-01-01",
        "customer_id":"666"
    }
    response = client.put("/orders/999", json=order_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Order nicht gefunden"

def test_create_order_with_empty_title():
    order_data = {
        "title": "",
        "description":"Test",
        "status":"NEW",
        "priority":"NIEDRIG",
        "due_date":"2030-01-01",
        "customer_id":"666"
    }
    response = client.post("/orders", json=order_data)
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["type"] == "string_too_short"

def test_create_order_with_space_title(test_data):
    _, customer_without_order, _ = test_data

    order_data = {
        "title": "     ",
        "description":"Test",
        "status":"NEW",
        "priority":"NIEDRIG",
        "due_date":"2030-01-01",
        "customer_id":customer_without_order.id
    }
    response = client.post("/orders", json=order_data)
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["type"] == "value_error"

def test_create_order_with_invalid_status(test_data):
    _, customer_without_order, _ = test_data

    order_data = {
        "title": "Falscher Status",
        "description":"Test",
        "status":"HII",
        "priority":"NIEDRIG",
        "due_date":"2030-01-01",
        "customer_id":customer_without_order.id
    }
    response = client.post("/orders", json=order_data)
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"] == ["body", "status"]
    assert data["detail"][0]["type"] == "enum"  

def test_create_order_with_invalid_priority(test_data):
    _, customer_without_order, _ = test_data

    order_data = {
        "title": "Falscher Status",
        "description":"Test",
        "status":"NEW",
        "priority":"EGAL",
        "due_date":"2030-01-01",
        "customer_id":customer_without_order.id
    }
    response = client.post("/orders", json=order_data)
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"] == ["body", "priority"]
    assert data["detail"][0]["type"] == "enum"  


@pytest.fixture
def test_data():
    db = TestSessionLocal()

    customer_with_order = models.Customer(
        name="Kunde mit Order",
        email="order@example.com",
        phone="111111",
        address="Teststraße 1"
    )

    customer_without_order = models.Customer(
        name="Kunde ohne Order",
        email="noorder@example.com",
        phone="222222",
        address="Teststraße 2"
    )

    db.add(customer_with_order)
    db.add(customer_without_order)
    db.commit()

    db.refresh(customer_with_order)
    db.refresh(customer_without_order)

    order = models.Order(
        title="Order von Kunde",
        description="ist zum Testen",
        status="NEW",
        priority="HOCH",
        due_date=date(2027, 10, 20),
        customer_id=customer_with_order.id
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    yield customer_with_order, customer_without_order, order

    # Orders löschen
    orders = db.query(models.Order).filter(
        models.Order.customer_id == customer_with_order.id
    ).all()
    for order in orders:
        db.delete(order)

    # Customer mit Order löschen
    db.delete(customer_with_order)

    # Customer ohne Order löschen
    customer_check = db.query(models.Customer).filter(
        models.Customer.id == customer_without_order.id
    ).first()
    if customer_check:
        db.delete(customer_check)

    db.commit()
    db.close()