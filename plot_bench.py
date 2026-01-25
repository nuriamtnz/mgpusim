import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt

# Configuración
BASE_DIR = Path("results_prefetch")
BENCH = "fma"  # Cambia aquí para cada benchmark

# Carpeta de salida para todas las gráficas
PLOTS_DIR = Path("plots_prefetch") / BENCH
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

MODES = {
    "none": "metrics_none.sqlite3",
    "next": "metrics_next.sqlite3",
    "two":  "metrics_two.sqlite3",
    "far":  "metrics_far.sqlite3",
    "loop": "metrics_loop.sqlite3",
}

TABLE_NAME = "mgpusim_metrics"
L2_LOCATION_FILTER = "GPU[1].L2Cache%"


def get_metric_per_mode(metric_name, aggregate="avg"):
    results = {}
    for mode, file_name in MODES.items():
        db_path = BASE_DIR / BENCH / file_name
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Filtros específicos por métrica
        if "kernel_time" in metric_name:
            # Driver
            cur.execute("SELECT Value FROM {} WHERE What = ? AND Location = 'Driver'".format(TABLE_NAME), (metric_name,))
        elif "cu_CPI" in metric_name or "simd_CPI" in metric_name:
            # Todos los CU
            cur.execute("SELECT Value FROM {} WHERE What = ? AND Location LIKE 'GPU[1].SA[0].CU%'".format(TABLE_NAME), (metric_name,))
        elif "read_trans_count" in metric_name or "write_trans_count" in metric_name:
            # Todos los DRAM
            cur.execute("SELECT Value FROM {} WHERE What = ? AND Location LIKE 'GPU[1].DRAM%'".format(TABLE_NAME), (metric_name,))
        elif "read-miss" in metric_name:
            # Solo L2
            cur.execute("SELECT Value FROM {} WHERE What = ? AND Location LIKE ?".format(TABLE_NAME), (metric_name, L2_LOCATION_FILTER))
        else:
            # Por defecto: L2
            cur.execute("SELECT Value FROM {} WHERE What = ? AND Location LIKE ?".format(TABLE_NAME), (metric_name, L2_LOCATION_FILTER))
        
        rows = cur.fetchall()
        conn.close()

        values = [row[0] for row in rows]
        if not values:
            results[mode] = 0.0
        else:
            if aggregate == "avg":
                results[mode] = sum(values) / len(values)
            else:
                results[mode] = sum(values)
    return results



def plot_bar_metric(metrics, title, ylabel, out_name):
    """Gráfica de barras"""
    modes = list(metrics.keys())
    values = [metrics[m] for m in modes]

    plt.figure(figsize=(6, 4))
    plt.bar(modes, values, color="steelblue")
    plt.title(title)
    plt.xlabel("Prefetch mode")
    plt.ylabel(ylabel)
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    
    # PDF vectorial para LaTeX + PNG backup
    plt.savefig(PLOTS_DIR / f"{out_name}.pdf", format="pdf", bbox_inches="tight")
    plt.savefig(PLOTS_DIR / f"{out_name}.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_time_vs_precision():
    """Tiempo kernel vs precisión"""
    precision = get_metric_per_mode("pref-precision", aggregate="avg")
    kernel_times = get_metric_per_mode("kernel_time")

    modes = list(MODES.keys())
    prec_vals = [precision[m] for m in modes]
    time_vals = [kernel_times[m] * 1e6 for m in modes]  # a microsegundos

    fig, ax1 = plt.subplots(figsize=(7, 4))

    # Tiempo (rojo)
    ax1.set_xlabel("Prefetch mode")
    ax1.set_ylabel("Tiempo kernel (µs)", color="tab:red")
    ax1.plot(modes, time_vals, marker="o", color="tab:red", linewidth=2)
    ax1.tick_params(axis="y", labelcolor="tab:red")
    ax1.grid(axis="y", linestyle="--", alpha=0.4)

    # Precisión (azul)
    ax2 = ax1.twinx()
    ax2.set_ylabel("Precisión (%)", color="tab:blue")
    ax2.plot(modes, prec_vals, marker="s", color="tab:blue", linewidth=2)
    ax2.tick_params(axis="y", labelcolor="tab:blue")

    plt.title(f"Tiempo kernel vs precisión de prefetch ({BENCH})")
    fig.tight_layout()
    
    plt.savefig(PLOTS_DIR / f"{BENCH}_time_vs_precision.pdf", format="pdf", bbox_inches="tight")
    plt.savefig(PLOTS_DIR / f"{BENCH}_time_vs_precision.png", dpi=300, bbox_inches="tight")
    plt.close()


def main():
    print(f"Generando 8 gráficas para {BENCH} en {PLOTS_DIR}")
    
    # 1. Precisión prefetch
    plot_bar_metric(
        get_metric_per_mode("pref-precision", aggregate="avg"),
        f"Precisión media de prefetch en L2 ({BENCH})",
        "Precisión (%)",
        f"{BENCH}_pref_precision",
    )
    
    # 2. Cobertura prefetch
    plot_bar_metric(
        get_metric_per_mode("pref-coverage", aggregate="avg"),
        f"Cobertura media de prefetch en L2 ({BENCH})",
        "Cobertura (%)",
        f"{BENCH}_pref_coverage",
    )
    
    # 3. Desperdicio prefetch
    plot_bar_metric(
        get_metric_per_mode("pref-waste-ratio", aggregate="avg"),
        f"Desperdicio medio de prefetch en L2 ({BENCH})",
        "Desperdicio (%)",
        f"{BENCH}_pref_waste_ratio",
    )
    
    # 4. Prefetch enviados
    plot_bar_metric(
        get_metric_per_mode("pref-req-sent", aggregate="sum"),
        f"Prefetch enviados en L2 ({BENCH})",
        "pref-req-sent (suma L2)",
        f"{BENCH}_pref_req_sent",
    )
    
    # 5. CPI promedio
    plot_bar_metric(
        get_metric_per_mode("cu_CPI"),
        f"CPI promedio por CU ({BENCH})",
        "CPI (cycles/inst)",
        f"{BENCH}_cu_CPI",
    )
    
    # 6. Read-miss L2
    plot_bar_metric(
        get_metric_per_mode("read-miss", aggregate="sum"),
        f"Read-miss en L2 ({BENCH})",
        "Read-miss (suma L2)",
        f"{BENCH}_l2_read_miss",
    )
    
    # 7. DRAM reads
    plot_bar_metric(
        get_metric_per_mode("read_trans_count", aggregate="sum"),
        f"Accesos DRAM lectura ({BENCH})",
        "read_trans_count (suma DRAM)",
        f"{BENCH}_dram_reads",
    )
    
    # 8. Tiempo vs precisión (bonus)
    plot_time_vs_precision()
    
    print("¡Listo! 8 gráficas guardadas en:", PLOTS_DIR)
    print("Archivos .pdf listos para LaTeX")


if __name__ == "__main__":
    main()
