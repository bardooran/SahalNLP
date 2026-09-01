"""Core immutable record types shared across SahalNLP modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping


class LanguageStatus(StrEnum):
    """A deliberately non-binary language classification."""

    SOMALI = "somali"
    NON_SOMALI = "non_somali"
    MIXED = "mixed"
    UNCERTAIN = "uncertain"


class QualityTier(StrEnum):
    """Intended data-use tier, not a grammatical-correctness label."""

    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"
    QUARANTINE = "quarantine"


@dataclass(frozen=True, slots=True)
class Provenance:
    """Where a text record came from."""

    source_id: str
    source_type: str
    license_id: str | None = None
    url: str | None = None
    collected_at: str | None = None

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id must not be blank")
        if not self.source_type.strip():
            raise ValueError("source_type must not be blank")


@dataclass(frozen=True, slots=True)
class TextRecord:
    """Minimal v1 record carried between SahalNLP stages."""

    record_id: str
    text: str
    provenance: Provenance
    language_status: LanguageStatus = LanguageStatus.UNCERTAIN
    quality_tier: QualityTier = QualityTier.QUARANTINE
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.record_id.strip():
            raise ValueError("record_id must not be blank")
        if not self.text.strip():
            raise ValueError("text must not be blank")
