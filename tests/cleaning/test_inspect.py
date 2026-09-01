from sahalnlp.cleaning import CleaningIssue, clean_text, inspect_text


def test_normal_somali_text_has_no_technical_issue() -> None:
    assert inspect_text("Carruurtu way ciyaareen maanta.") == ()


def test_replacement_character_is_flagged_not_deleted() -> None:
    result = clean_text("Soomaaliya \ufffd waa dal.")

    assert CleaningIssue.REPLACEMENT_CHARACTER in result.issues
    assert "\ufffd" in result.text
    assert result.needs_review is True


def test_format_character_is_flagged_not_deleted() -> None:
    original = "Soomaali\u200bya"
    result = clean_text(original)

    assert CleaningIssue.FORMAT_CHARACTER in result.issues
    assert result.text == original


def test_control_character_is_flagged_not_deleted() -> None:
    original = "Somali\x07text"
    result = clean_text(original)

    assert CleaningIssue.CONTROL_CHARACTER in result.issues
    assert "\x07" in result.text


def test_possible_mojibake_is_detection_only() -> None:
    original = "Qoraal â€™ jaban"
    result = clean_text(original)

    assert CleaningIssue.POSSIBLE_MOJIBAKE in result.issues
    assert result.text == original
