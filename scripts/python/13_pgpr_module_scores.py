#!/usr/bin/env python3

import pandas as pd
from scipy.stats import mannwhitneyu

matrix_file = "05_pgpr_matrix/pgpr_matrix_with_metadata.tsv"
module_file = "05_pgpr_matrix/pgpr_ko_modules.tsv"

out_scores = "05_pgpr_matrix/pgpr_module_scores.tsv"
out_stats = "06_statistics/pgpr_module_score_stats.tsv"

df = pd.read_csv(matrix_file, sep="\t")
modules = pd.read_csv(module_file, sep="\t")

results = df[["genome", "Organism Name", "species_clean", "group"]].copy()

stats = []

for module in modules["module"].unique():
    kos = modules[modules["module"] == module]["KO"].tolist()
    kos = [ko for ko in kos if ko in df.columns]

    score_col = module + "_score"
    fraction_col = module + "_fraction"

    results[score_col] = df[kos].sum(axis=1)
    results[fraction_col] = results[score_col] / len(kos)

    sal = results[results["group"] == "saline"][fraction_col]
    non = results[results["group"] == "non_saline"][fraction_col]

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

results.to_csv(out_scores, sep="\t", index=False)
pd.DataFrame(stats).to_csv(out_stats, sep="\t", index=False)

print("Saved:", out_scores)
print("Saved:", out_stats)
print(pd.DataFrame(stats))
