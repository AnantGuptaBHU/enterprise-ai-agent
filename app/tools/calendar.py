from pydantic import BaseModel


class CreateCalendarEventInput(BaseModel):
    title: str
    date: str
    time: str
    attendees: list[str]


def create_calendar_event(
    title: str,
    date: str,
    time: str,
    attendees: list[str]
):

    return {
        "event_id": "EVT-1001",
        "title": title,
        "date": date,
        "time": time,
        "attendees": attendees,
        "status": "scheduled"
    }