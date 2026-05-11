#p13_theoretical_vs_real.py
import numpy as np
import matplotlib.pyplot as plt
from plot_utils import smart_ylim, top_right_legend
from config import BENCHMARKS, MODES, PALETTE, PLOTS_DIR, REF_LINE_COLOR


def run(data):
    fig, ax = plt.subplots(figsize=(max(14, len(BENCHMARKS) * 0.85), 6))
    x     = np.arange(len(BENCHMARKS))
    width = 0.3

    theoretical = [min(data[b]["none"]["max_theoretical_speedup"], 3.0) for b in BENCHMARKS]
    best_real   = [max(data[b][m]["speedup"] for m in MODES[1:])        for b in BENCHMARKS]
    all_vals    = theoretical + best_real + [1.0]

    ax.bar(x - width / 2, theoretical, width,
           label="Speedup teórico máximo (Ley de Amdahl)",
           color=PALETTE[1], alpha=0.85, edgecolor="black", linewidth=0.5)
    ax.bar(x + width / 2, best_real, width,
           label="Mejor speedup real (mejor modo)",
           color=PALETTE[0], alpha=0.85, edgecolor="black", linewidth=0.5)
    ax.axhline(y=1.0, color=REF_LINE_COLOR, linestyle="--", linewidth=1.2,
               alpha=0.85, label="Baseline")

    smart_ylim(ax, all_vals, force_zero=False)
    ax.set_ylabel("Speedup (ratio)", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(BENCHMARKS, rotation=90, fontsize=8)
    top_right_legend(ax, fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "13_theoretical_vs_real_speedup.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  → 13_theoretical_vs_real_speedup.png")