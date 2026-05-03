#!/usr/bin/env python3

import pandas as pd
from skbio.stats.distance import permanova
from skbio.stats.distance import DistanceMatrix
from scipy.spatial.distance import pdist, squareform

infile = "05_pgpr_matrix/pgpr_matrix_with_metadata.tsv"

df = pd.read_csv(infile, sep="\t")

ko_cols = [c for c in df.columns if c.startswith("K")]

X = df[ko_cols].values
ids = df["genome"].astype(str).tolist()

dist = pdist(X, metric="jaccard")
dist_matrix = DistanceMatrix(squareform(dist), ids=ids)

metadata = df[["genome", "group"]].copy()
metadata["genome"] = metadata["genome"].astype(str)
metadata = metadata.set_index("genome")

res = permanova(
    dist_matrix,
    metadata,
    column="group",
    permutations=999
)

print(res)
