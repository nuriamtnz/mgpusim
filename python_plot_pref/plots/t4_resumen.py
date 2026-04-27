#t4_resumen.py
from plot_utils import plot_table
from config import BENCHMARKS, MODES


def run(data):
    rows = []
    for b in BENCHMARKS:
        best_m  = max(MODES[1:], key=lambda m: data[b][m]["speedup"])
        d       = data[b][best_m]
        d0      = data[b]["none"]
        mem_pct = d0["mem_bound_ratio"] * 100
        theo    = min(d0["max_theoretical_speedup"], 9.99)
        rows.append([
            b,
            f"{mem_pct:.0f}%",
            f"{theo:.2f}x",
            best_m,
            f"{d['speedup']:.3f}x",
            f"{d['precision_pct']:.1f}%",
            f"{d['coverage_pct']:.1f}%",
            f"{d['waste_pct']:.1f}%",
        ])

    plot_table(
        rows,
        ["Benchmark", "Mem-bound%", "Speedup teórico",
         "Mejor modo", "Speedup real",
         "Precisión", "Cobertura", "Waste"],
        "T4_resumen.png",
    )