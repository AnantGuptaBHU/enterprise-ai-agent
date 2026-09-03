from dotenv import load_dotenv

from google import genai
from google.genai import types


load_dotenv()


class LLMResponse:

    def __init__(
        self,
        text=None,
        tool_calls=None,
        message=None,
    ):
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

    def generate(self, prompt: str) -> LLMResponse:
        # response = self.chat.send_message(prompt)
        # tool_calls = response.function_calls or []
        # return LLMResponse(
        #     text=response.text,
        #     tool_calls=tool_calls,
        #     message=response.candidates[0].content,
        # )
        return LLMResponse(
            tool_calls=[
                types.FunctionCall(
                    name="unknown_tool",
                    args={
                        "a": 6,
                        "b": 7,
                        "operation": "add",
                    },
                )
            ]
        )

    def send_tool_results(self, tool_calls, results):

        # function_responses = []

        # for function_call, result in zip(tool_calls, results):

        #     function_responses.append(
        #         types.Part.from_function_response(
        #             name=function_call.name,
        #             response={
        #                 "result": result
        #             },
        #         )
        #     )

        # response = self.chat.send_message(
        #     function_responses
        # )

        # return self._normalize_response(response)
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