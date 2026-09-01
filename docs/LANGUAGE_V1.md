# Language Analysis v1

Language Analysis v1 gives SahalNLP a conservative first way to assign the existing language-status labels:

- `somali`
- `non_somali`
- `mixed`
- `uncertain`

It is intentionally an **auditable evidence gate**, not a general language-identification model.

## What v1 uses

The analyzer tokenizes text and looks for a deliberately small set of transparent lexical signals:

- strong Somali function-word/clitic signals;
- supporting Somali signals;
- strong English counter-signals.

A Somali decision needs at least one strong Somali signal plus a second distinct Somali signal. Repeating the same word does not create extra evidence.

A non-Somali decision in v1 is narrower: it requires several distinct strong English signals and no Somali signal. Text in other languages is generally left `uncertain` rather than guessed.

A mixed decision requires substantial evidence from both the Somali and English signal sets.

## What v1 does not do

Language Analysis v1 does not:

- identify every language;
- treat Arabic-script text as automatically non-Somali;
- use a statistical or neural language-ID model;
- return a fake probability or calibrated confidence score;
- rewrite, translate, spell-correct, or clean the input;
- change a record's quality tier;
- prove that text is grammatically correct Somali.

The cleaner and language analyzer remain separate stages.

## Auditability

`LanguageAnalysis` returns the exact distinct markers that contributed to a decision and a short reason. `analyze_record()` updates only `language_status`; provenance, text, metadata, record ID, and quality tier are preserved.

## Evaluation boundary

The unit tests in `tests/language/` are **development/regression tests**. They were authored while implementing v1 and must not be described as unseen performance.

A future genuine unseen language benchmark must be selected from separately sourced material, frozen before its labels are used for tuning, and stored under `benchmarks/language/` with its provenance and scoring policy.

## Why this is intentionally conservative

Somali shares the Latin script with many other languages, code-switching is common, and short text is inherently difficult to classify safely. Returning `uncertain` is preferable to turning weak evidence into a false fact.
