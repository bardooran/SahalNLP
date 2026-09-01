# Project rules

These rules define how SahalNLP should grow.

## 1. Project boundary

SahalNLP is the **tools** project. SahalDataset owns reviewed corpora, training data, validation data, and frozen evaluation data. Sahal AI owns intelligence/product behavior.

Do not move dataset ownership into SahalNLP just because a tool needs to read or evaluate data.

## 2. Independent implementation

SahalNLP code, documentation, schemas, tests, and architecture should be written for this project. External NLP systems can be studied for general techniques and comparison, but source code or documentation must not be copied unless a future dependency is intentionally adopted under a compatible license and documented separately.

## 3. Preserve uncertainty

Do not turn a weak guess into a fact. Language classification and quality decisions must support uncertain outcomes.

## 4. Preserve provenance

When known, tools should preserve source identity, source type, URL, collection time, and license information so SahalDataset can retain that information with reviewed records.

## 5. Separate cleanliness from grammar

A clean text record is not automatically grammatically correct. Corpus cleaning should remove technical noise; linguistic judgment belongs to reviewed language-analysis stages.

## 6. Quality tiers

- **Gold:** human-reviewed or backed by exceptionally strong reviewed evidence.
- **Silver:** high-confidence Somali from a reliable, well-processed source.
- **Bronze:** useful but less certain material suitable for broad language modeling with caution.
- **Quarantine:** suspicious, mixed, unresolved, or otherwise unsuitable for normal training until reviewed.

A tool may downgrade or recommend a tier. Upgrading data to Gold must require explicit evidence or human review, and the reviewed result belongs in SahalDataset.

## 7. Frozen evaluation

A benchmark intended to measure unseen performance must be frozen before tuning against its answers. Frozen benchmark files belong in SahalDataset. SahalNLP should contain only the runners and scoring code needed to evaluate them.

Once benchmark answers are inspected and used for development, that benchmark becomes diagnostic/regression data and must not be described as unseen.

## 8. Clean repository structure

Code should be grouped by tool responsibility and tests should mirror those responsibilities. Do not add many narrowly named files to the repository root when a clear module or documentation category exists.

Do not create placeholder dataset directories in SahalNLP. Add a new directory only when the tools actually need it.

## 9. Claims require measurements

Test counts show regression coverage, not model superiority. Comparative claims require the same task, same data, same scoring rules, and reproducible outputs.
