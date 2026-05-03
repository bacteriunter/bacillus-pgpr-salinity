import pandas as pd
import re
from pathlib import Path

infile = Path("00_metadata/bacillus_refseq_metadata.tsv")
outfile = Path("00_metadata/bacillus_saline_candidate_classification.tsv")

df = pd.read_csv(infile, sep="\t", dtype=str).fillna("")

saline_terms = [
    "saline", "salinity", "salt", "sodic", "soda", "saline-alkali",
    "saline alkaline", "alkaline-saline", "hypersaline", "halophilic",
    "halotolerant", "saltern", "brine", "salt lake", "salt marsh",
    "salt pan", "coastal", "marine sediment", "mangrove", "halophyte",
    "seawater", "sea water"
]

exclude_terms = [
    "human", "clinical", "blood", "wound", "feces", "faeces",
    "urine", "hospital", "patient", "food", "milk", "cheese",
    "fermentation", "industrial", "mutant", "laboratory"
]

def norm(x):
    return re.sub(r"\s+", " ", str(x).lower())

def classify(row):
    text = norm(" ".join(row.astype(str).tolist()))

    saline_hits = [t for t in saline_terms if t in text]
    exclude_hits = [t for t in exclude_terms if t in text]

    if exclude_hits:
        return pd.Series(["exclude_review", ";".join(exclude_hits)])
    if saline_hits:
        return pd.Series(["saline_candidate", ";".join(saline_hits)])

    if any(t in text for t in ["soil", "rhizosphere", "root", "plant"]):
        return pd.Series(["non_saline_candidate", ""])

    return pd.Series(["uncertain", ""])

df[["candidate_group", "keyword_hits"]] = df.apply(classify, axis=1)

df.to_csv(outfile, sep="\t", index=False)

print("Saved:", outfile)
print(df["candidate_group"].value_counts())
