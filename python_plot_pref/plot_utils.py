#  plot_utils.py
import csv
import numpy as np
import matplotlib.pyplot as plt
from config import BENCHMARKS, MODES, COLORS, PLOTS_DIR

#  Zoom de eje Y
#
#  La idea: si los datos tienen un rango interesante alejado del 0
#  (p.ej. speedup de 0.93 a 1.17), no tiene sentido mostrar el eje
#  desde 0. Mostramos el rango [ymin - margen, ymax + margen].
#
#  Para gráficas de porcentaje (0-100%) donde 0 tiene significado
#  real se puede pasar force_zero=True.

def smart_ylim(ax, values, force_zero=False, margin_ratio=0.15):
    """
    Ajusta el eje Y para hacer zoom sobre el rango real de los datos.

    margin_ratio : fracción del rango total que se añade arriba y abajo.
    force_zero   : fuerza el eje a empezar en 0 (para porcentajes 0-100%).
    """
    valid = [v for v in values if v is not None and not np.isnan(v) and not np.isinf(v)]
    if not valid:
        return

    ymin = min(valid)
    ymax = max(valid)

    if ymax == ymin:
        margin = max(abs(ymin) * 0.1, 0.05)
    else:
        margin = (ymax - ymin) * margin_ratio

    lo = 0.0 if force_zero else (ymin - margin)
    hi = ymax + margin
    ax.set_ylim(lo, hi)


#  Generador genérico de barras agrupadas

def plot_bars(data, metric_key, title, ylabel, filename,
              is_normalized=False, force_zero=False, reference_line=None):
    """
    data          : diccionario data[bench][mode][metric_key]
    is_normalized : divide cada valor por el valor del modo "none"
    force_zero    : eje Y desde 0 (porcentajes absolutos)
    reference_line: valor numérico para trazar una línea horizontal de referencia
    """
    fig_width = max(14, len(BENCHMARKS) * 0.85)
    x     = np.arange(len(BENCHMARKS))
    width = 0.15
    fig, ax = plt.subplots(figsize=(fig_width, 7))

    all_values = []
    for i, mode in enumerate(MODES):
        values = []
        for b in BENCHMARKS:
            val = data[b][mode].get(metric_key, 0.0)
            if is_normalized:
                base_val = data[b]["none"].get(metric_key, 0.0)
                val = val / base_val if base_val > 0 else 0.0
            values.append(val)
        all_values.extend(values)
        ax.bar(x + i * width, values, width, label=mode, color=COLORS[i])

    if reference_line is not None:
        ax.axhline(y=reference_line, color="red", linestyle="--",
                   linewidth=1.5, alpha=0.8,
                   label=f"Referencia ({reference_line})")

    smart_ylim(ax, all_values, force_zero=force_zero)

    ax.set_title(title, fontweight="bold", fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_xticks(x + 2 * width)
    ax.set_xticklabels(BENCHMARKS, rotation=90, fontsize=9)
    ax.legend(fontsize=11, loc="upper left", bbox_to_anchor=(1.01, 1), borderaxespad=0)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(PLOTS_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  → {filename}")



# ─────────────────────────────────────────────────────────────
#  Generador de tablas
# ─────────────────────────────────────────────────────────────
def plot_table(cell_text, col_labels, filename):
    row_h      = 0.32
    fig_height = max(4, len(cell_text) * row_h + 1.0)
    fig, ax    = plt.subplots(figsize=(max(12, len(col_labels) * 1.9), fig_height))
    ax.axis("off")
    tabla = ax.table(cellText=cell_text, colLabels=col_labels,
                     loc="center", cellLoc="center")
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(8)
    tabla.scale(1, 1.5)
    fig.savefig(PLOTS_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  → {filename}")

    # Exportar también automáticamente a formato CSV
    csv_filename = filename.replace('.png', '.csv')
    with open(PLOTS_DIR / csv_filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_ALL)
        writer.writerow(col_labels)
        writer.writerows(cell_text)
    print(f"  → {csv_filename}")