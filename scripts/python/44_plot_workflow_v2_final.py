#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

outdir = Path("08_figures/fig1_workflow_v2_final")
outdir.mkdir(parents=True, exist_ok=True)

out_png = outdir / "workflow_pgpr_comparative_genomics_v2_final.png"
out_pdf = outdir / "workflow_pgpr_comparative_genomics_v2_final.pdf"

fig, ax = plt.subplots(figsize=(15.5, 6.2))
ax.set_xlim(0, 15.5)
ax.set_ylim(0, 6.2)
ax.axis("off")

box_w = 2.05
box_h = 0.9
fs = 7.8

boxes = [
    ("Genome retrieval\nNCBI RefSeq", 0.3, 4.25),
    ("Metadata curation\nBioSample fields", 2.8, 4.25),
    ("Environmental classification\nSaline vs non-saline", 5.3, 4.25),
    ("Quality filtering\nAssembly quality\nPathogen exclusion", 7.8, 4.25),
    ("Proteome extraction\nRefSeq .faa files", 10.3, 4.25),
    ("PGPR KO panel\n41 screened\n36 retained", 12.8, 4.25),
    ("Targeted HMM annotation\nHMMER hmmsearch\nKOfam thresholds", 12.8, 1.75),
    ("Presence–absence matrix\nBinary marker profiles", 10.3, 1.75),
    ("Functional summaries\nMarker frequencies\nModule scores", 7.8, 1.75),
    ("Multivariate analyses\nJaccard PCoA\nPERMANOVA / PERMDISP", 5.3, 1.75),
    ("Robustness analyses\nSensitivity filtering\nSpecies-matched control\nDetectability assessment", 2.8, 1.75),
    ("Final outputs\nFigures, statistics\nGitHub + Zenodo", 0.3, 1.75),
]

def add_box(text, x, y):
    patch = FancyBboxPatch(
        (x, y), box_w, box_h,
        boxstyle="round,pad=0.04,rounding_size=0.06",
        linewidth=1.2,
        edgecolor="black",
        facecolor="#f2f2f2"
    )
    ax.add_patch(patch)
    ax.text(
        x + box_w / 2,
        y + box_h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fs,
        linespacing=1.05
    )

def add_arrow(x1, y1, x2, y2):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="->",
            mutation_scale=12,
            linewidth=1.1,
            color="black"
        )
    )

for text, x, y in boxes:
    add_box(text, x, y)

# Top row arrows
for i in range(5):
    _, x1, y1 = boxes[i]
    _, x2, y2 = boxes[i + 1]
    add_arrow(x1 + box_w, y1 + box_h / 2, x2, y2 + box_h / 2)

# Down arrow
add_arrow(
    boxes[5][1] + box_w / 2,
    boxes[5][2],
    boxes[6][1] + box_w / 2,
    boxes[6][2] + box_h
)

# Bottom row arrows right to left
for i in range(6, 11):
    _, x1, y1 = boxes[i]
    _, x2, y2 = boxes[i + 1]
    add_arrow(x1, y1 + box_h / 2, x2 + box_w, y2 + box_h / 2)

ax.text(
    7.75,
    5.85,
    "Comparative genomic workflow for PGPR-associated traits in Bacillus",
    ha="center",
    va="center",
    fontsize=13,
    fontweight="bold"
)

plt.tight_layout()
plt.savefig(out_png, dpi=600, bbox_inches="tight")
plt.savefig(out_pdf, bbox_inches="tight")

print("Saved:", out_png)
print("Saved:", out_pdf)
