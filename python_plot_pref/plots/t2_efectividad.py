#t2_efectividad.py
from plot_utils import plot_table
from config import BENCHMARKS, MODES


def run(data):
    rows = []
    for b in BENCHMARKS:
        for m in MODES[1:]:
            d = data[b][m]
            rows.append([
                b, m,
                f"{int(d['pref_miss'])}",
                f"{int(d['pref_first'])}",
                f"{d['precision_pct']:.1f}%",
                f"{d['coverage_pct']:.1f}%",
                f"{d['waste_pct']:.1f}%",
            ])

    plot_table(
        rows,
        ["Benchmark", "Modo", "Traídos de RAM",
         "First-hits", "Precisión", "Cobertura", "Waste"],
        "T2_efectividad.png",
    )