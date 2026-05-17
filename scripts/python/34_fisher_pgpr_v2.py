#!/usr/bin/env python3

import pandas as pd
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests
from pathlib import Path
import numpy as np

infile = "05_pgpr_matrix/pgpr_matrix_with_metadata_v2.tsv"

outdir = Path("06_statistics/v2")
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "fisher_pgpr_results_v2.tsv"

df = pd.read_csv(infile, sep="\t")

ko_cols = [c for c in df.columns if c.startswith("K")]

rows = []

for ko in ko_cols:
    sal = df[df["group"] == "saline"][ko]
    non = df[df["group"] == "non_saline"][ko]

    a = int(sal.sum())
    b = int(len(sal) - sal.sum())
    c = int(non.sum())
    d = int(len(non) - non.sum())

    table = [[a, b], [c, d]]
    oddsratio, p = fisher_exact(table, alternative="two-sided")

    rows.append({
        "KO": ko,
        "saline_present": a,
        "saline_absent": b,
        "non_saline_present": c,
        "non_saline_absent": d,
        "saline_frequency": a / len(sal),
        "non_saline_frequency": c / len(non),
        "frequency_difference": (a / len(sal)) - (c / len(non)),
        "odds_ratio": oddsratio,
        "p_value": p
    })

res = pd.DataFrame(rows)
res["q_value"] = multipletests(res["p_value"], method="fdr_bh")[1]
res = res.sort_values(["q_value", "p_value"])

res.to_csv(outfile, sep="\t", index=False)

print("KOs tested:", len(res))
print("Nominal p < 0.05:", (res["p_value"] < 0.05).sum())
print("FDR q < 0.05:", (res["q_value"] < 0.05).sum())
print("\nTop results:")
print(res.head(10).to_string(index=False))
print("\nSaved:", outfile)
