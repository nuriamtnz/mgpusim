#p02_l2miss.py
from plot_utils import plot_bars


def run(data):
    plot_bars(
        data, "l2_miss",
        title="Misses de lectura en L2 (normalizado al baseline)",
        ylabel="Ratio misses",
        filename="02_l2miss_norm.png",
        is_normalized=True,
        force_zero=False,
        reference_line=1.0,
    )