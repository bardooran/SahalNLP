"""Audit-friendly result types for SahalNLP cleaning."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class CleaningChange(StrEnum):
    """Safe transformations that may be applied automatically."""

    UNICODE_NFC = "unicode_nfc"
    LINE_ENDINGS = "line_endings"
    LEADING_BOM = "leading_bom"
    HORIZONTAL_WHITESPACE = "horizontal_whitespace"
    EDGE_WHITESPACE = "edge_whitespace"


class CleaningIssue(StrEnum):
    """Suspicious technical conditions that are detected, not guessed away."""

    CONTROL_CHARACTER = "control_character"
    FORMAT_CHARACTER = "format_character"
    REPLACEMENT_CHARACTER = "replacement_character"
    PRIVATE_USE_CHARACTER = "private_use_character"
    SURROGATE_CHARACTER = "surrogate_character"
    POSSIBLE_MOJIBAKE = "possible_mojibake"


@dataclass(frozen=True, slots=True)
class CleaningResult:
    """The cleaned text plus a complete v1 audit report."""

    original_text: str
    text: str
    changes: tuple[CleaningChange, ...] = ()
    issues: tuple[CleaningIssue, ...] = ()

    @property
    def changed(self) -> bool:
        return self.original_text != self.text

    @property
    def needs_review(self) -> bool:
        return bool(self.issues)
