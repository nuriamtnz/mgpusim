#t5_estadisticas.py
import numpy as np
from plot_utils import plot_table
from config import BENCHMARKS, MODES


def run(data):
    rows = []
    for m in MODES[1:]:
        speedups  = [data[b][m]["speedup"]             for b in BENCHMARKS if data[b][m]["time"] > 0]
        precs     = [data[b][m]["precision_pct"]       for b in BENCHMARKS]
        covs      = [data[b][m]["coverage_pct"]        for b in BENCHMARKS]
        wastes    = [data[b][m]["waste_pct"]            for b in BENCHMARKS]
        overheads = [data[b][m]["traffic_overhead_pct"] for b in BENCHMARKS]

        pos_s     = [s for s in speedups if s > 0]
        geo_mean  = np.exp(np.mean(np.log(pos_s))) if pos_s else 1.0
        harm_mean = len(speedups) / sum(1 / s for s in speedups if s > 0) if speedups else 1.0
        n_better  = sum(1 for s in speedups if s > 1.0)
        n_worse   = sum(1 for s in speedups if s < 0.99)

        rows.append([
            m,
            f"{geo_mean:.3f}",
            f"{harm_mean:.3f}",
            f"{np.mean(precs):.1f}%",
            f"{np.mean(covs):.1f}%",
            f"{np.mean(wastes):.1f}%",
            f"{np.mean(overheads):.1f}%",
            f"{n_better}/{len(BENCHMARKS)}",
            f"{n_worse}/{len(BENCHMARKS)}",
        ])

    plot_table(
        rows,
        ["Modo", "Media Geom.", "Media Arm.",
         "Prec. media", "Cob. media", "Waste medio",
         "OH tráfico medio", "Mejoras", "Regresiones"],
        "T5_estadisticas.png",
    )