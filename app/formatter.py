"""
Uses LLM to convert structured RAG context into a human-readable answer.
"""

import subprocess


class AnswerFormattingError(Exception):
    pass


class AnswerFormatter:
    """
    Converts validated RAG context into a final chatbot response.
    """

    SYSTEM_PROMPT = """
You are a chatbot answering ONLY from the provided context.

Rules:
- Use ONLY the given context
- Do NOT add new facts
- If context_type is EMPTY, say:
  "Sorry can not find the answer"
"""

    def format(self, context: dict) -> str:
        prompt = f"{self.SYSTEM_PROMPT}\nContext:\n{context}"

        try:
            result = subprocess.run(
                ["ollama", "run", "llama3"],
                input=prompt,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except Exception as e:
            raise AnswerFormattingError(f"Failed to format answer: {e}")
