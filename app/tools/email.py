from pydantic import BaseModel


class SendEmailInput(BaseModel):
    recipient: str
    subject: str
    body: str


def send_email(
    recipient: str,
    subject: str,
    body: str
):

    return {
        "status": "sent",
        "recipient": recipient,
        "subject": subject,
        "message": "Email sent successfully."
    }