# Language Analysis v1.1

Language v1.1 is a focused improvement to the conservative Somali-first evidence gate.

## Why this change exists

Frozen Language Benchmark v1 was selected and committed in SahalDataset before SahalNLP was measured. The untouched v1 analyzer scored 57/60 (95.0%) on the primary Somali-detection metric, with 17/20 Somali records recognized and 40/40 non-Somali records safely not classified as Somali.

After that baseline was inspected, the benchmark became a regression/diagnostic set for language v1.1. It must not be described as unseen evidence for v1.1.

## Evidence-backed additions

### `waxa`

VOA Somali uses the split construction `waxa uu` repeatedly in normal reporting, including:

- https://www.voasomali.com/z/7187?aId=6757537&p=1
- https://www.voasomali.com/a/galgala-qarax-lala-beegsaday-gaari-ciidan-/1249971.html

Language v1.1 therefore recognizes `waxa` as a strong Somali lexical signal. It still needs at least one second distinct Somali signal before a Somali classification is made.

### `laakin`

VOA Somali uses `laakin` in published Somali text, including:

- https://www.voasomali.com/a/xaaji-shukri-goaanka-maxkamadda-shaqo-kuma-lihin--95016814/1249654.html
- https://www.voasomali.com/a/7659231.html

Language v1.1 therefore accepts both `laakiin` and `laakin` as strong Somali signals. Neither spelling alone is enough to classify a text as Somali.

## Minor English noise

Language v1 treated any single English marker as enough to block an otherwise valid Somali classification. That is too brittle for Somali text containing an English publication, organization, or other named expression.

v1.1 allows exactly one English marker only when there are at least three distinct Somali signals including a strong Somali marker. Two or more English markers still produce `mixed` when the Somali base is present.

This is an engineering threshold, not a claim about Somali grammar.

## Safety rules preserved

- One Somali marker is still insufficient.
- Repeating one marker does not create extra evidence.
- Clear English still requires several distinct English signals before `non_somali`.
- Unknown foreign languages remain `uncertain` rather than being guessed.
- Analysis never rewrites the input text.
- The classifier remains an auditable lexical evidence gate, not a universal language identifier.

## Evaluation boundary

Language Benchmark v1 may be used only as regression/diagnostic data after the baseline measurement. A new separately frozen benchmark is required before making a fresh generalization claim about v1.1.
