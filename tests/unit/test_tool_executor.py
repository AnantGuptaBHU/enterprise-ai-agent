import pytest
from pydantic import BaseModel

from app.agent.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.tools.tool import Tool


class CalculatorInput(BaseModel):
    a: int
    b: int


def add(a: int, b: int):
    return a + b


@pytest.fixture
def executor():
    registry = ToolRegistry()

    registry.register(
        Tool(
            name="add",
            description="Add two numbers",
            function=add,
            input_schema=CalculatorInput,
        )
    )

    return ToolExecutor(registry)


def test_execute_tool(executor):
    class FunctionCall:
        name = "add"
        args = {"a": 2, "b": 3}

    result = executor.execute(FunctionCall())

    assert result == 5


def test_unknown_tool(executor):
    class FunctionCall:
        name = "unknown"
        args = {}

    with pytest.raises(ValueError, match="Unknown tool"):
        executor.execute(FunctionCall())


def test_invalid_tool_arguments(executor):
    class FunctionCall:
        name = "add"
        args = {"a": "invalid", "b": 3}

    with pytest.raises(Exception):
        executor.execute(FunctionCall())