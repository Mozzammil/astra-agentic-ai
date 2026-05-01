class SimpleMemory:
    def __init__(self):
        self.history = []

    def add(self, role, content):
        self.history.append({
            "role": role,
            "content": content
        })

    def add_structured(self, data):
        """
        Store only useful structured output
        """
        self.history.append({
            "role": "assistant",
            "content": {
                "summary": data.get("summary"),
                "key_points": data.get("key_points"),
                "insights": data.get("insights")
            }
        })

    def get_context(self):
        context = ""

        # 🔥 only last 3 items (reduce noise)
        for item in self.history[-3:]:
            content = item["content"]

            if isinstance(content, dict):
                # structured memory
                context += f"Assistant Summary: {content.get('summary')}\n"
                context += f"Key Points: {content.get('key_points')}\n"
            else:
                context += f"{item['role']}: {content}\n"

        return context