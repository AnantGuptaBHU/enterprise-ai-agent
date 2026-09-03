class ContextBuilder:

    def build(self, results: list[dict], max_chars: int = 600) -> str:
        if not results:
            return ""

        context_parts = []
        current_size = 0
        for index, result in enumerate(results, start=1):
            context = (
                f"[Context {index}]\n"
                f"{result['content']}"
            )
            if current_size + len(context) > max_chars:
                break

            context_parts.append(context)
            current_size += len(context) + 2  # "\n\n"

        return "\n\n".join(context_parts)