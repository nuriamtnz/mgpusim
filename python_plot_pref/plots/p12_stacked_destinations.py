#p12_stacked_destinations.py
import numpy as np
import matplotlib.pyplot as plt
from plot_utils import top_right_legend
from config import BENCHMARKS, MODES, COLORS, PLOTS_DIR


def run(data):
    fig, ax = plt.subplots(figsize=(max(14, len(BENCHMARKS) * 0.85), 7))
    x     = np.arange(len(BENCHMARKS))
    width = 0.18

    for i, mode in enumerate(MODES[1:]):
        miss_v, mshr_v, l2_v = [], [], []
        for b in BENCHMARKS:
            d     = data[b][mode]
            total = d["pref_req_sent"]
            if total > 0:
                miss_v.append(d["pref_miss"] / total * 100)
                mshr_v.append(d["pref_mshr"] / total * 100)
                l2_v.append(d["pref_l2"]   / total * 100)
            else:
                miss_v.append(0); mshr_v.append(0); l2_v.append(0)

        offset = i * width
        c = COLORS[i + 1]
        ax.bar(x + offset, miss_v, width, color=c, alpha=0.9,  label=f"{mode} — fue a RAM")
        ax.bar(x + offset, mshr_v, width, color=c, alpha=0.55, label=f"{mode} — hit MSHR",
               bottom=miss_v)
        ax.bar(x + offset, l2_v,   width, color=c, alpha=0.25, label=f"{mode} — hit L2",
               bottom=[a + b for a, b in zip(miss_v, mshr_v)])

    ax.set_ylabel("Porcentaje (%)", fontsize=11)
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(BENCHMARKS, rotation=45, ha="right", fontsize=8)
    # 12 elementos → 4 columnas × 3 filas para que la leyenda quepa encima del eje
    top_right_legend(ax, ncol=4, fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "12_stacked_destinations.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  → 12_stacked_destinations.png")