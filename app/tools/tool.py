from typing import Callable
from google.genai import types
from pydantic import BaseModel

class Tool:
    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        input_schema: type[BaseModel],
    ):
        self.name = name
        self.description = description
        self.function = function
        self.input_schema = input_schema

    def to_gemini_function(self):
        schema = self.input_schema.model_json_schema()
        return types.FunctionDeclaration(
            name=self.name,
            description=self.description,
            parameters_json_schema=schema,
        )