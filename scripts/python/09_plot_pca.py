#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

# INPUT
infile = "08_figures/fig5_pcoa/pca_coordinates.tsv"

# OUTPUT
outfile = "08_figures/fig5_pcoa/pca_plot.png"

df = pd.read_csv(infile, sep="\t")

# separar grupos
sal = df[df["group"] == "saline"]
non = df[df["group"] == "non_saline"]

plt.figure(figsize=(6,5))

plt.scatter(sal["PC1"], sal["PC2"], label="Saline", alpha=0.7)
plt.scatter(non["PC1"], non["PC2"], label="Non-saline", alpha=0.7)

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.legend()
plt.tight_layout()

plt.savefig(outfile, dpi=600)

print("Saved:", outfile)
