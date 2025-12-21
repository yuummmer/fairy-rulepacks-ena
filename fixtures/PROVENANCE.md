# Fixture provenance (ENA community rulepack)

This repo contains small, derived fixtures used to demonstrate ENA/Webin-style validation checks.

## Source records (public INSDC/ENA accessions)
- AB015477.1
- AB023029.1
- AB808705.1
- AY164027.1
- KP191301.1
- PV530470.1

## How fixtures are produced
- Records downloaded as EMBL flatfiles and stored under:
  fixtures/raw_downloads/ena_embl/   (intentionally gitignored)
- CDS qualifiers extracted into:
  fixtures/tiny/annotations_all.tsv
  using scripts/extract_embl_products.py
- A curated subset is committed as:
  fixtures/tiny/annotations.tsv

## Notes
- Rows with source_accession = DERIVED are intentionally edited/added examples to guarantee test coverage of specific validation patterns.