"""Conservative, language-preserving Unicode and whitespace normalization."""

from __future__ import annotations

import re
import unicodedata

from .model import CleaningChange

# Horizontal spacing characters that can safely be represented as an ordinary space.
# Newlines are deliberately excluded so paragraph structure is preserved.
_HORIZONTAL_SPACE_RE = re.compile(r"[ \t\u00a0\u1680\u2000-\u200a\u202f\u205f\u3000]+")


def normalize_text(text: str) -> tuple[str, tuple[CleaningChange, ...]]:
    """Apply only transformations that do not require linguistic judgment.

    This function does not lowercase, spell-correct, rewrite punctuation, collapse
    repeated letters, or alter Somali words.
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    value = text
    changes: list[CleaningChange] = []

    if value.startswith("\ufeff"):
        value = value.lstrip("\ufeff")
        changes.append(CleaningChange.LEADING_BOM)

    nfc = unicodedata.normalize("NFC", value)
    if nfc != value:
        value = nfc
        changes.append(CleaningChange.UNICODE_NFC)

    line_normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    if line_normalized != value:
        value = line_normalized
        changes.append(CleaningChange.LINE_ENDINGS)

    horizontal = _HORIZONTAL_SPACE_RE.sub(" ", value)
    if horizontal != value:
        value = horizontal
        changes.append(CleaningChange.HORIZONTAL_WHITESPACE)

    edged = value.strip(" \n")
    if edged != value:
        value = edged
        changes.append(CleaningChange.EDGE_WHITESPACE)

    return value, tuple(changes)
