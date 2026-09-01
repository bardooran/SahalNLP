# SahalNLP

**Somali-first NLP tools for building clean, auditable, linguistically useful data.**

SahalNLP is the **tools** project in the Sahal ecosystem. It contains Python code for processing and evaluating Somali language data. Reviewed corpora, training data, validation data, and frozen evaluation data belong in **SahalDataset**, not in this repository.

## Sahal ecosystem map

- **SahalNLP = tools**
- **SahalDataset = data**
- **Sahal AI = intelligence/product**

## v1 scope

SahalNLP v1 is intentionally small:

1. **Ingest** — accept text with source metadata.
2. **Cleaning** — normalize technical noise while preserving useful Somali linguistic content.
3. **Language status** — represent `somali`, `non_somali`, `mixed`, and `uncertain` instead of forcing every record into a yes/no decision.
4. **Duplicate control** — exact and later near-duplicate processing.
5. **Quality tooling** — apply explicit quality/review policy without treating a guess as reviewed fact.
6. **Evaluation tooling** — score frozen data supplied from SahalDataset without embedding benchmark answers in production code.

## Not in v1

Tokenizer training, POS tagging, morphology, syntax, web crawling, OCR, translation, NER, and LLM training are later stages. They should only be added when the current foundation is stable and there is a clear need.

## Core principles

- **Somali-first:** protect Somali linguistic information, not only generic text cleanliness.
- **Uncertainty is data:** ambiguous records remain ambiguous rather than being guessed.
- **Provenance by default:** processing should preserve available source and licensing metadata.
- **Project separation:** SahalNLP contains tools; SahalDataset contains reviewed and frozen data.
- **Evaluation isolation:** frozen benchmark answers must never become hidden runtime knowledge.
- **Small modules:** new capabilities get clear homes instead of growing one large flat folder.
- **Original implementation:** external projects may inform research questions, but their code, documentation, and project structure are not copied.

## Repository layout

```text
SahalNLP/
├── src/sahalnlp/
│   ├── core/          # shared record contracts and enums
│   ├── ingest/        # source ingestion tools
│   ├── cleaning/      # conservative text normalization + corruption reports
│   ├── language/      # conservative Somali/mixed/non-Somali/uncertain analysis
│   ├── dedup/         # duplicate-control tools
│   ├── quality/       # quality/review policy tools
│   └── evaluation/    # evaluation runners and scoring helpers
├── tests/             # development and regression tests by area
├── docs/              # architecture, rules, and implementation notes
└── .github/workflows/ # automated tests and benchmark runners
```

## Data boundary

SahalNLP may read local files during development or CI, but dataset content is not owned here. Reviewed corpora, training/validation splits, and frozen benchmark files live in **SahalDataset** with provenance and licensing information.

Evaluation workflows should pin the exact SahalDataset revision and verify downloaded benchmark files when practical. This keeps development tests separate from frozen/unseen evaluation data.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## Current status

**Language Analysis v1.1 is implemented.** The foundation, Cleaning v1, conservative language-status analyzer, and a frozen-benchmark runner are in place. The benchmark runner downloads frozen evaluation data from SahalDataset; the benchmark data itself is not stored in SahalNLP.

Development/regression tests are not unseen benchmarks. Comparative performance claims require a fair frozen evaluation with the same task, data, scoring rules, and reproducible outputs.

## License

No project license has been selected yet.
