from pydantic import BaseModel


class GetTicketInput(BaseModel):
    ticket_id: str


class CreateTicketInput(BaseModel):
    customer_id: str
    title: str
    description: str
    priority: str


def get_ticket(ticket_id: str):

    return {
        "ticket_id": ticket_id,
        "status": "open",
        "priority": "high",
        "assigned_to": "support-team",
        "message": "Ticket is currently being investigated."
    }


def create_support_ticket(
    customer_id: str,
    title: str,
    description: str,
    priority: str
):

    return {
        "ticket_id": "INC-1001",
        "customer_id": customer_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "created"
    }