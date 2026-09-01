# Project rules

These rules define how SahalNLP should grow.

## 1. Independent implementation

SahalNLP code, documentation, schemas, tests, and architecture should be written for this project. External NLP systems can be studied for general techniques and comparison, but source code or documentation must not be copied unless a future dependency is intentionally adopted under a compatible license and documented separately.

## 2. Preserve uncertainty

Do not turn a weak guess into a fact. Language classification and quality decisions must support uncertain outcomes.

## 3. Preserve provenance

When known, keep source identity, source type, URL, collection time, and license information with the record or its source manifest.

## 4. Separate cleanliness from grammar

A clean text record is not automatically grammatically correct. Corpus cleaning should remove technical noise; linguistic judgment belongs to later reviewed language-analysis layers.

## 5. Quality tiers

- **Gold:** human-reviewed or backed by exceptionally strong reviewed evidence.
- **Silver:** high-confidence Somali from a reliable, well-processed source.
- **Bronze:** useful but less certain material suitable for broad language modeling with caution.
- **Quarantine:** suspicious, mixed, unresolved, or otherwise unsuitable for normal training until reviewed.

A pipeline may downgrade data; upgrading to Gold must require explicit evidence or review.

## 6. Frozen evaluation

A benchmark intended to measure unseen performance must be frozen before tuning against its answers. Once its answers are inspected and used for development, it becomes diagnostic/regression data and must not be described as unseen.

## 7. Clean repository structure

Tests and data should be grouped by responsibility. Do not add many narrowly named files to the repository root when a clear category exists.

## 8. Claims require measurements

Test counts show regression coverage, not model superiority. Comparative claims require the same task, same data, same scoring rules, and reproducible outputs.
