#p09_heatmap.py
import numpy as np
import matplotlib.pyplot as plt
from config import BENCHMARKS, MODES, PLOTS_DIR


def run(data):
    speedups  = np.array([
        [data[b][m]["speedup"] for m in MODES[1:]]
        for b in BENCHMARKS
    ])
    deviation = max(abs(speedups.max() - 1.0), abs(1.0 - speedups.min()), 0.05)
    vmin, vmax = 1.0 - deviation, 1.0 + deviation

    fig, ax = plt.subplots(figsize=(7, max(6, len(BENCHMARKS) * 0.42)))
    im = ax.imshow(speedups, cmap="RdYlGn", aspect="auto", vmin=vmin, vmax=vmax)
    ax.set_xticks(np.arange(len(MODES[1:])))
    ax.set_yticks(np.arange(len(BENCHMARKS)))
    ax.set_xticklabels(MODES[1:], fontsize=11)
    ax.set_yticklabels(BENCHMARKS, fontsize=9)

    for i in range(len(BENCHMARKS)):
        for j in range(len(MODES[1:])):
            color = "white" if speedups[i, j] < (vmin + (vmax - vmin) * 0.3) else "black"
            ax.text(j, i, f"{speedups[i, j]:.3f}",
                    ha="center", va="center", color=color, fontsize=7)

    plt.colorbar(im, ax=ax, label="Speedup", shrink=0.8)
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "09_heatmap_speedup.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  → 09_heatmap_speedup.png")