# 03_precision.py
from plot_utils import plot_bars


def run(data):
    plot_bars(
        data, "precision_pct",
        title="Precisión del prefetcher\n(bloques útiles / bloques traídos de RAM)",
        ylabel="Precisión (%)",
        filename="03_precision.png",
        force_zero=True,
    )