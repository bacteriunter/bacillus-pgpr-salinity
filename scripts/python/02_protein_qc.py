#!/usr/bin/env python3

from pathlib import Path
import pandas as pd

# INPUT
faa_dir = Path("01_downloads/proteomes_faa")

# OUTPUT
out_file = Path("02_quality_control/protein_counts/protein_counts.tsv")

rows = []

for faa in sorted(faa_dir.glob("*.faa")):
    acc = faa.stem
    nseq = 0
    aa_total = 0
    lengths = []

    with open(faa) as f:
        seq = ""
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq:
                    lengths.append(len(seq))
                    aa_total += len(seq)
                nseq += 1
                seq = ""
            else:
                seq += line

        # última secuencia
        if seq:
            lengths.append(len(seq))
            aa_total += len(seq)

    rows.append({
        "accession": acc,
        "protein_count": nseq,
        "total_aa": aa_total,
        "mean_length": round(sum(lengths)/len(lengths), 2) if lengths else 0
    })

# dataframe
df = pd.DataFrame(rows)

# guardar
out_file.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out_file, sep="\t", index=False)

# resumen
print("\n=== Protein QC summary ===")
print(df.describe())
print(f"\nSaved: {out_file}")
