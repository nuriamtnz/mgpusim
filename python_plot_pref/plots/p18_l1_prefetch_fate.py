# p18_l1_prefetch_fate.py
import numpy as np
import matplotlib.pyplot as plt
from plot_utils import top_right_legend
from config import BENCHMARKS, MODES, PALETTE, PLOTS_DIR

def run(data):
    fig, ax = plt.subplots(figsize=(max(18, len(BENCHMARKS) * 1.2), 7))
    x = np.arange(len(BENCHMARKS))
    modes_to_plot = MODES[1:]
    n_modes = len(modes_to_plot)
    width = 0.8 / n_modes

    # Colores de la paleta unificada (mantienen coherencia con el resto de gráficas).
    c_sent, c_l1, c_mshr, c_port, c_infl = PALETTE[:5]

    for i, mode in enumerate(modes_to_plot):
        offset = (i - n_modes/2 + 0.5) * width

        sent_v, l1_v, mshr_v, port_v, infl_v = [], [], [], [], []
        for b in BENCHMARKS:
            d = data[b][mode]
            total = d.get("l1_pref_attempted", 0)
            if total > 0:
                sent_v.append(d["l1_pref_sent"] / total * 100)
                l1_v.append(d["l1_pref_abort_l1"] / total * 100)
                mshr_v.append(d["l1_pref_abort_mshr"] / total * 100)
                port_v.append(d["l1_pref_abort_port"] / total * 100)
                infl_v.append(d["l1_pref_abort_inflight"] / total * 100)
            else:
                sent_v.append(0); l1_v.append(0); mshr_v.append(0); port_v.append(0); infl_v.append(0)

        b2 = sent_v
        b3 = [a + b for a, b in zip(b2, l1_v)]
        b4 = [a + b for a, b in zip(b3, mshr_v)]
        b5 = [a + b for a, b in zip(b4, port_v)]

        l_sent = "Enviado a L2"             if i == 0 else ""
        l_l1   = "Abortado: Ya en L1"       if i == 0 else ""
        l_mshr = "Abortado: Ya en MSHR"     if i == 0 else ""
        l_port = "Abortado: Red L1-L2 Llena"if i == 0 else ""
        l_infl = "Abortado: Límite en vuelo"if i == 0 else ""

        ax.bar(x + offset, sent_v, width, label=l_sent, color=c_sent, alpha=0.9, edgecolor='black', linewidth=0.5)
        ax.bar(x + offset, l1_v,   width, bottom=b2, label=l_l1,   color=c_l1,   alpha=0.85, edgecolor='black', linewidth=0.5, hatch='//')
        ax.bar(x + offset, mshr_v, width, bottom=b3, label=l_mshr, color=c_mshr, alpha=0.85, edgecolor='black', linewidth=0.5, hatch='\\\\')
        ax.bar(x + offset, port_v, width, bottom=b4, label=l_port, color=c_port, alpha=0.9,  edgecolor='black', linewidth=0.5, hatch='xx')
        ax.bar(x + offset, infl_v, width, bottom=b5, label=l_infl, color=c_infl, alpha=0.9,  edgecolor='black', linewidth=0.5, hatch='..')

        # Nombre del modo encima de cada barra
        for j in range(len(BENCHMARKS)):
            tot = sent_v[j] + l1_v[j] + mshr_v[j] + port_v[j] + infl_v[j]
            if tot > 0.1:
                ax.text(x[j] + offset, tot + 2, mode, rotation=90, ha='center', va='bottom', fontsize=6)

    ax.set_ylabel("Porcentaje sobre Prefetches Generados (%)", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(BENCHMARKS, rotation=45, ha="right", fontsize=9)
    top_right_legend(ax, fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "18_l1_prefetch_fate.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  → 18_l1_prefetch_fate.png")