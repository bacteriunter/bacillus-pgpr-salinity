#!/usr/bin/env python3

import pandas as pd
from pathlib import Path

OUTDIR = Path("09_tables/supplementary")
OUTDIR.mkdir(parents=True, exist_ok=True)

# TS1: Genome metadata
meta = pd.read_csv("05_pgpr_matrix/pgpr_matrix_with_metadata_v2.tsv", sep="\t")
meta_cols = [
    "genome",
    "Organism Name",
    "species_clean",
    "group",
    "Assembly BioSample Isolation source",
    "Assembly BioSample Geographic location"
]
meta_cols = [c for c in meta_cols if c in meta.columns]
meta[meta_cols].drop_duplicates().to_csv(
    OUTDIR / "TS1_genome_metadata.tsv",
    sep="\t",
    index=False
)

# TS2: Fisher exact test results
fisher = pd.read_csv("06_statistics/v2/fisher_pgpr_results_v2.tsv", sep="\t")
fisher.to_csv(
    OUTDIR / "TS2_fisher_pgpr_all_markers.tsv",
    sep="\t",
    index=False
)

# TS3: Functional module statistics
mods = pd.read_csv("06_statistics/v2/pgpr_module_score_stats_v2_final.tsv", sep="\t")
mods.to_csv(
    OUTDIR / "TS3_pgpr_module_statistics.tsv",
    sep="\t",
    index=False
)

# TS4: Robustness summary
def read_result(path):
    df = pd.read_csv(path, sep="\t", index_col=0)
    return df.iloc[:, 0]

main_perm = read_result("06_statistics/v2/permanova_jaccard_pgpr_v2.tsv")
main_disp = read_result("06_statistics/v2/permdisp_jaccard_pgpr_v2.tsv")

sens_perm = read_result("06_statistics/v2_sensitivity/permanova_jaccard_pgpr_v2_sensitivity.tsv")
sens_disp = read_result("06_statistics/v2_sensitivity/permdisp_jaccard_pgpr_v2_sensitivity.tsv")

sp_perm = read_result("06_statistics/v2_species_matched/permanova_jaccard_pgpr_v2_species_matched.tsv")
sp_disp = read_result("06_statistics/v2_species_matched/permdisp_jaccard_pgpr_v2_species_matched.tsv")

ts4 = pd.DataFrame([
    {
        "analysis": "main",
        "n_saline": 54,
        "n_non_saline": 46,
        "pseudo_F": float(main_perm["test statistic"]),
        "permanova_p": float(main_perm["p-value"]),
        "permdisp_F": float(main_disp["test statistic"]),
        "permdisp_p": float(main_disp["p-value"])
    },
    {
        "analysis": "sensitivity",
        "n_saline": 52,
        "n_non_saline": 46,
        "pseudo_F": float(sens_perm["test statistic"]),
        "permanova_p": float(sens_perm["p-value"]),
        "permdisp_F": float(sens_disp["test statistic"]),
        "permdisp_p": float(sens_disp["p-value"])
    },
    {
        "analysis": "species_matched",
        "n_saline": 46,
        "n_non_saline": 46,
        "pseudo_F": float(sp_perm["test statistic"]),
        "permanova_p": float(sp_perm["p-value"]),
        "permdisp_F": float(sp_disp["test statistic"]),
        "permdisp_p": float(sp_disp["p-value"])
    }
])

ts4.to_csv(
    OUTDIR / "TS4_robustness_summary.tsv",
    sep="\t",
    index=False
)

# TS5: PGPR marker panel
panel = pd.read_csv("05_pgpr_matrix/pgpr_ko_modules_v2_final.tsv", sep="\t")
panel.to_csv(
    OUTDIR / "TS5_pgpr_marker_panel.tsv",
    sep="\t",
    index=False
)

print("Generated supplementary tables:")
for table in sorted(OUTDIR.glob("TS*.tsv")):
    print("-", table)
