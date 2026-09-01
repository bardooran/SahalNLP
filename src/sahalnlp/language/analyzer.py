"""Conservative v1 language-status analysis for SahalNLP.

This module is an auditable evidence gate, not a general-purpose language-ID model.
It is deliberately willing to return ``uncertain`` when evidence is weak.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import re

from sahalnlp.core import LanguageStatus, TextRecord


_TOKEN_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?", re.UNICODE)

# Strong markers are intentionally small and transparent. A Somali classification
# requires at least one strong marker plus a second distinct Somali signal.
_SOMALI_STRONG_MARKERS = frozenset(
    {
        "waa",
        "ayaa",
        "waxaa",
        "waxa",
        "waxaan",
        "wuxuu",
        "waxay",
        "baan",
        "baad",
        "buu",
        "bay",
        "tahay",
        "yahay",
        "yihiin",
        "haddii",
        "laakiin",
        "laakin",
    }
)

_SOMALI_SUPPORT_MARKERS = frozenset(
    {
        "iyo",
        "oo",
        "ku",
        "ka",
        "u",
        "la",
        "marka",
        "sida",
    }
)

# v1 only has an explicit counter-signal set for clear English text. Other
# languages remain uncertain rather than being guessed as non-Somali.
_ENGLISH_STRONG_MARKERS = frozenset(
    {
        "the",
        "and",
        "are",
        "was",
        "were",
        "with",
        "this",
        "from",
        "because",
        "have",
        "has",
        "not",
        "but",
        "their",
        "they",
        "he",
        "she",
        "we",
        "our",
        "can",
        "will",
        "would",
        "should",
        "which",
        "who",
        "when",
        "where",
    }
)


@dataclass(frozen=True, slots=True)
class LanguageAnalysis:
    """Auditable evidence behind one language-status decision."""

    status: LanguageStatus
    reason: str
    token_count: int
    somali_strong_markers: tuple[str, ...] = ()
    somali_support_markers: tuple[str, ...] = ()
    english_markers: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class LanguageRecordResult:
    """A record with updated language status plus the evidence used."""

    record: TextRecord
    analysis: LanguageAnalysis


def _tokens(text: str) -> tuple[str, ...]:
    return tuple(match.group(0).casefold() for match in _TOKEN_RE.finditer(text))


def _ordered_unique_hits(tokens: tuple[str, ...], markers: frozenset[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    hits: list[str] = []
    for token in tokens:
        if token in markers and token not in seen:
            seen.add(token)
            hits.append(token)
    return tuple(hits)


def analyze_text(text: str) -> LanguageAnalysis:
    """Classify text as Somali, non-Somali, mixed, or uncertain.

    v1 recognizes only conservative lexical evidence for modern Somali written in
    Latin script plus a small set of strong English counter-signals. It does not
    claim to identify every non-Somali language.
    """

    tokens = _tokens(text)
    somali_strong = _ordered_unique_hits(tokens, _SOMALI_STRONG_MARKERS)
    somali_support = _ordered_unique_hits(tokens, _SOMALI_SUPPORT_MARKERS)
    english = _ordered_unique_hits(tokens, _ENGLISH_STRONG_MARKERS)

    somali_total = len(somali_strong) + len(somali_support)
    has_somali_base = len(somali_strong) >= 1 and somali_total >= 2
    has_strong_somali_with_minor_english_noise = (
        has_somali_base and somali_total >= 3 and len(english) == 1
    )

    if has_somali_base and len(english) >= 2:
        status = LanguageStatus.MIXED
        reason = "substantial Somali and English evidence"
    elif has_somali_base and (not english or has_strong_somali_with_minor_english_noise):
        status = LanguageStatus.SOMALI
        reason = "strong Somali evidence without substantial English counter-signal"
    elif len(english) >= 3 and somali_total == 0:
        status = LanguageStatus.NON_SOMALI
        reason = "strong English evidence with no Somali signal"
    else:
        status = LanguageStatus.UNCERTAIN
        reason = "insufficient or conflicting evidence"

    return LanguageAnalysis(
        status=status,
        reason=reason,
        token_count=len(tokens),
        somali_strong_markers=somali_strong,
        somali_support_markers=somali_support,
        english_markers=english,
    )


def analyze_record(record: TextRecord) -> LanguageRecordResult:
    """Update only ``language_status`` while preserving the rest of a record."""

    analysis = analyze_text(record.text)
    updated = replace(record, language_status=analysis.status)
    return LanguageRecordResult(record=updated, analysis=analysis)
