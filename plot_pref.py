import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Directorios
BASE_DIR = Path("results_prefetch")
PLOTS_DIR = Path("plots_prefetch")
PLOTS_DIR.mkdir(exist_ok=True)

MODES = ["none", "next", "two", "far", "loop"]
L2_FILTER = "GPU[1].L2Cache%"

# Buscar todos los benchmarks
benchmarks = []
for path in BASE_DIR.glob("*/metrics_none.sqlite3"):
    bench = path.parent.name
    if len(bench) > 0:
        benchmarks.append(bench)
benchmarks.sort()
print("Benchmarks:", benchmarks)

def leer_kernel_time(db_path):
    if not db_path.exists():
        return 0.0
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Busca CommandProcessor
    cur.execute("SELECT SUM(Value) FROM mgpusim_metrics WHERE What='kernel_time' AND Location LIKE '%CommandProcessor%'")
    valor = cur.fetchone()[0] or 0.0
    conn.close()
    return valor

def leer_valor(db_path, what):
    if not db_path.exists():
        print(f"  FALTA: {db_path} para {what}")
        return 0.0
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"SELECT SUM(Value) FROM mgpusim_metrics WHERE What=? AND Location LIKE ?", 
                (what, L2_FILTER))
    valor = cur.fetchone()[0] or 0.0
    conn.close()
    return valor

# DEBUG: Verificar valores reales
print("\n=== DEBUG VALORES REALES ===")
for bench in benchmarks:
    print(f"\n--- {bench} ---")
    for modo in MODES:
        db = BASE_DIR / bench / f"metrics_{modo}.sqlite3"
        tiempo = leer_kernel_time(db)
        l2_miss = leer_valor(db, "read-miss")
        print(f"  {modo}: tiempo={tiempo:.1f}, L2_miss={l2_miss:.0f}")
print("\n=== FIN DEBUG ===")

width = 0.14
x = np.arange(len(benchmarks))
colores_pastel = {
    'none': '#A8A8A8',  # Gris
    'next': '#98D8C8',  # Verde menta
    'two': '#F7DC6F',   # Amarillo suave
    'far': '#D7BDE2',   # Lila
    'loop': '#85C1E9'   # Azul cielo
}

# 1. GRAFICA 1: Tiempo normalizado (clusters por benchmark)
fig1, ax1 = plt.subplots(figsize=(12, 6))
for i, modo in enumerate(MODES):
    valores = []
    for bench in benchmarks:
        db_none = BASE_DIR / bench / "metrics_none.sqlite3"
        db_modo = BASE_DIR / bench / f"metrics_{modo}.sqlite3"
        tiempo_none = leer_kernel_time(db_none)
        tiempo_modo = leer_kernel_time(db_modo)
        norm = tiempo_modo / tiempo_none if tiempo_none > 0 else 1.0
        valores.append(norm)
        print(f"Tiempo {bench} {modo}: {tiempo_modo}/{tiempo_none} = {norm:.3f}")
    ax1.bar(x + i*width, valores, width, label=modo, color=colores_pastel[modo])

ax1.set_xticks(x)
ax1.set_xticklabels(benchmarks, rotation=45, ha='right')
ax1.set_ylabel('Tiempo / tiempo_none')
ax1.set_title('Tiempo normalizado por benchmark')
##mas precisión
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.3f}'))
ax1.set_ylim(0.95, 1.05)
##
ax1.legend()
ax1.grid(True, alpha=0.3)
fig1.tight_layout()
fig1.savefig(PLOTS_DIR / 'tiempo_norm.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. GRAFICA 2: Precision (clusters por benchmark)
fig2, ax2 = plt.subplots(figsize=(12, 6))

for i, modo in enumerate(MODES):
    valores = []
    for bench in benchmarks:
        db_modo = BASE_DIR / bench / f"metrics_{modo}.sqlite3"
        pref_hit = leer_valor(db_modo, "prefetch-hit")
        first_hits = leer_valor(db_modo, "prefetch-first-hit")
        precision = (first_hits / pref_hit * 100) if pref_hit > 0 else 0.0
        valores.append(precision)
    ax2.bar(x + i*width, valores, width, label=modo, color=colores_pastel[modo])

ax2.set_xticks(x)
ax2.set_xticklabels(benchmarks, rotation=45, ha='right')
ax2.set_ylabel('Precision (%)')
ax2.set_title('Precision del prefetch por benchmark')
ax2.legend()
ax2.grid(True, alpha=0.3)
fig2.tight_layout()
fig2.savefig(PLOTS_DIR / 'precision.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. GRAFICA 3: Coverage miss (clusters por benchmark)
fig3, ax3 = plt.subplots(figsize=(12, 6))

for i, modo in enumerate(MODES):
    valores = []
    for bench in benchmarks:
        db_none = BASE_DIR / bench / "metrics_none.sqlite3"
        db_modo = BASE_DIR / bench / f"metrics_{modo}.sqlite3"
        l2_miss_none = leer_valor(db_none, "read-miss")
        l2_miss_modo = leer_valor(db_modo, "read-miss")
        norm = l2_miss_modo / l2_miss_none if l2_miss_none > 0 else 1.0
        valores.append(norm)
        print(f"L2_miss {bench} {modo}: {l2_miss_modo}/{l2_miss_none} = {norm:.3f}")
    ax3.bar(x + i*width, valores, width, label=modo, color=colores_pastel[modo])

ax3.set_xticks(x)
ax3.set_xticklabels(benchmarks, rotation=45, ha='right')
ax3.set_ylabel('L2 read-miss / none')
ax3.set_title('L2 read-miss normalizado por benchmark')
##más Precisión
ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.3f}'))
ax3.set_ylim(0.95, 1.10)
##
ax3.legend()
ax3.grid(True, alpha=0.3)
fig3.tight_layout()
fig3.savefig(PLOTS_DIR / 'l2_miss_norm.png', dpi=300, bbox_inches='tight')
plt.close()

print("Graficas guardadas en:", PLOTS_DIR)
