#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

stats_file = "06_statistics/v2/pgpr_module_score_stats_v2_final.tsv"

outdir = Path("08_figures/fig4_module_summary_v2_final")
outdir.mkdir(parents=True, exist_ok=True)

out_png = outdir / "pgpr_module_summary_heatmap_v2_final.png"
out_pdf = outdir / "pgpr_module_summary_heatmap_v2_final.pdf"

df = pd.read_csv(stats_file, sep="\t")

order = [
    "phosphorus_acquisition",
    "iron_acquisition",
    "nitrogen_assimilation",
    "colonization_motility",
    "voc_isr",
    "biocontrol"
]

labels = {
    "phosphorus_acquisition": "Phosphorus\nacquisition",
    "iron_acquisition": "Iron\nacquisition",
    "nitrogen_assimilation": "Nitrogen\nassimilation",
    "colonization_motility": "Colonization /\nmotility",
    "voc_isr": "VOC-associated\nmarker",
    "biocontrol": "Biocontrol"
}

df = df.set_index("module").loc[order].reset_index()

means = np.column_stack([
    df["saline_mean_fraction"].values,
    df["non_saline_mean_fraction"].values
])

delta = (
    df["saline_mean_fraction"].values -
    df["non_saline_mean_fraction"].values
).reshape(-1, 1)

fig, (ax1, ax2) = plt.subplots(
    1, 2,
    figsize=(8.2, 5.4),
    gridspec_kw={"width_ratios": [2, 1]}
)

im1 = ax1.imshow(
    means,
    aspect="auto",
    interpolation="nearest",
    vmin=0,
    vmax=1
)

im2 = ax2.imshow(
    delta,
    aspect="auto",
    interpolation="nearest",
    vmin=-0.15,
    vmax=0.15,
    cmap="coolwarm"
)

ax1.set_xticks([0, 1])
ax1.set_xticklabels(["Saline-\nassociated", "Non-\nsaline"], fontsize=10)

ax2.set_xticks([0])
ax2.set_xticklabels(["Δ\nS - NS"], fontsize=10)

ax1.set_yticks(np.arange(len(df)))
ax1.set_yticklabels([labels[m] for m in df["module"]], fontsize=10)

ax2.set_yticks(np.arange(len(df)))
ax2.set_yticklabels([])

for i in range(len(df)):
    for j in range(2):
        ax1.text(
            j, i,
            f"{means[i, j]:.2f}",
            ha="center",
            va="center",
            fontsize=9
        )

    ax2.text(
        0, i,
        f"{delta[i, 0]:.2f}",
        ha="center",
        va="center",
        fontsize=9
    )

cbar1 = fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
cbar1.set_label("Mean module fraction")

cbar2 = fig.colorbar(im2, ax=ax2, fraction=0.08, pad=0.08)
cbar2.set_label("Difference")

fig.suptitle(
    "Comparative representation of PGPR functional modules",
    fontsize=14
)

plt.tight_layout(rect=[0, 0, 1, 0.96])

plt.savefig(out_png, dpi=600, bbox_inches="tight")
plt.savefig(out_pdf, bbox_inches="tight")

print("Saved:", out_png)
print("Saved:", out_pdf)
