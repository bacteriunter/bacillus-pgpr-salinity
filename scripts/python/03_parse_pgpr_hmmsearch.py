#!/usr/bin/env python3

from pathlib import Path
import pandas as pd
import sys

if len(sys.argv) != 3:
    print("Usage: python 03_parse_pgpr_hmmsearch.py input.tbl output.tsv")
    sys.exit(1)

infile = Path(sys.argv[1])
outfile = Path(sys.argv[2])

rows = []

with open(infile) as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue

        parts = line.strip().split()
        target = parts[0]
        ko = parts[2]
        evalue = float(parts[4])
        score = float(parts[5])

        if evalue <= 1e-10:
            rows.append({
                "protein_id": target,
                "ko": ko,
                "evalue": evalue,
                "score": score
            })

df = pd.DataFrame(rows)

if not df.empty:
    df = df.sort_values(["ko", "score"], ascending=[True, False])
    df = df.drop_duplicates(subset=["ko"], keep="first")

df.to_csv(outfile, sep="\t", index=False)

print(f"Input: {infile}")
print(f"Filtered hits: {len(df)}")
print(f"Saved: {outfile}")
