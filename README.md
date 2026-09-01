# SahalNLP

**Somali-first NLP infrastructure for clean, auditable, linguistically useful language data.**

SahalNLP is an original project for building trustworthy Somali NLP foundations. The first release focuses on the data layer: ingesting text, cleaning it without destroying useful Somali information, classifying language status, controlling duplicates, assigning quality tiers, and evaluating every stage with frozen tests.

## v1 scope

SahalNLP v1 is intentionally small:

1. **Ingest** — accept Somali text with source metadata.
2. **Cleaning** — normalize technical noise while preserving linguistic content.
3. **Language status** — represent `somali`, `non_somali`, `mixed`, and `uncertain` instead of forcing every record into a yes/no decision.
4. **Duplicate control** — exact and near-duplicate processing.
5. **Quality & provenance** — rank usable data as Gold, Silver, Bronze, or Quarantine while retaining where it came from.
6. **Evaluation** — keep frozen evaluation data separate from development data and regression tests.

## Not in v1

Tokenizer training, POS tagging, morphology, syntax, web crawling, OCR, translation, NER, and LLM training are later modules. They should only be added after the data foundation is stable.

## Core principles

- **Somali-first:** decisions should protect Somali linguistic information, not only generic text cleanliness.
- **Uncertainty is data:** ambiguous records remain ambiguous rather than being guessed.
- **Provenance by default:** useful records should be traceable to their source and license information when known.
- **Evaluation isolation:** benchmarks must not quietly become training inputs.
- **Small modules:** new capabilities get clear homes instead of growing one large flat folder.
- **Original implementation:** SahalNLP is designed and implemented independently; external projects may inform research questions, but their code, documentation, and project structure are not copied.

## Repository layout

```text
SahalNLP/
├── src/sahalnlp/
│   ├── core/          # shared record contracts and enums
│   ├── ingest/        # source ingestion
│   ├── cleaning/      # conservative text normalization + corruption reports
│   ├── language/      # Somali/mixed/uncertain language analysis
│   ├── dedup/         # duplicate control
│   ├── quality/       # quality tiers and review policy
│   └── evaluation/    # evaluation helpers; no production learning
├── tests/             # regression and behavior tests by area
├── data/              # small reviewed fixtures only; not bulk corpora
├── benchmarks/        # frozen evaluation manifests and documentation
├── docs/              # architecture and project rules
└── .github/workflows/ # automated checks
```

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## Current status

**Cleaning v1 implemented.** The foundation, core record contracts, conservative technical text cleaner, tests, and CI are in place. Cleaning v1 normalizes safe Unicode/whitespace representation issues and flags suspicious corruption rather than guessing a repair. See `docs/CLEANING_V1.md`.

## License

No project license has been selected yet.
