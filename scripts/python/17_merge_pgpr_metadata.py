#!/usr/bin/env python3

import pandas as pd

sal_file = "00_metadata/saline_final.tsv"
non_file = "00_metadata/non_saline_final.tsv"
matrix_file = "05_pgpr_matrix/pgpr_presence_absence_matrix_complete.tsv"
out_file = "05_pgpr_matrix/pgpr_matrix_with_metadata.tsv"

sal = pd.read_csv(sal_file, sep="\t")
non = pd.read_csv(non_file, sep="\t")
matrix = pd.read_csv(matrix_file, sep="\t")

sal["group"] = "saline"
non["group"] = "non_saline"

meta = pd.concat([sal, non], ignore_index=True)
meta = meta.rename(columns={"Assembly Accession": "genome"})

cols = [
    "genome",
    "Organism Name",
    "species_clean",
    "group",
    "Assembly BioSample Isolation source",
    "Assembly BioSample Geographic location"
]

cols = [c for c in cols if c in meta.columns]
meta = meta[cols]

merged = meta.merge(matrix, on="genome", how="inner")
merged.to_csv(out_file, sep="\t", index=False)

print("Metadata genomes:", len(meta))
print("Matrix genomes:", len(matrix))
print("Merged genomes:", len(merged))
print(merged["group"].value_counts())
print("Saved:", out_file)
