"""Public cleaning operations for strings and SahalNLP records."""

from __future__ import annotations

from dataclasses import replace

from sahalnlp.core import TextRecord

from .inspect import inspect_text
from .model import CleaningResult
from .normalize import normalize_text


def clean_text(text: str) -> CleaningResult:
    """Normalize safe technical noise and report unresolved suspicious content."""

    normalized, changes = normalize_text(text)
    return CleaningResult(
        original_text=text,
        text=normalized,
        changes=changes,
        issues=inspect_text(normalized),
    )


def clean_record(record: TextRecord) -> tuple[TextRecord, CleaningResult]:
    """Clean only ``record.text`` while preserving every other record field."""

    result = clean_text(record.text)
    if not result.text.strip():
        raise ValueError("cleaning produced an empty text record")
    return replace(record, text=result.text), result
