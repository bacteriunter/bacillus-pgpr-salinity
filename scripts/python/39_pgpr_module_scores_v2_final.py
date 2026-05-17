#!/usr/bin/env python3

import pandas as pd
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests
from pathlib import Path

matrix_file = "05_pgpr_matrix/pgpr_matrix_with_metadata_v2.tsv"
module_file = "05_pgpr_matrix/pgpr_ko_modules_v2_final.tsv"

outdir = Path("06_statistics/v2")
outdir.mkdir(parents=True, exist_ok=True)

out_scores = "05_pgpr_matrix/pgpr_module_scores_v2_final.tsv"
out_stats = outdir / "pgpr_module_score_stats_v2_final.tsv"

df = pd.read_csv(matrix_file, sep="\t")
modules = pd.read_csv(module_file, sep="\t")

results = df[["genome", "Organism Name", "species_clean", "group"]].copy()

stats = []

for module in modules["module"].unique():
    kos = modules.loc[modules["module"] == module, "KO"].tolist()

    score_col = module + "_score"
    frac_col = module + "_fraction"

    results[score_col] = df[kos].sum(axis=1)
    results[frac_col] = results[score_col] / len(kos)

    sal = results.loc[results["group"] == "saline", frac_col]
    non = results.loc[results["group"] == "non_saline", frac_col]

    stat, p = mannwhitneyu(sal, non, alternative="two-sided")

    stats.append({
        "module": module,
        "n_kos": len(kos),
        "saline_mean_fraction": sal.mean(),
        "non_saline_mean_fraction": non.mean(),
        "saline_median_fraction": sal.median(),
        "non_saline_median_fraction": non.median(),
        "mannwhitney_U": stat,
        "p_value": p
    })

stats_df = pd.DataFrame(stats)
stats_df["q_value"] = multipletests(stats_df["p_value"], method="fdr_bh")[1]
stats_df = stats_df.sort_values("q_value")

results.to_csv(out_scores, sep="\t", index=False)
stats_df.to_csv(out_stats, sep="\t", index=False)

print(stats_df.to_string(index=False))
