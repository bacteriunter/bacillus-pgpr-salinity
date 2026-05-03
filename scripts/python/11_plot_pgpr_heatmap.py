#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

infile = "05_pgpr_matrix/pgpr_matrix_with_metadata.tsv"
outfile = "08_figures/fig3_heatmap/pgpr_presence_absence_heatmap.png"

df = pd.read_csv(infile, sep="\t")

ko_cols = [c for c in df.columns if c.startswith("K")]

df = df.sort_values(["group", "species_clean", "genome"])
matrix = df[ko_cols].values

fig, ax = plt.subplots(figsize=(11, 12))

im = ax.imshow(
    matrix,
    aspect="auto",
    interpolation="nearest",
    cmap="viridis",
    vmin=0,
    vmax=1
)

ax.set_xticks(np.arange(len(ko_cols)))
ax.set_xticklabels(ko_cols, rotation=90, fontsize=8)

ax.set_yticks([])
ax.set_xlabel("KEGG orthologs (PGPR-related)")
ax.set_ylabel(r"$\it{Bacillus}$ genomes")

group_values = df["group"].values
change_idx = np.where(group_values[:-1] != group_values[1:])[0]

for idx in change_idx:
    ax.axhline(idx + 0.5, color="black", linewidth=1)

saline_n = (df["group"] == "saline").sum()
non_n = (df["group"] == "non_saline").sum()

# Group labels inside the heatmap, left side
ax.text(
    0.2,
    saline_n / 2,
    f"Saline (n={saline_n})",
    va="center",
    ha="left",
    fontsize=10,
    bbox=dict(facecolor="white", edgecolor="none", alpha=0.8)
)

ax.text(
    0.2,
    saline_n + non_n / 2,
    f"Non-saline (n={non_n})",
    va="center",
    ha="left",
    fontsize=10,
    bbox=dict(facecolor="white", edgecolor="none", alpha=0.8)
)

cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.04)
cbar.set_label("Presence / Absence")
cbar.set_ticks([0, 1])
cbar.set_ticklabels(["0", "1"])

plt.tight_layout()
plt.savefig(outfile, dpi=600, bbox_inches="tight")

print("Saved:", outfile)
