# Auftragsverwaltung

# Backend-Struktur
    Frontend (kommt noch)
       │
       │ HTTP / REST
       ▼
    ┌──────────────────┐
    │     FastAPI      │  ← API-Endpunkte
    ├──────────────────┤
    │      Pydantic    │  ← Validierung
    ├──────────────────┤
    │    SQLAlchemy    │  ← Datenbankzugriff
    ├──────────────────┤
    │      SQLite      │  ← Datenbank
    └──────────────────┘

## REST-API

| Methode  | Endpoint          | Beschreibung                   | Tests                                                                                                                                                                                                                                    |
| -------- | ----------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GET`    | `/customers`      | Alle Kunden abrufen            | `test_get_customers`                                                                                                                                                                                                                     |
| `GET`    | `/customers/{id}` | Einen einzelnen Kunden abrufen | `test_get_customers_with_id`<br>`test_get_customers_who_not_exist`                                                                                                                                                                                                                                      |
| `POST`   | `/customers`      | Einen neuen Kunden erstellen   | `test_create_customer`                                                                                                                                                                                                                                        |
| `PUT`    | `/customers/{id}` | Einen Kunden ändern            | `test_update_customer`                                                                                                                                                                                                                                        |
| `DELETE` | `/customers/{id}` | Einen Kunden löschen           | `test_delete_customer_with_order`<br>`test_delete_customer_without_order`                                                                                                                                                                |
| `GET`    | `/orders`         | Alle Orders abrufen            | `test_get_orders`                                                                                                                                                                                                                                        |
| `GET`    | `/orders/{id}`    | Eine einzelne Order abrufen    | `test_get_order`                                                                                                                                                                                                                                        |
| `POST`   | `/orders`         | Eine neue Order erstellen      | `test_create_order`<br>`test_create_order_with_unknown_customer`<br>`test_create_order_with_empty_title`<br>`test_create_order_with_space_title`<br>`test_create_order_with_invalid_status`<br>`test_create_order_with_invalid_priority` |
| `PUT`    | `/orders/{id}`    | Eine Order ändern              | `test_update_order`<br>`test_update_order_with_unknown_customer`<br>`test_update_unknown_order`                                                                                                                                          |
| `DELETE` | `/orders/{id}`    | Eine Order löschen             | `test_delete_order`                                                                                                                                                                                                                      |


# Pytest
    yield gibt die Testdaten an den Test zurück. Sobald der Test beendet ist, wird der Code nach yield als Teardown ausgeführt.

    test_data-Fixture:
    Setup
    ↓
    Customer mit Order erstellen
    ↓
    Customer ohne Order erstellen
    ↓
    Order erstellen
    ↓
    Test ausführen
    ↓
    Teardown
    ↓
    alle Orders des Kunden löschen
    ↓
    Kunden löschen

# Pydantic
    schemas.py

# SQLAlchemy
    models.py

    Customer
    │
    ├── Order
    ├── Order
    └── Order

    Ein Kunde kann viele Orders haben, aber eine Order gehört nur zu einem Kunden.