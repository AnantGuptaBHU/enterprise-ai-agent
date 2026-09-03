from app.tools.calculator import CalculatorInput, calculator
from app.tools.calendar import CreateCalendarEventInput, create_calendar_event
from app.tools.customer import CustomerInput, get_customer
from app.tools.email import SendEmailInput, send_email
from app.tools.knowledge_base import KnowledgeBaseInput, search_knowledge_base
from app.tools.ticket import CreateTicketInput, GetTicketInput, create_support_ticket, get_ticket
from app.tools.tool import Tool

from app.tools.registry import ToolRegistry
from app.tools.tool import Tool


def create_tool_registry() -> ToolRegistry:

    registry = ToolRegistry()

    calculator_tool = Tool(
        name="calculator",
        description="Perform basic arithmetic operations using two numbers and an operation.",
        function=calculator,
        input_schema=CalculatorInput,
    )
    registry.register(calculator_tool)

    kb_tool = Tool(
        name="search_knowledge_base",
        description= "Search the enterprise knowledge base for information relevant to the user's request.",
        function=search_knowledge_base,
        input_schema=KnowledgeBaseInput,
    )
    registry.register(kb_tool)

    get_customer_tool = Tool(
        name="get_customer",
        description= "Retrieve customer information using a customer ID.",
        function=get_customer,
        input_schema=CustomerInput,
    )
    registry.register(get_customer_tool)
    get_ticket_tool = Tool(
        name="get_ticket",
        description= "Retrieve the current status and details of a support ticket.",
        function=get_ticket,
        input_schema=GetTicketInput,
    )
    registry.register(get_ticket_tool)

    create_support_ticket_tool = Tool(
            name="create_support_ticket",
            description= "Create a new support ticket for a customer.",
            function=create_support_ticket,
            input_schema=CreateTicketInput,
        )
    registry.register(create_support_ticket_tool)

    send_email_tool = Tool(
        name="send_email",
        description= "Send an email to a specified recipient.",
        function=send_email,
        input_schema=SendEmailInput,
            )
    registry.register(send_email_tool)

    calendar_event_tool = Tool(
            name="create_calendar_event",
            description= "Create a calendar event with attendees.",
            function=create_calendar_event,
            input_schema=CreateCalendarEventInput,
        )
    registry.register(calendar_event_tool)

    return registry
