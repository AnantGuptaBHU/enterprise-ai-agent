from app.tools.registry import ToolRegistry

class ToolExecutor:
    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry

    def execute(self, tool_call):
        # 1. Find the requested tool
        tool = self.tool_registry.get(tool_call.name)
        if tool is None:
            raise ValueError(
                f"Unknown tool: {tool_call.name}"
            )
        # 2. Validate the arguments
        arguments = tool.input_schema.model_validate(
            tool_call.args
        )
        print(f"Tool requested: {tool}")
        print(f"Arguments: {arguments}")
        # 3. Execute the tool
        result = tool.function(
            **arguments.model_dump()
        )
        return result