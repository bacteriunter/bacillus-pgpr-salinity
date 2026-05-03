#!/usr/bin/env python3

import pandas as pd

# INPUTS
freq = pd.read_csv("06_statistics/pgpr_frequencies_by_group.tsv", sep="\t")
fisher = pd.read_csv("06_statistics/fisher_pgpr_results.tsv", sep="\t")

# separar grupos
sal = freq[freq["group"] == "saline"].rename(columns={
    "present": "saline_present",
    "total": "saline_total",
    "frequency": "saline_freq"
})

non = freq[freq["group"] == "non_saline"].rename(columns={
    "present": "non_present",
    "total": "non_total",
    "frequency": "non_freq"
})

# unir
merged = sal.merge(non, on="KO")

# unir con fisher
final = merged.merge(fisher, on="KO")

# ordenar por p_adj
final = final.sort_values("p_adj")

# redondear
final["saline_freq"] = final["saline_freq"].round(3)
final["non_freq"] = final["non_freq"].round(3)
final["p_value"] = final["p_value"].apply(lambda x: f"{x:.2e}")
final["p_adj"] = final["p_adj"].apply(lambda x: f"{x:.2e}")

# OUTPUT
outfile = "09_tables/main_tables/table_pgpr_summary.tsv"
final.to_csv(outfile, sep="\t", index=False)

print("Saved:", outfile)
print(final.head(10))
