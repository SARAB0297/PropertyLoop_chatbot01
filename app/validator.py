# app/validator.py

"""
Validates intent and context to enforce RAG safety.
"""

class ValidationError(Exception):
    pass


class Validator:
    """
    Ensures intent and context are valid before answer generation.
    """

    @staticmethod
    def validate_intent(intent: dict) -> None:
        if intent.get("intent") == "UNSUPPORTED":
            raise ValidationError("Unsupported query")

    @staticmethod
    def validate_context(context: dict) -> None:
        if context.get("context_type") == "EMPTY":
            raise ValidationError("Empty context")
