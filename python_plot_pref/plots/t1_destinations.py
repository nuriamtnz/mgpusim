#t1_destinations.py
from plot_utils import plot_table
from config import BENCHMARKS, MODES


def run(data):
    rows = []
    for b in BENCHMARKS:
        for m in MODES[1:]:
            d = data[b][m]
            rows.append([
                b, m,
                f"{int(d['pref_req_sent'])}",
                f"{int(d['pref_miss'])}",
                f"{int(d['pref_mshr'])}",
                f"{int(d['pref_l2'])}",
                f"{d['redundancy_pct']:.1f}%",
            ])

    plot_table(
        rows,
        ["Benchmark", "Modo", "Total peticiones pref.",
         "→ RAM", "Hit MSHR", "Hit L2", "Descartados L2/MSHR (%)"],
        "T1_destinos.png",
    )