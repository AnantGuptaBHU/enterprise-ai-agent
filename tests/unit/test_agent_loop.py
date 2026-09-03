import pytest

from app.agent.loop import AgentLoop
from app.agent.executor import ToolExecutor
from app.llm.client import LLMResponse
from app.tools.registry import ToolRegistry
from app.tools.tool import Tool
from pydantic import BaseModel


class AddInput(BaseModel):
    a: int
    b: int


def add(a: int, b: int):
    return a + b


class FakeLLMClient:

    def __init__(self, responses):
        self.responses = responses
        self.index = 0

    def generate(self, prompt):
        response = self.responses[self.index]
        self.index += 1
        return response

    def send_tool_results(self, tool_calls, results):
        response = self.responses[self.index]
        self.index += 1
        return response


class FakeFunctionCall:

    def __init__(self, name, args):
        self.name = name
        self.args = args


@pytest.fixture
def executor():
    registry = ToolRegistry()

    registry.register(
        Tool(
            name="add",
            description="Add two numbers",
            function=add,
            input_schema=AddInput,
        )
    )

    return ToolExecutor(registry)


def test_agent_loop_tool_execution(executor):

    tool_call = FakeFunctionCall(
        name="add",
        args={"a": 2, "b": 3},
    )

    llm = FakeLLMClient([
        LLMResponse(tool_calls=[tool_call]),
        LLMResponse(text="The answer is 5."),
    ])

    loop = AgentLoop(
        llm_client=llm,
        tool_executor=executor,
    )

    result = loop.run("What is 2 + 3?")

    assert result.success is True
    assert result.output == "The answer is 5."


def test_agent_loop_direct_response(executor):

    llm = FakeLLMClient([
        LLMResponse(text="Hello!")
    ])

    loop = AgentLoop(
        llm_client=llm,
        tool_executor=executor,
    )

    result = loop.run("Hello")

    assert result.success is True
    assert result.output == "Hello!"


def test_agent_loop_unknown_tool(executor):

    tool_call = FakeFunctionCall(
        name="unknown",
        args={},
    )

    llm = FakeLLMClient([
        LLMResponse(tool_calls=[tool_call]),
    ])

    loop = AgentLoop(
        llm_client=llm,
        tool_executor=executor,
    )

    result = loop.run("Do something")

    assert result.success is False
    assert result.error is not None


def test_agent_loop_repeated_tool_call(executor):

    tool_call = FakeFunctionCall(
        name="add",
        args={"a": 2, "b": 3},
    )

    llm = FakeLLMClient([
        LLMResponse(tool_calls=[tool_call]),
        LLMResponse(tool_calls=[tool_call]),
    ])

    loop = AgentLoop(
        llm_client=llm,
        tool_executor=executor,
    )

    result = loop.run("What is 2 + 3?")

    assert result.success is False
    assert "repeated tool call" in result.error.lower()


def test_agent_loop_max_iterations(executor):

    responses = []

    for _ in range(3):
        responses.append(
            LLMResponse(
                tool_calls=[
                    FakeFunctionCall(
                        name="add",
                        args={
                            "a": _,
                            "b": 1,
                        },
                    )
                ]
            )
        )

    llm = FakeLLMClient(responses)

    loop = AgentLoop(
        llm_client=llm,
        tool_executor=executor,
        max_iterations=2,
    )

    result = loop.run("Keep calculating")

    assert result.success is False
    assert "maximum iterations" in result.error.lower()