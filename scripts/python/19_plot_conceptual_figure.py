#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

outfile = "08_figures/fig6_conceptual_model/conceptual_model.png"

fig, ax = plt.subplots(figsize=(6, 8))
ax.axis("off")

# =========================
# FUNCTIONS
# =========================
def draw_box(x, y, w, h, text):
    rect = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.04,rounding_size=0.06",
        linewidth=1.2,
        edgecolor="black",
        facecolor="#f7f7f7"
    )
    ax.add_patch(rect)

    ax.text(
        x + w/2,
        y + h/2,
        text,
        ha="center",
        va="center",
        fontsize=10,
        wrap=True
    )


def draw_arrow(x1, y1, x2, y2):
    arr = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="->",
        mutation_scale=12,
        linewidth=1.2,
        color="black"
    )
    ax.add_patch(arr)


# =========================
# LAYOUT (TOP → DOWN)
# =========================

w = 3.5
h = 0.9
x = 1.25

y_positions = [
    6.5,  # Bacillus
    5.2,  # PGPR
    3.8,  # Core
    2.4,  # Variable
    1.2,  # No structuring
    0.0   # Regulation
]

texts = [
    "Bacillus genomes",
    "PGPR functional traits",
    "Conserved functional core\n(phytohormone, colonization)",
    "Variable traits\n(nutrient acquisition)",
    "No salinity-driven structuring",
    "Regulation and\ncontext-dependent effects"
]

# Draw boxes
for y, text in zip(y_positions, texts):
    draw_box(x, y, w, h, text)

# Draw arrows (correct direction ↓)
for i in range(len(y_positions) - 1):
    y_top = y_positions[i] - 0.05
    y_bottom = y_positions[i+1] + h + 0.05

    draw_arrow(
        x + w/2,
        y_top,
        x + w/2,
        y_bottom
    )

# =========================
# LIMITS (CRITICAL FIX)
# =========================
ax.set_xlim(0, 6)
ax.set_ylim(-0.5, 7.8)

plt.tight_layout()
plt.savefig(outfile, dpi=600, bbox_inches="tight")

print("Saved:", outfile)
