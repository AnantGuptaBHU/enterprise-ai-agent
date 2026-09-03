from app.agent.executor import ToolExecutor
from app.llm.client import LLMClient
from app.agent.models import AgentState
from app.agent.models import AgentState, AgentResult
from app.agent.message_store import MessageStore
from app.models import Role

class AgentLoop:

    def __init__(self,llm_client: LLMClient,tool_executor: ToolExecutor, message_store: MessageStore,max_iterations = 10):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.message_store = message_store
        self.max_iterations = max_iterations

    def run(self, user_input: str, conversation_id: int):
        state = AgentState(user_input=user_input)

        try:
            response = self.llm_client.generate(user_input)
            state.iteration = 0
            tool_history = set()

            while response.is_tool_call:
                state.iteration += 1

                if state.iteration > self.max_iterations:
                    raise RuntimeError(
                        "Agent exceeded maximum iterations"
                    )

                print("response -- ", response)

                tool_calls = response.tool_calls
                state.tool_calls.extend(tool_calls)

                results = []

                for function_call in tool_calls:
                    self.message_store.save_message(
                        conversation_id=conversation_id,
                        role=Role.ASSISTANT,
                        tool_call_id=function_call.id,
                        tool_name=function_call.name,
                        tool_arguments=function_call.args,
                    )
                    tool_signature = (
                        function_call.name,
                        str(function_call.args)
                    )

                    if tool_signature in tool_history:
                        raise RuntimeError(
                            f"Agent detected repeated tool call: "
                            f"{function_call.name}"
                        )

                    tool_history.add(tool_signature)

                    print(f"Tool requested: {function_call.name}")
                    print(f"Arguments: {function_call.args}")

                    result = self.tool_executor.execute(function_call)
                    self.message_store.save_message(
                        conversation_id=conversation_id,
                        role=Role.TOOL,
                        content=str(result),
                        tool_call_id=function_call.id,
                        tool_name=function_call.name,
                    )

                    print(f"Tool result: {result}")
                    results.append(result)

                state.tool_results.extend(results)

                response = self.llm_client.send_tool_results(
                    tool_calls,
                    results,
                )

            state.status = "completed"
            return AgentResult(
                success=True,
                output=response.text,
            )

        except Exception as e:

            # print("in failure Exception")
            state.status = "failed"
            state.error = str(e)
            return AgentResult(
                success=False,
                error=str(e),
            )