#!/usr/bin/env python3

import pandas as pd

df = pd.read_csv("05_pgpr_matrix/pgpr_matrix_with_metadata_v2.tsv", sep="\t")

species_counts = df.groupby(["species_clean", "group"]).size().unstack(fill_value=0)

shared_species = species_counts[
    (species_counts["saline"] > 0) &
    (species_counts["non_saline"] > 0)
].index

sub = df[df["species_clean"].isin(shared_species)].copy()

sub.to_csv(
    "05_pgpr_matrix/pgpr_matrix_with_metadata_v2_species_matched.tsv",
    sep="\t",
    index=False
)

print("Shared species:", len(shared_species))
print("Subset size:", len(sub))
print("\nGroup counts:")
print(sub["group"].value_counts())
