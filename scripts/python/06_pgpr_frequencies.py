#!/usr/bin/env python3

import pandas as pd

# INPUT
infile = "05_pgpr_matrix/pgpr_matrix_with_metadata.tsv"

# OUTPUT
outfile = "06_statistics/pgpr_frequencies_by_group.tsv"

df = pd.read_csv(infile, sep="\t")

# identificar columnas KO
ko_cols = [c for c in df.columns if c.startswith("K")]

results = []

for ko in ko_cols:
    for group in ["saline", "non_saline"]:
        subset = df[df["group"] == group]

        total = len(subset)
        present = subset[ko].sum()
        freq = present / total if total > 0 else 0

        results.append({
            "KO": ko,
            "group": group,
            "present": int(present),
            "total": total,
            "frequency": round(freq, 3)
        })

out = pd.DataFrame(results)

out.to_csv(outfile, sep="\t", index=False)

print("Saved:", outfile)
print(out.head(10))
