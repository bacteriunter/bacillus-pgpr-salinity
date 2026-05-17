#!/usr/bin/env python3

import pandas as pd

main = pd.read_csv("05_pgpr_matrix/pgpr_matrix_with_metadata_v2.tsv", sep="\t")
exclude = pd.read_csv("00_metadata/exclude_sensitivity.tsv", sep="\t")

exclude_ids = set(exclude["Assembly Accession"])

sens = main[~main["genome"].isin(exclude_ids)].copy()

sens.to_csv(
    "05_pgpr_matrix/pgpr_matrix_with_metadata_v2_sensitivity.tsv",
    sep="\t",
    index=False
)

print("Main dataset:", len(main))
print("Excluded:", len(exclude_ids))
print("Sensitivity dataset:", len(sens))
print("\nGroup counts:")
print(sens["group"].value_counts())
