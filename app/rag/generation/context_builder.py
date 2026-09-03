class ContextBuilder:

    def build(self, results: list[dict]) -> str:
        if not results:
            return ""

        context_parts = []

        for index, result in enumerate(results, start=1):
            context_parts.append(
                f"[Context {index}]\n"
                f"{result['content']}"
            )

        return "\n\n".join(context_parts)