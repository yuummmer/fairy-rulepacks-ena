from pathlib import Path
import csv
import re

IN_DIR = Path("fixtures/raw_downloads/ena_embl")
OUT = Path("fixtures/tiny/annotations_all.tsv")
OUT.parent.mkdir(parents=True, exist_ok=True)

re_cds = re.compile(r"^FT\s+CDS\s+")
re_qstart = re.compile(r'^FT\s+/(gene|locus_tag|product)="(.*)$')

def strip_ft_prefix(line: str) -> str:
    return re.sub(r"^FT\s+", "", line).rstrip()

rows = []

for fp in sorted(IN_DIR.glob("*.embl")):
    acc = fp.stem

    in_cds = False
    gene = ""
    product = ""
    locus = ""
    cds_idx = 0

    cur_key = None
    cur_val = ""

    lines = fp.read_text(encoding="utf-8", errors="replace").splitlines()

    # We'll flush by repeating a small block inline instead:
    for line in lines:
        # New CDS begins
        if re_cds.match(line):
            if in_cds and (gene or product or locus):
                cds_idx += 1
                rows.append({
                    "source_accession": acc,
                    "feature_id": locus or f"CDS_{cds_idx}",
                    "gene_name": gene or locus or "",
                    "product_name": product,
                })
            in_cds = True
            gene = ""
            product = ""
            locus = ""
            cur_key = None
            cur_val = ""
            continue

        if not in_cds:
            continue

        # Continuation of a multi-line qualifier
        if cur_key is not None:
            cont = strip_ft_prefix(line).strip()
            
            if cont.endswith('"'):
                chunk = cont[:-1]
                if cur_val and not cur_val.endswith(" ") and chunk and not chunk.startswith(" "):
                    cur_val += " "
                cur_val += chunk

                if cur_key == "gene":
                    gene = cur_val
                elif cur_key == "product":
                    product = cur_val
                elif cur_key == "locus_tag":
                    locus = cur_val

                cur_key = None
                cur_val = ""
            else:
                if cur_val and not cur_val.endswith(" ") and cont and not cont.startswith(" "):
                    cur_val += " "
                cur_val += cont

            continue

        # Start of a qualifier
        m = re_qstart.match(line)
        if m:
            key = m.group(1)
            rest = m.group(2)

            if rest.endswith('"'):
                val = rest[:-1]
                if key == "gene":
                    gene = val
                elif key == "product":
                    product = val
                elif key == "locus_tag":
                    locus = val
            else:
                cur_key = key
                cur_val = rest
            continue

    # Flush last CDS in file
    if in_cds and (gene or product or locus):
        cds_idx += 1
        rows.append({
            "source_accession": acc,
            "feature_id": locus or f"CDS_{cds_idx}",
            "gene_name": gene or locus or "",
            "product_name": product,
        })

    print(f"{acc}: extracted {cds_idx} CDS rows")

with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(
        f,
        fieldnames=["source_accession", "feature_id", "gene_name", "product_name"],
        delimiter="\t",
    )
    w.writeheader()
    w.writerows(rows)

print(f"TOTAL: wrote {len(rows)} CDS rows -> {OUT}")
