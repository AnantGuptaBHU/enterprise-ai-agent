from pydantic import BaseModel


class CustomerInput(BaseModel):
    customer_id: str


def get_customer(customer_id: str):

    return {
        "customer_id": customer_id,
        "name": "Rahul Sharma",
        "email": "rahul@example.com",
        "status": "active",
        "plan": "enterprise"
    }