import pytest

from sahalnlp import LanguageStatus, Provenance, QualityTier, TextRecord


def test_new_record_defaults_to_uncertain_quarantine() -> None:
    record = TextRecord(
        record_id="example:1",
        text="Soomaali waa af hodan ah.",
        provenance=Provenance(source_id="fixture", source_type="reviewed_fixture"),
    )

    assert record.language_status is LanguageStatus.UNCERTAIN
    assert record.quality_tier is QualityTier.QUARANTINE


def test_record_can_preserve_explicit_status_and_quality() -> None:
    record = TextRecord(
        record_id="example:2",
        text="Qoraal tijaabo ah.",
        provenance=Provenance(source_id="fixture", source_type="reviewed_fixture"),
        language_status=LanguageStatus.SOMALI,
        quality_tier=QualityTier.GOLD,
    )

    assert record.language_status.value == "somali"
    assert record.quality_tier.value == "gold"


@pytest.mark.parametrize("field,value", [("source_id", ""), ("source_type", "  ")])
def test_provenance_rejects_blank_required_fields(field: str, value: str) -> None:
    kwargs = {"source_id": "source", "source_type": "fixture", field: value}
    with pytest.raises(ValueError):
        Provenance(**kwargs)


def test_record_rejects_blank_text() -> None:
    with pytest.raises(ValueError):
        TextRecord(
            record_id="example:3",
            text="   ",
            provenance=Provenance(source_id="fixture", source_type="reviewed_fixture"),
        )
