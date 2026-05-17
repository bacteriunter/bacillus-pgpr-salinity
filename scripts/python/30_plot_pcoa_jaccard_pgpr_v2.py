#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

coord_file = Path("08_figures/fig5_pcoa_v2/pcoa_jaccard_coordinates_v2.tsv")
eig_file = Path("08_figures/fig5_pcoa_v2/pcoa_jaccard_eigenvalues_v2.tsv")

out_png = Path("08_figures/fig5_pcoa_v2/pcoa_jaccard_plot_v2.png")
out_pdf = Path("08_figures/fig5_pcoa_v2/pcoa_jaccard_plot_v2.pdf")

df = pd.read_csv(coord_file, sep="\t")
eig = pd.read_csv(eig_file, sep="\t")

axis1 = eig.loc[eig["Axis"] == "Axis1", "Variance_explained"].iloc[0] * 100
axis2 = eig.loc[eig["Axis"] == "Axis2", "Variance_explained"].iloc[0] * 100

jitter = 0.002
df["Axis1_j"] = df["Axis1"] + np.random.normal(0, jitter, len(df))
df["Axis2_j"] = df["Axis2"] + np.random.normal(0, jitter, len(df))

sal = df[df["group"] == "saline"]
non = df[df["group"] == "non_saline"]

plt.figure(figsize=(7, 6))

plt.scatter(
    sal["Axis1_j"], sal["Axis2_j"],
    label="Saline-associated",
    alpha=0.70,
    s=55,
    marker="o",
    edgecolors="black",
    linewidths=0.3
)

plt.scatter(
    non["Axis1_j"], non["Axis2_j"],
    label="Non-saline",
    alpha=0.70,
    s=60,
    marker="^",
    edgecolors="black",
    linewidths=0.3
)

plt.axhline(0, linewidth=0.8, linestyle="--", alpha=0.4)
plt.axvline(0, linewidth=0.8, linestyle="--", alpha=0.4)

plt.xlabel(f"PCoA1 ({axis1:.1f}%)")
plt.ylabel(f"PCoA2 ({axis2:.1f}%)")
plt.legend(frameon=False)
plt.tight_layout()

plt.savefig(out_png, dpi=600)
plt.savefig(out_pdf)

print("Saved:", out_png)
print("Saved:", out_pdf)
