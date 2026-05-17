#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

matrix_file = "05_pgpr_matrix/pgpr_matrix_with_metadata_v2.tsv"
module_file = "05_pgpr_matrix/pgpr_ko_modules_v2_final.tsv"

outdir = Path("08_figures/fig2_heatmap_v2_final")
outdir.mkdir(parents=True, exist_ok=True)

out_png = outdir / "pgpr_presence_absence_heatmap_v2_final.png"
out_pdf = outdir / "pgpr_presence_absence_heatmap_v2_final.pdf"

df = pd.read_csv(matrix_file, sep="\t")
modules = pd.read_csv(module_file, sep="\t")

# Keep KO order according to module file
ko_cols = [ko for ko in modules["KO"].tolist() if ko in df.columns]

# Sort genomes by group, species, genome
df = df.sort_values(["group", "species_clean", "genome"]).reset_index(drop=True)
matrix = df[ko_cols].values

fig, ax = plt.subplots(figsize=(13, 12))

im = ax.imshow(
    matrix,
    aspect="auto",
    interpolation="nearest",
    cmap="binary",
    vmin=0,
    vmax=1
)

ax.set_xticks(np.arange(len(ko_cols)))

# Use gene names if available; otherwise KO
ko_to_gene = dict(zip(modules["KO"], modules["gene"]))
xlabels = [ko_to_gene.get(ko, ko) for ko in ko_cols]

ax.set_xticklabels(xlabels, rotation=90, fontsize=7)
ax.set_yticks([])

ax.set_xlabel("PGPR-associated KEGG orthologs")
ax.set_ylabel(r"$\it{Bacillus}$ genomes")

# Horizontal group separator
group_values = df["group"].values
change_idx = np.where(group_values[:-1] != group_values[1:])[0]

for idx in change_idx:
    ax.axhline(idx + 0.5, color="black", linewidth=1.2)

saline_n = (df["group"] == "saline").sum()
non_n = (df["group"] == "non_saline").sum()

ax.text(
    -0.4,
    saline_n / 2,
    f"Saline-associated\n(n={saline_n})",
    va="center",
    ha="right",
    fontsize=10
)

ax.text(
    -0.4,
    saline_n + non_n / 2,
    f"Non-saline\n(n={non_n})",
    va="center",
    ha="right",
    fontsize=10
)

# Module separators and labels
module_bounds = []
start = 0

for module, sub in modules.groupby("module", sort=False):
    kos = [ko for ko in sub["KO"].tolist() if ko in ko_cols]
    if not kos:
        continue

    idxs = [ko_cols.index(ko) for ko in kos]
    module_bounds.append((min(idxs), max(idxs), module))

for i, (start, end, module) in enumerate(module_bounds):
    if i < len(module_bounds) - 1:
        ax.axvline(end + 0.5, color="black", linewidth=1.0)

module_labels = {
    "phosphorus_acquisition": "Phosphorus",
    "iron_acquisition": "Iron",
    "nitrogen_assimilation": "Nitrogen",
    "colonization_motility": "Colonization/\nmotility",
    "voc_isr": "VOC\nmarker",
    "biocontrol": "Biocontrol"
}

for start, end, module in module_bounds:
    ax.text(
        (start + end) / 2,
        -4.5,
        module_labels.get(module, module),
        ha="center",
        va="bottom",
        fontsize=9
    )

cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.03)
cbar.set_label("Presence / Absence")
cbar.set_ticks([0, 1])
cbar.set_ticklabels(["Absent", "Present"])

plt.tight_layout()

plt.savefig(out_png, dpi=600, bbox_inches="tight")
plt.savefig(out_pdf, bbox_inches="tight")

print("Saved:", out_png)
print("Saved:", out_pdf)
print("KOs plotted:", len(ko_cols))
print("Genomes plotted:", len(df))
