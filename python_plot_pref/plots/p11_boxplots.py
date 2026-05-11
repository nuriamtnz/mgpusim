#p11_boxplots.py
import matplotlib.pyplot as plt
from plot_utils import smart_ylim, top_right_legend
from config import BENCHMARKS, MODES, COLORS, PLOTS_DIR, REF_LINE_COLOR


def run(data):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    metrics = [
        (axes[0, 0], "speedup",              "Speedup (ratio)",  True,  False),
        (axes[0, 1], "precision_pct",        "Precisión (%)",    False, True),
        (axes[1, 0], "coverage_pct",         "Cobertura (%)",    False, True),
        (axes[1, 1], "traffic_overhead_pct", "Overhead (%)",     False, True),
    ]
    for ax, key, ylabel, add_hline, force_zero in metrics:
        box_data   = [[data[b][m][key] for b in BENCHMARKS] for m in MODES[1:]]
        all_values = [v for series in box_data for v in series]
        bp = ax.boxplot(box_data, labels=MODES[1:], patch_artist=True)
        for patch, color in zip(bp["boxes"], COLORS[1:]):
            patch.set_facecolor(color)
        if add_hline:
            ax.axhline(1.0, color=REF_LINE_COLOR, linestyle="--",
                       linewidth=1.2, alpha=0.85, label="Baseline")
            top_right_legend(ax, fontsize=10)
        smart_ylim(ax, all_values, force_zero=force_zero)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.tick_params(axis="x", labelsize=11)
        ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "11_boxplots.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  → 11_boxplots.png")