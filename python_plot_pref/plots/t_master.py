# t_master.py
from plot_utils import plot_table
from config import BENCHMARKS, MODES

def run(data):
    rows = []
    for b in BENCHMARKS:
        bm = data[b]["none"]["l2_miss"]
        for m in MODES[1:]:
            d    = data[b][m]

            l1_att  = d.get("l1_pref_attempted", 0)
            l1_red  = d.get("l1_pref_redundant_pct", 0.0)
            l1_drp  = d.get("l1_pref_drop_port_pct", 0.0)
            l1_infl = d.get("l1_pref_drop_inflight_pct", 0.0)

            rows.append([
                b, m,
                f"{d['speedup']:.3f}x",
                f"{int(d['top_demand_read'])}",
                f"{int(d['top_prefetch_read'])}",
                f"{int(bm)}",
                f"{int(d['l2_miss'])}",
                f"{int(d['pref_first'])}",
                f"{d['precision_pct']:.1f}%",
                f"{d['coverage_pct']:.1f}%",
                f"{d['waste_pct']:.1f}%",
                f"{d['traffic_overhead_pct']:.1f}%",
                f"{int(l1_att)}",
                f"{l1_red:.1f}%",
                f"{l1_drp:.1f}%",
                f"{l1_infl:.1f}%",
            ])

    cols = [
        "Bench", "Modo", "Speedup",
        "L2 dem-reads", "L2 pref-reads",
        "Base miss", "Miss actual",
        "First-hit L2",
        "Precisión", "Cobertura", "Waste",
        "OH tráfico",
        "L1 Gen. Total", "L1 Ya en Caché%", "L1 Red Llena%", "L1 Lím. en vuelo%"
    ]
    
    plot_table(rows, cols, "T_master.png")