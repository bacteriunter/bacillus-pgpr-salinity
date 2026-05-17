#!/usr/bin/env python3

import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from pathlib import Path

infile = "05_pgpr_matrix/pgpr_matrix_with_metadata_v2.tsv"

outdir = Path("08_figures/fig5_pcoa_v2")
outdir.mkdir(parents=True, exist_ok=True)

outfile = outdir / "pcoa_jaccard_coordinates_v2.tsv"
eigfile = outdir / "pcoa_jaccard_eigenvalues_v2.tsv"

df = pd.read_csv(infile, sep="\t")

ko_cols = [c for c in df.columns if c.startswith("K")]
X = df[ko_cols].values

D = squareform(pdist(X, metric="jaccard"))

n = D.shape[0]
J = np.eye(n) - np.ones((n, n)) / n
B = -0.5 * J @ (D ** 2) @ J

eigvals, eigvecs = np.linalg.eigh(B)

idx = np.argsort(eigvals)[::-1]
eigvals = eigvals[idx]
eigvecs = eigvecs[:, idx]

positive = eigvals > 0
eigvals = eigvals[positive]
eigvecs = eigvecs[:, positive]

coords = eigvecs[:, :2] * np.sqrt(eigvals[:2])
variance = eigvals / eigvals.sum()

out = pd.DataFrame({
    "genome": df["genome"],
    "group": df["group"],
    "Axis1": coords[:, 0],
    "Axis2": coords[:, 1]
})

eig = pd.DataFrame({
    "Axis": [f"Axis{i+1}" for i in range(len(eigvals))],
    "Eigenvalue": eigvals,
    "Variance_explained": variance
})

out.to_csv(outfile, sep="\t", index=False)
eig.to_csv(eigfile, sep="\t", index=False)

print("Genomes:", df.shape[0])
print("KOs:", len(ko_cols))
print("Axis1 variance:", round(variance[0]*100, 2))
print("Axis2 variance:", round(variance[1]*100, 2))
print("Saved:", outfile)
