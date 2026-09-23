from schemas import CustomerCreate

customer = CustomerCreate(
    name=" ",
    email="max@example.com",
    phone="0123456789",
    address="Musterstraße 1, Worms"
)

print(customer)