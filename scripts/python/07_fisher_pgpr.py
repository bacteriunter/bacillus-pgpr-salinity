#!/usr/bin/env python3

import pandas as pd
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests

# INPUT
infile = "05_pgpr_matrix/pgpr_matrix_with_metadata.tsv"

# OUTPUT
outfile = "06_statistics/fisher_pgpr_results.tsv"

df = pd.read_csv(infile, sep="\t")

ko_cols = [c for c in df.columns if c.startswith("K")]

results = []

for ko in ko_cols:
    sal = df[df["group"] == "saline"]
    non = df[df["group"] == "non_saline"]

    a = sal[ko].sum()
    b = len(sal) - a

    c = non[ko].sum()
    d = len(non) - c

    table = [[a, b], [c, d]]

    oddsratio, p = fisher_exact(table)

    results.append({
        "KO": ko,
        "saline_present": int(a),
        "saline_absent": int(b),
        "non_present": int(c),
        "non_absent": int(d),
        "odds_ratio": oddsratio,
        "p_value": p
    })

res = pd.DataFrame(results)

# corrección FDR
res["p_adj"] = multipletests(res["p_value"], method="fdr_bh")[1]

res.to_csv(outfile, sep="\t", index=False)

print("Saved:", outfile)
print(res.sort_values("p_adj").head(10))
