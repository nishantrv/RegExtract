# Synthetic sample data

Everything under `data/` and `gold/` in this repository is **synthetic**. It was made up for testing and does not come from any real regulation.

| File | What it is |
|---|---|
| `data/sample/SAMPLE-01.pdf` | A made-up 3-page regulation ("Requirements for Registration of Garden Water Pumps", fictional issuer "Examplia Standards Authority"). It has numbered clauses, a definitions section, obligations, a validity clause, a fine, references to another law and a standard, and a product table. |
| `data/sample/SAMPLE-01.html` | The source of the PDF. Print it to PDF to rebuild it. |
| `data/corpus_catalog.json` | Invented documents that stand in for a corpus, used to link references. |
| `data/distractor_titles.txt` | Invented unrelated titles, mixed in as noise when testing reference linking. |
| `gold/section_5.json` | Hand-written labels for section 5 (definitions) of SAMPLE-01. |
| `gold/resolution.json` | Hand-written reference-linking cases for the synthetic catalogue. |

The original evaluation document used during development, and its hand-labelled data, are not included. Tests that need them are skipped automatically when `data/CARL-01.pdf` is absent.

Run the pipeline on the sample, offline and with no API key:

```bash
python run.py extract --pdf data/sample/SAMPLE-01.pdf --issuer ESA --jurisdiction EX
```
