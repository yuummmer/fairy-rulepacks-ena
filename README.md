# FAIRy ENA Rulepacks (Community)

This repository contains **ENA-focused rulepacks** for **FAIRy** — a local-first validator/packager that runs rulepacks against tabular metadata and produces human-readable + machine-readable reports.

**Scope of this repo (community):**
- Reusable, ENA/Webin-style checks that apply broadly to common ENA submission metadata patterns.
- Small public fixtures and examples for demos/tests.

---

## What’s inside

- `rulepacks/`
  - `ena_webin_cli/` — starter ENA community rulepack (Webin-style naming/annotation hygiene checks)
- `fixtures/`
  - `tiny/annotations.tsv` — committed tiny fixture used for demos/tests
  - `PROVENANCE.md` — where fixtures came from and how they were derived
- `scripts/`
  - `extract_embl_products.py` — helper to extract CDS `/product` (and gene/locus when present) from EMBL flatfiles into TSV

---

## Prerequisites

You need **FAIRy** installed from `fairy-core`.

Example (from a Python venv):

```bash
pip install -e /path/to/fairy-core
```
---
## Quickstart (dev workflow)
### 1)Generate/refresh the derived TSV from ENA EMBL flatfiles
1. Download one or more ENA records as EMBL flatfile (public INSDC/ENA accessions).
2. Put them under:

```bash
fixtures/raw_downloads/ena_embl
```
3. Run extraction:
```bash
python scripts/extract_embl_products.py
```
This writes:
`fixtures/tiny/annotations_all.tsv` (derived pool)
Then curate/update:
`fixtures/tiny/annotations.tsv` (committed tiny fixture)
See `fixtures/PROVENANCE.md` for sourcing and notes.
---

## Running FAIRy with ENA rulepack

From your `fairy-core` environment, run FAIRy against a fixture file with the ENA rulepack (exact CLI flags may vary depending on your FAIRy version):

```bash
fairy validate \
  --rulepack rulepacks/ena_webin_cli/rulepack.yaml \
  --input fixtures/tiny/annotations.tsv \
  --out out/

```
Outputs typically include:
- `report.md` (human-readable)
- `report.json` (machine-readable)
---
## Contributing
Issues and PRs welcome:
- new ENA/Webin-inspired checks
- better fixtures (public-source and documented provenance)
- improved remediation wording for novices
---
## License
See `LICENSE`.