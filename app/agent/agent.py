from app.agent.executor import ToolExecutor
from app.agent.loop import AgentLoop
from app.llm.client import LLMClient
from app.tools.register import create_tool_registry
from app.agent.message_store import MessageStore

class Agent:
    def __init__(self, message_store: MessageStore, system_prompt = None): 
        self.tool_registry = create_tool_registry() # Create tool registry
        self.llm_client = LLMClient(tools=self.tool_registry.get_definitions(), system_prompt = system_prompt) # Create LLM client
        self.tool_executor = ToolExecutor(self.tool_registry)# Create tool executor
        self.loop = AgentLoop(llm_client=self.llm_client, tool_executor=self.tool_executor,message_store=message_store) # Create execution loop

    def run(self, user_input: str, conversation_id: int):
        return self.loop.run(user_input, conversation_id=conversation_id)