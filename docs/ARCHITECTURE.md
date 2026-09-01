# SahalNLP architecture

SahalNLP is the **tools** layer of the Sahal ecosystem.

```text
SahalNLP     = tools
SahalDataset = data
Sahal AI     = intelligence/product
```

The repository should contain reusable Python processing and evaluation code. Reviewed corpora, training/validation data, and frozen benchmark files belong in SahalDataset.

## Processing flow

```text
external/source data
   ↓
ingest
   ↓
cleaning
   ↓
language status
   ↓
dedup
   ↓
quality decision
   ↓
output records for review/storage in SahalDataset
```

`evaluation` measures SahalNLP behavior against data supplied from SahalDataset. Production modules must not read frozen benchmark answers as runtime knowledge.

## Package responsibilities

### `core`
Stable shared contracts: record identity, provenance, language status, quality tier, and other cross-module types. Keep this package small.

### `ingest`
Convert an external source into SahalNLP records while preserving available source, license, URL, and date metadata.

### `cleaning`
Repair technical text problems without pretending to judge Somali grammar. Cleaning should be reversible or auditable where practical, and uncertain destructive changes should be avoided.

### `language`
Estimate whether content is Somali, non-Somali, mixed, or uncertain. Mixed and uncertain are first-class outcomes.

### `dedup`
Detect exact and later near duplicates. Deduplication should preserve enough metadata to explain why records were linked or retained.

### `quality`
Apply explicit quality and review policy. A tool may assign or recommend a tier, but reviewed dataset truth belongs in SahalDataset.

### `evaluation`
Benchmark runners, scoring, and diagnostics. Frozen benchmark files themselves live in SahalDataset and should be pinned to an exact revision for reproducibility.

## Dependency direction

Feature modules may depend on `core`. `core` must not depend on feature modules. Evaluation may call production modules; production modules must not depend on evaluation.

```text
core ← ingest
core ← cleaning
core ← language
core ← dedup
core ← quality

production modules → evaluated by → evaluation
```

## Data policy

Do not commit corpora, training data, validation data, reviewed examples, or frozen benchmark answers to SahalNLP. Those belong in SahalDataset with provenance and licensing information.

Small literal examples may still exist inside unit tests when they are necessary to test code behavior. Those are development/regression fixtures, not frozen unseen benchmark data.

## Growth rule

Before adding a new module, answer three questions:

1. Is it a reusable NLP/data-processing **tool**?
2. Can it live clearly inside an existing module instead?
3. Can it be tested without moving dataset ownership into SahalNLP?

This keeps SahalNLP focused and prevents the Sahal projects from becoming mixed together.
