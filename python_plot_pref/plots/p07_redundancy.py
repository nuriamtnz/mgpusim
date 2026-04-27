#p07_redundancy.py
from plot_utils import plot_bars


def run(data):
    plot_bars(
        data, "redundancy_pct",
        title="Prefetches descartados en L2\n"
              "(línea ya presente en L2 o en vuelo en MSHR al llegar el prefetch)",
        ylabel="Prefetches descartados (%)",
        filename="07_redundancy.png",
        force_zero=True,
    )