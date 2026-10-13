"""Processor registry — name -> worker class lookup."""

from __future__ import annotations

from palette_ai.processors.ai_cluster_processor import AIClusterProcessor
from palette_ai.processors.base import BaseProcessor
from palette_ai.processors.kmeans_processor import KMeansProcessor

_REGISTRY: dict[str, type[BaseProcessor]] = {
    KMeansProcessor.name: KMeansProcessor,
    AIClusterProcessor.name: AIClusterProcessor,
}


def get_processor(name: str) -> BaseProcessor:
    """Instantiate a processor by name. Raises KeyError if unknown."""
    return _REGISTRY[name]()


def available() -> list[str]:
    return sorted(_REGISTRY)