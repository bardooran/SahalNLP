"""Evaluate SahalNLP language analysis against a frozen JSONL benchmark."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Any, Iterable

from sahalnlp.core import LanguageStatus
from sahalnlp.language import analyze_text

_REQUIRED_FIELDS = frozenset({"id", "text", "source_language", "expected_somali"})


def load_records(path: str | Path) -> list[dict[str, Any]]:
    """Load and minimally validate benchmark records without changing them."""

    records: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not raw_line.strip():
            continue
        record = json.loads(raw_line)
        missing = _REQUIRED_FIELDS - record.keys()
        if missing:
            names = ", ".join(sorted(missing))
            raise ValueError(f"benchmark line {line_number} missing fields: {names}")
        if not isinstance(record["expected_somali"], bool):
            raise ValueError(f"benchmark line {line_number} expected_somali must be boolean")
        records.append(record)
    if not records:
        raise ValueError("benchmark is empty")
    return records


def evaluate_records(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Return transparent Somali-detection metrics and status distributions."""

    total = 0
    correct = 0
    somali_total = 0
    somali_recognized = 0
    negative_total = 0
    negative_safe = 0
    negative_resolved = 0
    false_positive_ids: list[str] = []
    missed_somali_ids: list[str] = []
    by_language: dict[str, Counter[str]] = defaultdict(Counter)

    for record in records:
        analysis = analyze_text(record["text"])
        status = analysis.status
        status_value = status.value
        expected_somali = record["expected_somali"]
        predicted_somali = status is LanguageStatus.SOMALI
        source_language = str(record["source_language"])

        total += 1
        by_language[source_language][status_value] += 1

        if expected_somali:
            somali_total += 1
            if predicted_somali:
                somali_recognized += 1
                correct += 1
            else:
                missed_somali_ids.append(str(record["id"]))
        else:
            negative_total += 1
            if not predicted_somali:
                negative_safe += 1
                correct += 1
            else:
                false_positive_ids.append(str(record["id"]))
            if status is LanguageStatus.NON_SOMALI:
                negative_resolved += 1

    def ratio(numerator: int, denominator: int) -> float:
        return numerator / denominator if denominator else 0.0

    return {
        "total": total,
        "correct": correct,
        "accuracy": ratio(correct, total),
        "somali_total": somali_total,
        "somali_recognized": somali_recognized,
        "somali_recall": ratio(somali_recognized, somali_total),
        "negative_total": negative_total,
        "negative_safe": negative_safe,
        "negative_safety": ratio(negative_safe, negative_total),
        "negative_resolved_non_somali": negative_resolved,
        "negative_resolution_rate": ratio(negative_resolved, negative_total),
        "false_positive_ids": false_positive_ids,
        "missed_somali_ids": missed_somali_ids,
        "status_by_source_language": {
            language: dict(sorted(counts.items()))
            for language, counts in sorted(by_language.items())
        },
    }


def evaluate_file(path: str | Path) -> dict[str, Any]:
    return evaluate_records(load_records(path))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("benchmark", type=Path)
    args = parser.parse_args()
    print(json.dumps(evaluate_file(args.benchmark), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
