#t3_evictions.py
from plot_utils import plot_table
from config import BENCHMARKS, MODES


def run(data):
    rows = []
    for b in BENCHMARKS:
        for m in MODES[1:]:
            d         = data[b][m]
            evict_pct = (d["pref_evict"] / d["pref_miss"] * 100) if d["pref_miss"] > 0 else 0.0
            rows.append([
                b, m,
                f"{int(d['pref_miss'])}",
                f"{int(d['pref_evict'])}",
                f"{evict_pct:.1f}%",
            ])

    plot_table(
        rows,
        ["Benchmark", "Modo", "Traídos de RAM",
         "Eviccionados sin usar", "Evict (%)"],
        "T3_evictions.png",
    )