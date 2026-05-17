#!/usr/bin/env python3

import pandas as pd
import numpy as np
from scipy.stats import fisher_exact

df = pd.read_csv("05_pgpr_matrix/pgpr_matrix_with_metadata_v2.tsv", sep="\t")

n_sal = (df["group"] == "saline").sum()
n_non = (df["group"] == "non_saline").sum()

print("Sample sizes:")
print("Saline:", n_sal)
print("Non-saline:", n_non)

effect_sizes = [0.10, 0.15, 0.20, 0.25, 0.30]

baseline = 0.50

print("\nSensitivity analysis (approximate Fisher detectability)")
print("Assuming baseline frequency =", baseline)

for diff in effect_sizes:
    p1 = baseline
    p2 = baseline + diff

    a = round(n_sal * p1)
    b = n_sal - a
    c = round(n_non * p2)
    d = n_non - c

    _, p = fisher_exact([[a, b], [c, d]])

    print(f"Difference {diff:.2f}: p = {p:.5f}")
