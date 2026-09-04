from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:
    user_input: str
    conversation_id: int | None = None
    iteration: int = 0
    status: str = "running"
    tool_calls: list[Any] = field(default_factory=list)
    tool_results: list[Any] = field(default_factory=list)
    error: str | None = None


@dataclass
class AgentResult:
    success: bool
    output: str | None = None
    error: str | None = None