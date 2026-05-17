#!/usr/bin/env python3

import pandas as pd
from scipy.spatial.distance import pdist, squareform
from skbio.stats.distance import DistanceMatrix, permanova, permdisp
from pathlib import Path

infile = "05_pgpr_matrix/pgpr_matrix_with_metadata_v2_species_matched.tsv"

outdir = Path("06_statistics/v2_species_matched")
outdir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(infile, sep="\t")

ko_cols = [c for c in df.columns if c.startswith("K")]
X = df[ko_cols].values
ids = df["genome"].astype(str).tolist()

dist = pdist(X, metric="jaccard")
dm = DistanceMatrix(squareform(dist), ids=ids)

metadata = df[["genome", "group"]].copy()
metadata["genome"] = metadata["genome"].astype(str)
metadata = metadata.set_index("genome")

permanova_res = permanova(
    dm,
    metadata,
    column="group",
    permutations=999
)

permdisp_res = permdisp(
    dm,
    metadata,
    column="group",
    permutations=999
)

out_permanova = outdir / "permanova_jaccard_pgpr_v2_species_matched.tsv"
out_permdisp = outdir / "permdisp_jaccard_pgpr_v2_species_matched.tsv"

pd.DataFrame(permanova_res).to_csv(out_permanova, sep="\t")
pd.DataFrame(permdisp_res).to_csv(out_permdisp, sep="\t")

print("PERMANOVA")
print(permanova_res)

print("\nPERMDISP")
print(permdisp_res)

print("\nSaved:", out_permanova)
print("Saved:", out_permdisp)
