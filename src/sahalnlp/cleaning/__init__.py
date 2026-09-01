"""Somali-aware technical text cleaning.

The v1 cleaner performs only language-preserving technical normalization. Suspicious
corruption is reported for review instead of being guessed away. This package does
not judge grammatical correctness or spelling.
"""

from .inspect import inspect_text
from .model import CleaningChange, CleaningIssue, CleaningResult
from .normalize import normalize_text
from .pipeline import clean_record, clean_text

__all__ = [
    "CleaningChange",
    "CleaningIssue",
    "CleaningResult",
    "clean_record",
    "clean_text",
    "inspect_text",
    "normalize_text",
]
