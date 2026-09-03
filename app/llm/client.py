from dotenv import load_dotenv

from google import genai
from google.genai import types


load_dotenv()


class LLMResponse:

    def __init__(self,text=None,tool_calls=None,message=None):
        self.text = text
        self.tool_calls = tool_calls or []
        self.message = message

    @property
    def is_tool_call(self):
        return len(self.tool_calls) > 0


class LLMClient:

    def __init__(self, tools=None, system_prompt=None):
        self.client = genai.Client()
        self.chat = self.client.chats.create(
            model = "gemini-3.6-flash",
            config = types.GenerateContentConfig(
                system_instruction = system_prompt,
                tools = [types.Tool(function_declarations = tools)] if tools else None,
                automatic_function_calling = types.AutomaticFunctionCallingConfig(disable = True)
            )
        )
    def _normalize_response(self, response) -> LLMResponse:
        return LLMResponse(
            text=response.text,
            tool_calls=response.function_calls or [],
            message=response.candidates[0].content,
        )

    def generate(self, prompt: str) -> LLMResponse:
        response = self.chat.send_message(prompt)
        print(
            f"[LLMClient] Gemini | "
            f"text={response.text if response.function_calls is None else None} | "
            f"tools={response.function_calls}"
        )

        # return LLMResponse(
        #     text=response.text if not response.function_calls else None,
        #     tool_calls=response.function_calls or [],
        #     message=response.candidates[0].content,
        # )
        return LLMResponse(
            tool_calls=[
                types.FunctionCall(
                    name="search_knowledge_base",
                    args={
                        "query": "What is the warranty period?",
                        "tenant_id": "tenant-001",
                    },
                )
            ]
        )

    def send_tool_results(self, tool_calls, results):
        function_responses = []

        for tool_call, result in zip(tool_calls, results):

            function_responses.append(
                types.Part.from_function_response(
                    name=tool_call.name,
                    response={
                        "result": result
                    },
                )
            )

        response = self.chat.send_message(function_responses)

        print(
            f"[LLMClient] Gemini after tool | "
            f"text={response.text if response.function_calls is None else None} | "
            f"tools={response.function_calls}"
        )

        # return LLMResponse(
        #     text=response.text if not response.function_calls else None,
        #     tool_calls=response.function_calls or [],
        #     message=response.candidates[0].content,
        # )
    
        return LLMResponse(
            text=f"The result is {results[0]}."
        )
        # return LLMResponse(
        #     tool_calls=[
        #         types.FunctionCall(
        #             name="calculator",
        #             args={
        #                 "a": 6,
        #                 "b": 7,
        #                 "operation": "add",
        #             },
        #         )
        #     ]
        # )