#run_all.py
"""
run_all.py — punto de entrada único.

Uso:
    python3 run_all.py              # genera todo
    python3 run_all.py p01 p09 t4  # genera solo las gráficas/tablas indicadas

Los identificadores son los prefijos de los archivos en plots/:
    p01 … p17   gráficas
    t_master    tabla maestra
    t1 … t5     tablas de resumen
"""

import sys
import importlib
from data_loader import load_data, check_all_invariants

#Registro de módulos
# Cada entrada: (identificador_cli, módulo_python)
MODULES = [
    ("p01",      "plots.p01_speedup"),
    ("p02",      "plots.p02_l2miss"),
    ("p03",      "plots.p03_precision"),
    ("p04",      "plots.p04_coverage"),
    ("p05",      "plots.p05_waste"),
    ("p06",      "plots.p06_traffic_overhead"),
    ("p07",      "plots.p07_redundancy"),
    ("p08",      "plots.p08_memory_bound"),
    ("p09",      "plots.p09_heatmap"),
    ("p10",      "plots.p10_precision_vs_coverage"),
    ("p11",      "plots.p11_boxplots"),
    ("p12",      "plots.p12_stacked_destinations"),
    ("p13",      "plots.p13_theoretical_vs_real"),
    ("p14",      "plots.p14_cpi_stack"),
    ("p15",      "plots.p15_memboundness_vs_speedup"),
    ("p16",      "plots.p16_reclassification"),
    ("p17",      "plots.p17_l2_requests"),
    ("p18",      "plots.p18_l1_prefetch_fate"),
    ("t_master", "plots.t_master"),
    ("t1",       "plots.t1_destinations"),
    ("t2",       "plots.t2_efectividad"),
    ("t3",       "plots.t3_evictions"),
    ("t4",       "plots.t4_resumen"),
    ("t5",       "plots.t5_estadisticas"),
]

#Selección por CLI
requested = set(sys.argv[1:]) if len(sys.argv) > 1 else None

selected = [
    (key, mod) for key, mod in MODULES
    if requested is None or key in requested
]

if not selected:
    print(f"No se encontraron módulos para: {sys.argv[1:]}")
    print("Identificadores disponibles:", [k for k, _ in MODULES])
    sys.exit(1)

#Carga de datos (una sola vez)
data = load_data()
check_all_invariants(data)

#Ejecución
section = {"p": "Gráficas", "t": "Tablas"}
current_section = None

for key, mod_path in selected:
    sec = section.get(key[0], "Otros")
    if sec != current_section:
        print(f"\nGenerando {sec}...")
        current_section = sec

    mod = importlib.import_module(mod_path)
    mod.run(data)

print(f"\n¡Listo! Salidas en: plots_allBench/")