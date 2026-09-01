# SahalNLP architecture

SahalNLP v1 separates production data processing from evaluation so that the repository stays understandable and benchmark answers cannot become hidden runtime knowledge.

## Production flow

```text
source text
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
versioned usable records
```

`evaluation` observes these stages but does not supply production rules or training examples to them.

## Package responsibilities

### `core`
Stable shared contracts: record identity, provenance, language status, quality tier, and other cross-module types. Keep this package small.

### `ingest`
Convert an external source into SahalNLP records. Ingestion must preserve source identity and should preserve license/URL/date information when available.

### `cleaning`
Repair technical text problems without pretending to judge Somali grammar. Cleaning should be reversible or auditable where practical, and uncertain destructive changes should be avoided.

### `language`
Estimate whether content is Somali, non-Somali, mixed, or uncertain. Mixed and uncertain are first-class outcomes.

### `dedup`
Detect exact and later near duplicates. Deduplication must keep enough metadata to explain why a record was retained or linked to another.

### `quality`
Assign data-use tiers. Quality is not the same as grammatical correctness.

### `evaluation`
Frozen benchmarks, scoring, and diagnostic helpers. Production modules must not read frozen benchmark answers as runtime knowledge.

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

Large downloaded corpora are not committed to Git. Small reviewed fixtures and frozen benchmark manifests may be tracked when their origin and purpose are documented.

## Growth rule

Before adding a new top-level module, answer three questions:

1. Does it solve a distinct SahalNLP responsibility?
2. Can it live clearly inside an existing module instead?
3. How will it be tested without contaminating frozen evaluation data?

This rule is meant to prevent the repository from becoming structurally confusing as it grows.
