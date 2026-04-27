#p15_memboundness_vs_speedup.py
import matplotlib.pyplot as plt
from plot_utils import smart_ylim
from config import BENCHMARKS, MODES, COLORS, PLOTS_DIR


def run(data):
    fig, ax = plt.subplots(figsize=(9, 7))
    all_speedups = []

    for i, mode in enumerate(MODES[1:], start=1):
        mem_ratios = [data[b]["none"]["mem_bound_ratio"] * 100 for b in BENCHMARKS]
        speedups   = [data[b][mode]["speedup"]            for b in BENCHMARKS]
        all_speedups.extend(speedups)
        ax.scatter(mem_ratios, speedups, label=mode, color=COLORS[i],
                   s=80, alpha=0.75, edgecolors="black", linewidths=0.5)
        for b, mr, sp in zip(BENCHMARKS, mem_ratios, speedups):
            if sp > 1.005 or sp < 0.985:
                ax.annotate(b, (mr, sp), fontsize=7, alpha=0.85,
                            xytext=(3, 3), textcoords="offset points")

    ax.axhline(1.0, color="red", linestyle="--", linewidth=1, alpha=0.7, label="Sin cambio")
    smart_ylim(ax, all_speedups + [1.0], force_zero=False)

    ax.set_xlabel("Fracción memory-bound (%) — baseline", fontsize=11, fontweight="bold")
    ax.set_ylabel("Speedup real con prefetch", fontsize=11, fontweight="bold")
    ax.set_title("¿Los benchmarks más memory-bound se benefician más del prefetch?",
                 fontweight="bold")
    ax.legend(fontsize=11, loc="upper left", bbox_to_anchor=(1.01, 1), borderaxespad=0)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "15_memboundness_vs_speedup.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  → 15_memboundness_vs_speedup.png")