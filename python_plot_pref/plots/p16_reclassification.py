# p16_reclassification.py
import numpy as np
import matplotlib.pyplot as plt
from config import BENCHMARKS, MODES, PLOTS_DIR

def run(data):
    # Usamos un ancho mayor para acomodar barras agrupadas
    fig, ax = plt.subplots(figsize=(max(18, len(BENCHMARKS) * 1.2), 7))
    
    x = np.arange(len(BENCHMARKS))
    modes_to_plot = MODES[1:] # No incluimos 'none' porque es la referencia de la línea roja
    n_modes = len(modes_to_plot)
    width = 0.8 / n_modes # Ajustamos el ancho para que quepan todos los modos
    
    for i, mode in enumerate(modes_to_plot):
        # Calcular el offset para que las barras queden unas al lado de otras
        offset = (i - n_modes/2 + 0.5) * width
        
        remaining = [data[b][mode]["miss_remaining_pct"] / 100 for b in BENCHMARKS]
        to_mshr   = [data[b][mode]["miss_to_mshr_pct"]   / 100 for b in BENCHMARKS]
        to_hit    = [data[b][mode]["miss_to_hit_pct"]    / 100 for b in BENCHMARKS]
        org_mshr  = [data[b][mode]["mshr_organic_pct"]   / 100 for b in BENCHMARKS]
        org_hit   = [data[b][mode]["hit_organic_pct"]    / 100 for b in BENCHMARKS]

        b1 = remaining
        b2 = [a + b for a, b in zip(b1, to_mshr)]
        b3 = [a + b for a, b in zip(b2, to_hit)]
        b4 = [a + b for a, b in zip(b3, org_mshr)]

        # Solo ponemos label en la primera iteración para que la leyenda no se duplique
        l_rem   = "Miss (sigue siendo miss)" if i == 0 else ""
        l_tmshr = "→ MSHR-hit × prefetch"    if i == 0 else ""
        l_thit  = "→ L2-hit × prefetch"      if i == 0 else ""
        l_omshr = "→ MSHR-hit orgánico"      if i == 0 else ""
        l_ohit  = "→ L2-hit orgánico"        if i == 0 else ""

        ax.bar(x + offset, remaining, width, color="#4472C4", alpha=0.9, edgecolor='white', linewidth=0.5, label=l_rem)
        ax.bar(x + offset, to_mshr, width, bottom=b1, color="#ED7D31", alpha=0.9, edgecolor='white', linewidth=0.5, label=l_tmshr)
        ax.bar(x + offset, to_hit, width, bottom=b2, color="#70AD47", alpha=0.9, edgecolor='white', linewidth=0.5, label=l_thit)
        ax.bar(x + offset, org_mshr, width, bottom=b3, color="#FFC000", alpha=0.75, edgecolor='white', linewidth=0.5, label=l_omshr)
        ax.bar(x + offset, org_hit, width, bottom=b4, color="#9DC3E6", alpha=0.75, edgecolor='white', linewidth=0.5, label=l_ohit)

        # Añadimos el nombre del modo en vertical dentro de la barra o encima
        for j in range(len(BENCHMARKS)):
            total_height = remaining[j] + to_mshr[j] + to_hit[j] + org_mshr[j] + org_hit[j]
            if total_height > 0.05: # Solo si hay algo que mostrar
                ax.text(x[j] + offset, total_height + 0.02, mode, rotation=90, ha='center', va='bottom', fontsize=6)

    ax.axhline(1.0, color="red", linestyle="--", linewidth=1.5, alpha=0.8, label="Total demandas (Baseline)")

    ax.set_title("Reclasificación de Demandas a L2 (Agrupado por Benchmark y Modo)", fontweight="bold")
    ax.set_ylabel("Fracción respecto al total de demandas base", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(BENCHMARKS, rotation=45, ha="right", fontsize=9)
    ax.legend(fontsize=9, loc="upper left", bbox_to_anchor=(1.01, 1), borderaxespad=0)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / "16_miss_reclassification.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("  → 16_miss_reclassification.png")