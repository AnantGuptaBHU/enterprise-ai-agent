from app.tools.tool import Tool


class ToolRegistry:

    def __init__(self):
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self.tools.get(name)

    def get_all(self) -> list[Tool]:
        return list(self.tools.values())

    def get_definitions(self):
        return [
            tool.to_gemini_function()
            for tool in self.tools.values()
        ]