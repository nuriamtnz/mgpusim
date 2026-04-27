# 10_precision_vs_coverage.py
import matplotlib.pyplot as plt
from config import BENCHMARKS, MODES, COLORS, PLOTS_DIR


def run(data):
    fig, ax = plt.subplots(figsize=(11, 8))
    for i, mode in enumerate(MODES[1:], start=1):
        prec = [data[b][mode]["precision_pct"] for b in BENCHMARKS]
        cov  = [data[b][mode]["coverage_pct"]  for b in BENCHMARKS]
        ax.scatter(prec, cov, label=mode, color=COLORS[i],
                   s=80, alpha=0.75, edgecolors="black", linewidths=0.5)
        for b, p, c in zip(BENCHMARKS, prec, cov):
            if p > 15 or c > 15:
                ax.annotate(b, (p, c), fontsize=7, alpha=0.85,
                            xytext=(3, 3), textcoords="offset points")

    ax.axhline(50, color="gray", linestyle=":", alpha=0.5)
    ax.axvline(50, color="gray", linestyle=":", alpha=0.5)
    ax.set_xlabel("Precisión (%)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Cobertura (%)", fontsize=12, fontweight="bold")
    ax.set_title("Trade-off Precisión vs Cobertura\n"
                 "(ideal: esquina superior derecha)", fontweight="bold")
    ax.legend(fontsize=11, loc="upper left", bbox_to_anchor=(1.01, 1), borderaxespad=0)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "10_precision_vs_coverage.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  → 10_precision_vs_coverage.png")