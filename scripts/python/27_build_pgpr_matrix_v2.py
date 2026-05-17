#!/usr/bin/env python3
"""
Build PGPR presence-absence matrix v2 from parsed HMMER results.

This version uses parsed hits filtered with KO-specific KOfam thresholds.
"""

from pathlib import Path
import pandas as pd

IN_DIR = Path("04_functional_annotation/kofamscan/parsed_results_v2")
KO_FILE = Path("04_functional_annotation/kofamscan/target_ko_ids_v2.txt")
FINAL_ACCESSIONS = Path("00_metadata/final_accessions.txt")

OUT_HITS = Path("04_functional_annotation/kofamscan/annotation_summary/pgpr_hits_filtered_all_v2.tsv")
OUT_MATRIX = Path("05_pgpr_matrix/pgpr_presence_absence_matrix_v2.tsv")

kos = [x.strip() for x in KO_FILE.read_text().splitlines() if x.strip()]
genomes = [x.strip() for x in FINAL_ACCESSIONS.read_text().splitlines() if x.strip()]

all_hits = []

for tsv in sorted(IN_DIR.glob("*.tsv")):
    genome = tsv.stem
    df = pd.read_csv(tsv, sep="\t")

    if df.empty:
        continue

    df.insert(0, "genome", genome)
    all_hits.append(df)

if all_hits:
    hits_all = pd.concat(all_hits, ignore_index=True)
else:
    hits_all = pd.DataFrame(columns=[
        "genome", "protein_id", "ko", "evalue", "score",
        "threshold", "score_minus_threshold"
    ])

OUT_HITS.parent.mkdir(parents=True, exist_ok=True)
OUT_MATRIX.parent.mkdir(parents=True, exist_ok=True)

hits_all.to_csv(OUT_HITS, sep="\t", index=False)

matrix = pd.DataFrame({"genome": genomes})

if not hits_all.empty:
    detected = (
        hits_all.assign(present=1)
        .pivot_table(index="genome", columns="ko", values="present", fill_value=0, aggfunc="max")
        .reset_index()
    )
    matrix = matrix.merge(detected, on="genome", how="left")

for ko in kos:
    if ko not in matrix.columns:
        matrix[ko] = 0

matrix[kos] = matrix[kos].fillna(0).astype(int)
matrix = matrix[["genome"] + kos]

matrix.to_csv(OUT_MATRIX, sep="\t", index=False)

print("Expected genomes:", len(genomes))
print("Matrix rows:", matrix.shape[0])
print("Expected KOs:", len(kos))
print("Matrix KO columns:", len([c for c in matrix.columns if c.startswith('K')]))
print("Genomes with at least one hit:", hits_all["genome"].nunique() if not hits_all.empty else 0)
print("Total filtered genome-KO hits:", len(hits_all))
print("Saved:", OUT_HITS)
print("Saved:", OUT_MATRIX)
