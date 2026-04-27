#p01_speedup.py
from plot_utils import plot_bars


def run(data):
    plot_bars(
        data, "speedup",
        title="Speedup respecto al baseline (none)",
        ylabel="Speedup (ratio)",
        filename="01_speedup.png",
        force_zero=False,       # zoom sobre el rango real, no desde 0
        reference_line=1.0,
    )