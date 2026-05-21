#p17_l2_requests.py
import numpy as np
import matplotlib.pyplot as plt
from plot_utils import smart_ylim, top_right_legend
from config import BENCHMARKS, MODES, COLORS, PLOTS_DIR, REF_LINE_COLOR


def run(data):
    fig, ax = plt.subplots(figsize=(max(14, len(BENCHMARKS) * 0.85), 7))
    x     = np.arange(len(BENCHMARKS))
    width = 0.15

    baseline_demand = [data[b]["none"]["top_demand_read"] for b in BENCHMARKS]
    all_tops = []

    for i, mode in enumerate(MODES):
        demand   = [data[b][mode]["top_demand_read"]    for b in BENCHMARKS]
        prefetch = [data[b][mode]["top_prefetch_read"]  for b in BENCHMARKS]

        demand_norm   = [d / bd if bd > 0 else 0 for d, bd in zip(demand,   baseline_demand)]
        prefetch_norm = [p / bd if bd > 0 else 0 for p, bd in zip(prefetch, baseline_demand)]
        total_norm    = [d + p for d, p in zip(demand_norm, prefetch_norm)]
        all_tops.extend(total_norm)

        ax.bar(x + i * width, demand_norm,   width, color=COLORS[i], alpha=0.9,
               label=f"{mode} — demanda")
        ax.bar(x + i * width, prefetch_norm, width, color=COLORS[i], alpha=0.4,
               label=f"{mode} — prefetch", bottom=demand_norm)

    ax.axhline(1.0, color=REF_LINE_COLOR, linestyle="--", linewidth=1.2,
               alpha=0.85, label="Baseline demand reads")

    smart_ylim(ax, all_tops + [1.0], force_zero=True)

    ax.set_ylabel("Ratio respecto baseline demand-reads", fontsize=14)
    ax.set_xticks(x + 2 * width)
    ax.set_xticklabels(BENCHMARKS, rotation=45, ha="right", fontsize=12)
    ax.tick_params(axis="y", labelsize=12)
    # 11 elementos → 6 columnas × 2 filas
    top_right_legend(ax, ncol=6, fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "17_l2_total_requests.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  → 17_l2_total_requests.png")