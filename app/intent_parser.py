
"""
Uses an LLM to convert a user question into a structured intent.
This is the ONLY place where free-form user input is interpreted.
"""

import json
import subprocess
from typing import Dict


class IntentParsingError(Exception):
    pass


class IntentParser:
    """
    Converts natural language questions into structured intent JSON.
    """

    SYSTEM_PROMPT = """
You are an intent classification engine for a RAG system.

Rules:
- Output ONLY valid JSON
- Do NOT explain anything
- Do NOT guess missing information
- Use only these intent families: COUNT, AGGREGATE, COMPARE, UNSUPPORTED

JSON format:
{
  "intent": "...",
  "entity": "fund name or null",
  "metric": "PL_YTD | holdings_count | trades_count | null"
}
"""

    def parse(self, question: str) -> Dict:
        prompt = f"{self.SYSTEM_PROMPT}\nUser Question: {question}"

        try:
            result = subprocess.run(
                ["ollama", "run", "llama3"],
                input=prompt,
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout.strip())
        except Exception as e:
            raise IntentParsingError(f"Failed to parse intent: {e}")
