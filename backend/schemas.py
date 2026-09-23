from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from enum import Enum

class OrderStatus(str, Enum):
    NEW = "NEW"
    IN_BEARBEITUNG = "IN_BEARBEITUNG"
    ABGESCHLOSSEN = "ABGESCHLOSSEN"

class OrderPriority(str, Enum):
    NIEDRIG = "NIEDRIG"
    MITTEL = "MITTEL"
    HOCH = "HOCH"

class CustomerCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    phone: str = Field(min_length=1)
    address: str = Field(min_length=1)

    @field_validator("name", "phone", "address")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Darf nicht leer sein")

        return value

class OrderCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = None
    status: OrderStatus
    priority: OrderPriority
    due_date: date | None = None
    customer_id: int = Field(ge=1)