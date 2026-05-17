#!/usr/bin/env python3
"""
Parse hmmsearch tblout files using KOfam KO-specific score thresholds.

This parser is stricter and more reproducible than using a single global
E-value cutoff. For each KO, hits are retained only when their full-sequence
score is equal to or higher than the threshold reported in ko_list.
"""

from pathlib import Path
import pandas as pd
import sys

if len(sys.argv) != 3:
    print("Usage: python 26_parse_pgpr_hmmsearch_kofam_thresholds_v2.py input.tbl output.tsv")
    sys.exit(1)

infile = Path(sys.argv[1])
outfile = Path(sys.argv[2])

ko_list_file = Path("04_functional_annotation/kofamscan/db/ko_list")

ko = pd.read_csv(ko_list_file, sep="\t")
thresholds = dict(zip(ko["knum"], ko["threshold"]))

rows = []

with open(infile) as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue

        parts = line.strip().split()
        target = parts[0]
        hmm_name = parts[2]
        evalue = float(parts[4])
        score = float(parts[5])

        if hmm_name not in thresholds:
            continue

        threshold = float(thresholds[hmm_name])

        if score >= threshold:
            rows.append({
                "protein_id": target,
                "ko": hmm_name,
                "evalue": evalue,
                "score": score,
                "threshold": threshold,
                "score_minus_threshold": score - threshold
            })

df = pd.DataFrame(rows)

if not df.empty:
    df = df.sort_values(["ko", "score"], ascending=[True, False])
    df = df.drop_duplicates(subset=["ko"], keep="first")

outfile.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(outfile, sep="\t", index=False)

print(f"Input: {infile}")
print(f"Filtered hits: {len(df)}")
print(f"Saved: {outfile}")
