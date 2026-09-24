import pytest

from schemas import CustomerCreate


def test_customer_name_must_not_be_empty():
    with pytest.raises(ValueError):
        CustomerCreate(
            name=" ",
            email="test@example.com",
            phone="123456",
            address="Teststraße 1"
        )