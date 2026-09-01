"""Detection of suspicious technical text conditions without destructive repair."""

from __future__ import annotations

import unicodedata

from .model import CleaningIssue

# These fragments are common signs of UTF-8 text decoded through the wrong legacy
# encoding. They are indicators only: SahalNLP does not auto-repair them in v1.
_MOJIBAKE_MARKERS = ("Ã", "Â", "â€", "â€™", "â€œ", "â€\u009d", "ðŸ")
_ALLOWED_CONTROLS = {"\n", "\t"}


def inspect_text(text: str) -> tuple[CleaningIssue, ...]:
    """Return unique technical issues in stable enum order."""

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    found: set[CleaningIssue] = set()

    if "\ufffd" in text:
        found.add(CleaningIssue.REPLACEMENT_CHARACTER)

    if any(marker in text for marker in _MOJIBAKE_MARKERS):
        found.add(CleaningIssue.POSSIBLE_MOJIBAKE)

    for char in text:
        category = unicodedata.category(char)
        if category == "Cc" and char not in _ALLOWED_CONTROLS:
            found.add(CleaningIssue.CONTROL_CHARACTER)
        elif category == "Cf":
            found.add(CleaningIssue.FORMAT_CHARACTER)
        elif category == "Co":
            found.add(CleaningIssue.PRIVATE_USE_CHARACTER)
        elif category == "Cs":
            found.add(CleaningIssue.SURROGATE_CHARACTER)

    return tuple(issue for issue in CleaningIssue if issue in found)
