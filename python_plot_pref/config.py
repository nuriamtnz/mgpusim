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
COLORS = ["#A8A8A8", "#98D8C8", "#F7DC6F", "#D7BDE2", "#85C1E9"]

L2_FILTER = "GPU[1].L2Cache%"
CMD_FILTER = "GPU[1].CommandProcessor%"
CU_FILTER  = "GPU[1].SA[0].CU[0]"
BLOCK_SIZE = 64