import json

import pytest

from sahalnlp.evaluation.language_benchmark import evaluate_records, load_records


def test_evaluate_records_scores_somali_detection_safely():
    records = [
        {
            "id": "som-1",
            "text": "Waxaan joogaa guriga oo waan shaqaynayaa.",
            "source_language": "som",
            "expected_somali": True,
        },
        {
            "id": "eng-1",
            "text": "The people are here and they have food.",
            "source_language": "eng",
            "expected_somali": False,
        },
        {
            "id": "foreign-1",
            "text": "Bonjour tout le monde.",
            "source_language": "fra",
            "expected_somali": False,
        },
    ]

    result = evaluate_records(records)

    assert result["correct"] == 3
    assert result["accuracy"] == 1.0
    assert result["somali_recall"] == 1.0
    assert result["negative_safety"] == 1.0
    assert result["negative_resolution_rate"] == 0.5
    assert result["false_positive_ids"] == []
    assert result["missed_somali_ids"] == []


def test_load_records_requires_expected_fields(tmp_path):
    path = tmp_path / "benchmark.jsonl"
    path.write_text(json.dumps({"id": "x", "text": "test"}) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing fields"):
        load_records(path)


def test_load_records_requires_boolean_target(tmp_path):
    path = tmp_path / "benchmark.jsonl"
    path.write_text(
        json.dumps(
            {
                "id": "x",
                "text": "test",
                "source_language": "eng",
                "expected_somali": "false",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="must be boolean"):
        load_records(path)
