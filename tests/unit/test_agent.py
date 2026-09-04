from app.agent.agent import Agent

class FakeMessageStore:

    def __init__(self):
        self.messages = []

    def save_message(self, **kwargs):
        self.messages.append(kwargs)
        
def test_agent_initialization():

    agent = Agent( message_store = FakeMessageStore())

    assert agent.tool_registry is not None
    assert agent.llm_client is not None
    assert agent.tool_executor is not None
    assert agent.loop is not None