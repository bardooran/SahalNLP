from sahalnlp.core import LanguageStatus, Provenance, QualityTier, TextRecord
from sahalnlp.language import analyze_record, analyze_text


def test_clear_somali_with_multiple_distinct_signals() -> None:
    result = analyze_text("Soomaaliya waa dal ku yaal Geeska Afrika.")

    assert result.status is LanguageStatus.SOMALI
    assert "waa" in result.somali_strong_markers
    assert "ku" in result.somali_support_markers
    assert result.english_markers == ()


def test_another_clear_somali_example() -> None:
    result = analyze_text("Waxaan magaalada ka shaqeeyaa.")

    assert result.status is LanguageStatus.SOMALI
    assert result.somali_strong_markers == ("waxaan",)
    assert result.somali_support_markers == ("ka",)


def test_waxa_split_form_provides_strong_somali_evidence() -> None:
    result = analyze_text("waxa uu ku")

    assert result.status is LanguageStatus.SOMALI
    assert result.somali_strong_markers == ("waxa",)
    assert result.somali_support_markers == ("ku",)


def test_laakin_variant_provides_strong_somali_evidence() -> None:
    result = analyze_text("laakin oo")

    assert result.status is LanguageStatus.SOMALI
    assert result.somali_strong_markers == ("laakin",)
    assert result.somali_support_markers == ("oo",)


def test_one_english_marker_does_not_veto_three_somali_signals() -> None:
    result = analyze_text("ayaa oo iyo The")

    assert result.status is LanguageStatus.SOMALI
    assert result.english_markers == ("the",)


def test_two_english_markers_still_make_substantial_mixed_evidence() -> None:
    result = analyze_text("ayaa oo iyo the and")

    assert result.status is LanguageStatus.MIXED
    assert result.english_markers == ("the", "and")


def test_clear_english_requires_several_distinct_signals() -> None:
    result = analyze_text("The children are playing with their friends and teachers.")

    assert result.status is LanguageStatus.NON_SOMALI
    assert len(result.english_markers) >= 3


def test_mixed_requires_evidence_from_both_sides() -> None:
    result = analyze_text("Waxaan magaalada ka shaqeeyaa because the office is nearby.")

    assert result.status is LanguageStatus.MIXED
    assert result.somali_strong_markers == ("waxaan",)
    assert result.somali_support_markers == ("ka",)
    assert "because" in result.english_markers
    assert "the" in result.english_markers


def test_short_text_stays_uncertain() -> None:
    result = analyze_text("Muqdisho 2026")

    assert result.status is LanguageStatus.UNCERTAIN


def test_one_somali_marker_is_not_enough() -> None:
    result = analyze_text("Tani waa tijaabo")

    assert result.status is LanguageStatus.UNCERTAIN


def test_repeating_one_marker_does_not_fake_more_evidence() -> None:
    result = analyze_text("waa waa waa waa")

    assert result.status is LanguageStatus.UNCERTAIN
    assert result.somali_strong_markers == ("waa",)


def test_non_english_foreign_script_is_not_guessed() -> None:
    result = analyze_text("مرحبا بالعالم")

    assert result.status is LanguageStatus.UNCERTAIN


def test_marker_matching_uses_whole_tokens() -> None:
    result = analyze_text("theater wavelength")

    assert result.status is LanguageStatus.UNCERTAIN
    assert result.english_markers == ()


def test_record_analysis_changes_only_language_status() -> None:
    provenance = Provenance(
        source_id="reviewed-example",
        source_type="fixture",
        license_id="example-only",
        url="https://example.invalid/1",
    )
    original = TextRecord(
        record_id="r-1",
        text="Waxaan magaalada ka shaqeeyaa.",
        provenance=provenance,
        quality_tier=QualityTier.SILVER,
        metadata={"domain": "general"},
    )

    result = analyze_record(original)

    assert result.record.text == original.text
    assert result.record.record_id == original.record_id
    assert result.record.provenance == original.provenance
    assert result.record.quality_tier is QualityTier.SILVER
    assert result.record.metadata == original.metadata
    assert result.record.language_status is LanguageStatus.SOMALI


def test_analysis_does_not_rewrite_input_text() -> None:
    text = "  Waxaan\t magaalada ka shaqeeyaa.  "

    result = analyze_text(text)

    assert result.status is LanguageStatus.SOMALI
    assert text == "  Waxaan\t magaalada ka shaqeeyaa.  "
