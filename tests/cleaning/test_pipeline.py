from sahalnlp.cleaning import clean_record, clean_text
from sahalnlp.core import LanguageStatus, Provenance, QualityTier, TextRecord


def test_clean_record_changes_only_text() -> None:
    record = TextRecord(
        record_id="sample:1",
        text="  Soomaaliya\twaa dal.  ",
        provenance=Provenance(
            source_id="reviewed-sample",
            source_type="fixture",
            license_id="test-only",
        ),
        language_status=LanguageStatus.SOMALI,
        quality_tier=QualityTier.SILVER,
        metadata={"domain": "general"},
    )

    cleaned, report = clean_record(record)

    assert cleaned.text == "Soomaaliya waa dal."
    assert cleaned.record_id == record.record_id
    assert cleaned.provenance == record.provenance
    assert cleaned.language_status == LanguageStatus.SOMALI
    assert cleaned.quality_tier == QualityTier.SILVER
    assert cleaned.metadata == record.metadata
    assert report.changed is True


def test_clean_text_second_pass_makes_no_new_change() -> None:
    first = clean_text("\ufeff  Soomaaliya\twaa dal.  ")
    second = clean_text(first.text)

    assert first.changed is True
    assert second.changed is False
    assert second.changes == ()
