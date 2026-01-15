"""
Builds structured RAG context from retrieval results.

This module:
- Transforms raw retrieval outputs into LLM-safe context
- Enforces a strict contract between retrieval and generation
- Explicitly handles empty / invalid results
"""

from typing import Dict, Any, Optional


class ContextBuildError(Exception):
    pass


class EmptyContextError(ContextBuildError):
    pass


class RAGContextBuilder:
    """
    Builds validated, structured context for LLM consumption.

    This class is intentionally:
    - Stateless
    - Deterministic
    - Independent of LLM providers
    """

    @staticmethod
    def build_count_context(
        *,
        entity_type: str,
        entity_name: str,
        count: int,
        source: str
    ) -> Dict[str, Any]:
        """
        Build context for COUNT-based queries.
        """
        if count <= 0:
            raise EmptyContextError("Count result is empty.")

        return {
            "context_type": "COUNT",
            "entity_type": entity_type,
            "entity_name": entity_name,
            "result": {
                "count": count
            },
            "data_source": source
        }

    @staticmethod
    def build_aggregate_context(
        *,
        entity_type: str,
        entity_name: str,
        metric: str,
        value: float,
        source: str
    ) -> Dict[str, Any]:
        """
        Build context for AGGREGATE-based queries.
        """
        if value == 0:
            raise EmptyContextError("Aggregate result is zero or empty.")

        return {
            "context_type": "AGGREGATE",
            "entity_type": entity_type,
            "entity_name": entity_name,
            "metric": metric,
            "result": {
                "value": value
            },
            "data_source": source
        }

    @staticmethod
    def build_comparison_context(
        *,
        metric: str,
        best_entity: str,
        best_value: float,
        source: str
    ) -> Dict[str, Any]:
        """
        Build context for COMPARE-based queries.
        """
        if not best_entity:
            raise EmptyContextError("Comparison result is empty.")

        return {
            "context_type": "COMPARE",
            "metric": metric,
            "result": {
                "best_entity": best_entity,
                "best_value": best_value
            },
            "data_source": source
        }

    @staticmethod
    def build_empty_context(reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Explicitly build an empty context.
        """
        return {
            "context_type": "EMPTY",
            "reason": reason or "No data found in provided files."
        }
