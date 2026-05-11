#config.py
from pathlib import Path

ROOT = Path("/home/nmartinez/tfg/mgpusim") / "amd" / "samples"
PLOTS_DIR = Path("/home/nmartinez/tfg/mgpusim")/ "plots_selectedBench"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

#benchmarks
BENCHMARKS = [
    # "aes",
    "atax",
    # "bfs",
    "bicg",
    # "bitonicsort",
    # "concurrentkernel",
    # "conv2d",
    # "fastwalshtransform",
    "fft",
    # "fir",
    # "floydwarshall",
    # "im2col",
    "kmeans",
    "lenet",
    "matrixmultiplication",
    "matrixtranspose",
    # "minerva",
    # "nbody",
    "nw",
    # "pagerank",
    # "relu",
    "simpleconvolution",
    # "spmv",
    # "stencil2d",
    # "xor",
]

MODES = ["none", "next", "two", "far", "loop"]

# Paleta unificada — estilo formal de artículo científico (inspirada en seaborn "deep").
# El baseline (none) usa un gris oscuro para diferenciarlo claramente de los modos activos.
COLORS = ["#595959", "#4C72B0", "#DD8452", "#55A868", "#C44E52"]

# Paleta extendida para gráficas con más categorías (CPI stack, reclasificación,
# destino de prefetches en L1, etc.). Mantiene la coherencia visual con COLORS.
PALETTE = [
    "#4C72B0",  # azul acero
    "#DD8452",  # naranja terracota
    "#55A868",  # verde salvia
    "#C44E52",  # rojo terracota
    "#8172B2",  # violeta apagado
    "#937860",  # marrón apagado
    "#DA8BC3",  # rosa polvo
    "#8C8C8C",  # gris medio
    "#CCB974",  # ocre/mostaza
    "#64B5CD",  # cian apagado
]

# Color de líneas de referencia (baseline = 1.0, etc.) en estilo formal.
REF_LINE_COLOR = "#2B2B2B"

L2_FILTER = "GPU[1].L2Cache%"
CMD_FILTER = "GPU[1].CommandProcessor%"
CU_FILTER  = "GPU[1].SA[0].CU[0]"
BLOCK_SIZE = 64