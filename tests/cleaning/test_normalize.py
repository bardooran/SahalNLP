from sahalnlp.cleaning import CleaningChange, normalize_text


def test_normalize_horizontal_spacing_without_changing_words() -> None:
    text, changes = normalize_text("  Soomaaliya\twaa\u00a0dal.  ")

    assert text == "Soomaaliya waa dal."
    assert CleaningChange.HORIZONTAL_WHITESPACE in changes
    assert CleaningChange.EDGE_WHITESPACE in changes


def test_normalize_line_endings_but_preserve_paragraphs() -> None:
    text, changes = normalize_text("Khadka koowaad.\r\nKhadka labaad.\rKhadka saddexaad.")

    assert text == "Khadka koowaad.\nKhadka labaad.\nKhadka saddexaad."
    assert CleaningChange.LINE_ENDINGS in changes


def test_normalizer_does_not_spell_correct_or_collapse_letters() -> None:
    original = "Sooomaaliya, carruurtuna way ciyaareen; buuxisayna waa sidaas."
    text, changes = normalize_text(original)

    assert text == original
    assert changes == ()


def test_normalization_is_idempotent() -> None:
    once, _ = normalize_text("  Soomaaliya\twaa dal.  ")
    twice, second_changes = normalize_text(once)

    assert twice == once
    assert second_changes == ()
