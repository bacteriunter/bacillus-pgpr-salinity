#!/usr/bin/env python3

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# INPUT
infile = "05_pgpr_matrix/pgpr_matrix_with_metadata.tsv"

# OUTPUT
outfile = "08_figures/fig5_pcoa/pca_coordinates.tsv"

df = pd.read_csv(infile, sep="\t")

# columnas KO
ko_cols = [c for c in df.columns if c.startswith("K")]

X = df[ko_cols].values

# escalar (importante para PCA)
X_scaled = StandardScaler().fit_transform(X)

# PCA
pca = PCA(n_components=2)
coords = pca.fit_transform(X_scaled)

# guardar resultados
out = pd.DataFrame({
    "genome": df["genome"],
    "group": df["group"],
    "PC1": coords[:,0],
    "PC2": coords[:,1]
})

out.to_csv(outfile, sep="\t", index=False)

print("Explained variance:")
print(pca.explained_variance_ratio_)

print("\nSaved:", outfile)
