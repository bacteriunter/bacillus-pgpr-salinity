#!/usr/bin/env python3

from pathlib import Path
import pandas as pd

IN_DIR = Path("04_functional_annotation/kofamscan/hmmsearch_results")
OUT_HITS = Path("04_functional_annotation/kofamscan/annotation_summary/pgpr_hits_filtered_all.tsv")
OUT_MATRIX = Path("05_pgpr_matrix/pgpr_presence_absence_matrix.tsv")

EVALUE_CUTOFF = 1e-10

all_hits = []

for tbl in sorted(IN_DIR.glob("*.tbl")):
    genome = tbl.stem
    hits = []

    with open(tbl) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue

            parts = line.strip().split()
            protein_id = parts[0]
            ko = parts[2]
            evalue = float(parts[4])
            score = float(parts[5])

            if evalue <= EVALUE_CUTOFF:
                hits.append({
                    "genome": genome,
                    "protein_id": protein_id,
                    "ko": ko,
                    "evalue": evalue,
                    "score": score
                })

    if hits:
        df = pd.DataFrame(hits)
        df = df.sort_values(["ko", "score"], ascending=[True, False])
        df = df.drop_duplicates(subset=["ko"], keep="first")
        all_hits.append(df)

if all_hits:
    hits_all = pd.concat(all_hits, ignore_index=True)
else:
    hits_all = pd.DataFrame(columns=["genome", "protein_id", "ko", "evalue", "score"])

OUT_HITS.parent.mkdir(parents=True, exist_ok=True)
OUT_MATRIX.parent.mkdir(parents=True, exist_ok=True)

hits_all.to_csv(OUT_HITS, sep="\t", index=False)

matrix = (
    hits_all.assign(present=1)
    .pivot_table(index="genome", columns="ko", values="present", fill_value=0, aggfunc="max")
    .reset_index()
)

matrix.to_csv(OUT_MATRIX, sep="\t", index=False)

print("Genomes with hits:", hits_all["genome"].nunique())
print("Total filtered genome-KO hits:", len(hits_all))
print("Saved:", OUT_HITS)
print("Saved:", OUT_MATRIX)
