#!/usr/bin/env python3

import pandas as pd

matrix_file = "05_pgpr_matrix/pgpr_presence_absence_matrix.tsv"
kos_file = "04_functional_annotation/kofamscan/target_ko_ids_clean.txt"
out_file = "05_pgpr_matrix/pgpr_presence_absence_matrix_complete.tsv"

matrix = pd.read_csv(matrix_file, sep="\t")
target_kos = [line.strip() for line in open(kos_file) if line.strip()]

for ko in target_kos:
    if ko not in matrix.columns:
        matrix[ko] = 0

matrix = matrix[["genome"] + target_kos]
matrix.to_csv(out_file, sep="\t", index=False)

print("Rows:", matrix.shape[0])
print("Columns:", matrix.shape[1])
print("Saved:", out_file)
