# FAIRy ENA Rulepacks (Community)

This repository contains **ENA-focused rulepacks** for **FAIRy** — a local-first validator/packager that runs rulepacks against tabular metadata and produces human-readable + machine-readable reports.

**Scope of this repo (community):**
- Reusable, ENA/Webin-style checks that apply broadly to common ENA submission metadata patterns.
- Small public fixtures and examples for demos/tests.

---

## What’s inside
> Note: the committed tiny fixture is currently **CSV** (`fixtures/tiny/annotations.csv`) while TSV support is being added.  
> After TSV support lands, we’ll switch the fixture + examples to `.tsv` (or support both).


- `rulepacks/`
  - `ena_webin_cli/` — starter ENA community rulepack (Webin-style naming/annotation hygiene checks)
- `fixtures/`
  - `tiny/annotations.csv` — committed tiny fixture used for demos/tests
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
### Generate/refresh the derived CSV from ENA EMBL flatfiles

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
`fixtures/tiny/annotations_all.csv` (derived pool)
Then curate/update:
`fixtures/tiny/annotations.csv` (committed tiny fixture)
See `fixtures/PROVENANCE.md` for sourcing and notes.
---

## Running FAIRy with ENA rulepack

Run FAIRy against a fixture file with the ENA rulepack::

```bash
mkdir -p out

fairy validate \
  --inputs default=fixtures/tiny/annotations.csv \
  --rulepack rulepacks/ena_webin_cli/rulepack.yaml \
  --report-md out/ena_validate.md \
  --report-json out/ena_validate.json

```
Outputs typically include:
- `out/ena_validate.md` (human-readable)
- `out/ena_validate.json` (machine-readable)
---
## Contributing
Issues and PRs welcome:
- new ENA/Webin-inspired checks
- better fixtures (public-source and documented provenance)
- improved remediation wording for novices
---
## License
See `LICENSE`.