#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

# INPUT
infile = "05_pgpr_matrix/pgpr_module_scores.tsv"

# OUTPUT
outfile = "08_figures/fig4_module_scores/pgpr_module_scores_boxplot.png"

df = pd.read_csv(infile, sep="\t")

modules = [
    ("phytohormone_stress_fraction", "Phytohormone/\nstress"),
    ("nutrient_acquisition_fraction", "Nutrient\nacquisition"),
    ("colonization_persistence_fraction", "Colonization/\npersistence")
]

colors = {
    "saline": "#1f77b4",
    "non_saline": "#ff7f0e"
}

fig, ax = plt.subplots(figsize=(7, 5))

data = []
positions = []
module_centers = []

pos = 1.0

for col, label in modules:
    saline = df[df["group"] == "saline"][col]
    non = df[df["group"] == "non_saline"][col]

    data.extend([saline, non])
    positions.extend([pos, pos + 0.35])
    module_centers.append(pos + 0.175)

    pos += 1.3

# Boxplots
ax.boxplot(
    data,
    positions=positions,
    widths=0.28,
    patch_artist=False,
    showfliers=False
)

# Individual points with fixed colors
i = 0
for col, label in modules:
    saline = df[df["group"] == "saline"][col]
    non = df[df["group"] == "non_saline"][col]

    ax.scatter(
        [positions[i]] * len(saline),
        saline,
        color=colors["saline"],
        alpha=0.6,
        s=20,
        edgecolors="none"
    )

    ax.scatter(
        [positions[i + 1]] * len(non),
        non,
        color=colors["non_saline"],
        alpha=0.6,
        s=20,
        edgecolors="none"
    )

    i += 2

# Axis labels
ax.set_xticks(module_centers)
ax.set_xticklabels([m[1] for m in modules])
ax.set_ylabel("Module fraction")
ax.set_ylim(-0.05, 1.05)

# Legend
ax.scatter([], [], color=colors["saline"], label="Saline")
ax.scatter([], [], color=colors["non_saline"], label="Non-saline")
ax.legend(frameon=False, loc="lower left")

plt.tight_layout()
plt.savefig(outfile, dpi=600, bbox_inches="tight")

print("Saved:", outfile)
