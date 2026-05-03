#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import textwrap

outfile = "08_figures/fig1_workflow/workflow_comparative_genomics.png"

steps = [
    "Genome retrieval\nNCBI RefSeq",
    "Metadata curation\nBioSample fields",
    "Environmental classification\nSaline vs non-saline",
    "Quality filtering\nTaxonomic matching",
    "Proteome extraction\nRefSeq .faa files",
    "PGPR KO selection\n22 targeted KOs",
    "HMM annotation\nhmmsearch",
    "Presence–absence\nmatrix",
    "Statistical analysis\nFisher, PCA, PERMANOVA"
]

# Two-row layout: first 5 steps, second 4 steps
positions = [
    (0, 2), (2.4, 2), (4.8, 2), (7.2, 2), (9.6, 2),
    (9.6, 0.6), (7.2, 0.6), (4.8, 0.6), (2.4, 0.6)
]

fig, ax = plt.subplots(figsize=(14, 5))
ax.axis("off")

box_width = 1.9
box_height = 0.65

def add_box(ax, x, y, text):
    box = FancyBboxPatch(
        (x, y),
        box_width,
        box_height,
        boxstyle="round,pad=0.05,rounding_size=0.06",
        linewidth=1.2,
        facecolor="#f2f2f2",
        edgecolor="black"
    )
    ax.add_patch(box)

    ax.text(
        x + box_width / 2,
        y + box_height / 2,
        text,
        ha="center",
        va="center",
        fontsize=9,
        linespacing=1.15
    )

def add_arrow(ax, start, end):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="->",
        mutation_scale=14,
        linewidth=1.2,
        color="black"
    )
    ax.add_patch(arrow)

# Add boxes
for (x, y), step in zip(positions, steps):
    add_box(ax, x, y, step)

# Arrows top row
for i in range(4):
    x1, y1 = positions[i]
    x2, y2 = positions[i + 1]
    add_arrow(
        ax,
        (x1 + box_width, y1 + box_height / 2),
        (x2, y2 + box_height / 2)
    )

# Down arrow from step 5 to step 6
x1, y1 = positions[4]
x2, y2 = positions[5]
add_arrow(
    ax,
    (x1 + box_width / 2, y1),
    (x2 + box_width / 2, y2 + box_height)
)

# Arrows bottom row, right to left
for i in range(5, 8):
    x1, y1 = positions[i]
    x2, y2 = positions[i + 1]
    add_arrow(
        ax,
        (x1, y1 + box_height / 2),
        (x2 + box_width, y2 + box_height / 2)
    )

ax.set_xlim(-0.3, 12)
ax.set_ylim(0.1, 3.0)

plt.tight_layout()
plt.savefig(outfile, dpi=600, bbox_inches="tight")
print(f"Saved: {outfile}")
