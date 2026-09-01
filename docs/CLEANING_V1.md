# Cleaning engine v1

SahalNLP cleaning v1 has a narrow job: remove technical representation noise without
making linguistic decisions for Somali text.

## Automatically normalized

The cleaner may perform these operations because they do not require a grammar or
spelling judgment:

- Unicode NFC normalization.
- CRLF/CR line-ending normalization to LF.
- removal of a leading Unicode BOM.
- normalization of horizontal Unicode spacing to an ordinary space.
- removal of whitespace at the outer edges of a record.

Every applied operation is returned in `CleaningResult.changes`.

## Detection only

The following conditions are reported in `CleaningResult.issues` but are not
silently repaired or deleted:

- unexpected control characters;
- Unicode format/invisible characters;
- Unicode replacement characters (`U+FFFD`);
- private-use and surrogate characters;
- common signs of mojibake / incorrect decoding.

A reported issue means **review is needed**, not that the sentence is bad Somali.

## Explicit non-goals

Cleaning v1 does not:

- correct Somali spelling;
- judge grammar;
- lowercase text;
- rewrite punctuation;
- collapse repeated letters;
- remove foreign-language material;
- assign Gold/Silver/Bronze quality;
- guess a repaired string when encoding damage is uncertain.

These boundaries protect linguistic evidence from accidental destruction.

## Public API

- `normalize_text(text)` — safe normalization plus change list.
- `inspect_text(text)` — detect unresolved technical issues.
- `clean_text(text)` — produce one audit-friendly `CleaningResult`.
- `clean_record(record)` — clean only the text field of a `TextRecord` while preserving provenance, language status, quality tier, and metadata.

All normalization operations are required to be idempotent: cleaning an already
cleaned string must make no additional change.
