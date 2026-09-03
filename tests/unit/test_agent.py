from app.agent.agent import Agent


def test_agent_initialization():

    agent = Agent()

    assert agent.tool_registry is not None
    assert agent.llm_client is not None
    assert agent.tool_executor is not None
    assert agent.loop is not None