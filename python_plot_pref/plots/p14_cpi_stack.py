# p14_cpi_stack.py
import numpy as np
import matplotlib.pyplot as plt
from plot_utils import top_right_legend
from config import BENCHMARKS, MODES, PALETTE, PLOTS_DIR

def run(data):
    fig, ax = plt.subplots(figsize=(max(18, len(BENCHMARKS) * 1.2), 7))
    x = np.arange(len(BENCHMARKS))
    n_modes = len(MODES)
    width = 0.8 / n_modes

    # Colores tomados de la paleta unificada para mantener coherencia entre gráficas.
    c_valu, c_vmem, c_smem, c_fetch, c_other = PALETTE[:5]

    for i, mode in enumerate(MODES):
        offset = (i - n_modes/2 + 0.5) * width

        valu_v  = [data[b][mode]["cpi_valu"]       for b in BENCHMARKS]
        vmem_v  = [data[b][mode]["cpi_vmem"]       for b in BENCHMARKS]
        smem_v  = [data[b][mode]["cpi_scalarmem"]  for b in BENCHMARKS]
        fetch_v = [data[b][mode]["cpi_fetch"]      for b in BENCHMARKS]
        other_v = [max(data[b][mode]["cpi_total"] - data[b][mode]["cpi_valu"] - data[b][mode]["cpi_vmem"] - data[b][mode]["cpi_scalarmem"] - data[b][mode]["cpi_fetch"], 0) for b in BENCHMARKS]

        b2 = valu_v
        b3 = [a + b for a, b in zip(b2, vmem_v)]
        b4 = [a + b for a, b in zip(b3, smem_v)]
        b5 = [a + b for a, b in zip(b4, fetch_v)]

        l_valu  = "VALU (cómputo)"              if i == 0 else ""
        l_vmem  = "VMem (espera mem vectorial)" if i == 0 else ""
        l_smem  = "ScalarMem (espera mem escalar)"if i == 0 else ""
        l_fetch = "Fetch (instrucciones)"       if i == 0 else ""
        l_other = "Otros"                       if i == 0 else ""

        ax.bar(x + offset, valu_v, width, label=l_valu, color=c_valu, alpha=0.9, edgecolor='white', linewidth=0.2)
        ax.bar(x + offset, vmem_v, width, bottom=b2, label=l_vmem, color=c_vmem, alpha=0.9, edgecolor='white', linewidth=0.2)
        ax.bar(x + offset, smem_v, width, bottom=b3, label=l_smem, color=c_smem, alpha=0.9, edgecolor='white', linewidth=0.2)
        ax.bar(x + offset, fetch_v,width, bottom=b4, label=l_fetch, color=c_fetch, alpha=0.9, edgecolor='white', linewidth=0.2)
        ax.bar(x + offset, other_v,width, bottom=b5, label=l_other, color=c_other, alpha=0.9, edgecolor='white', linewidth=0.2)

        # Nombre del modo encima de cada barra
        for j in range(len(BENCHMARKS)):
            tot = valu_v[j] + vmem_v[j] + smem_v[j] + fetch_v[j] + other_v[j]
            ax.text(x[j] + offset, tot + 0.05, mode, rotation=90, ha='center', va='bottom', fontsize=8)

    ax.set_ylabel("Ciclos por instrucción (CPI)", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(BENCHMARKS, rotation=45, ha="right", fontsize=12)
    ax.tick_params(axis="y", labelsize=12)
    top_right_legend(ax, fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "14_cpi_stack_grouped.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  → 14_cpi_stack_grouped.png")