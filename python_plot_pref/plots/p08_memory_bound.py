#p08_memory_bound.py
from plot_utils import plot_bars


def run(data):
    plot_bars(
        data, "mem_bound_ratio",
        title="Fracción memory-bound del tiempo de ejecución (baseline)\n"
              "(VMem + ScalarMem) / CPI_total",
        ylabel="Ratio memoria / (memoria + cómputo)",
        filename="08_memory_bound_ratio.png",
        force_zero=True,
    )