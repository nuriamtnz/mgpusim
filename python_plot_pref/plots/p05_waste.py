#p05_waste.py
from plot_utils import plot_bars


def run(data):
    plot_bars(
        data, "waste_pct",
        title="Desperdicio de prefetch\n(bloques traídos de RAM nunca usados)",
        ylabel="Waste (%)",
        filename="05_waste.png",
        force_zero=True,
    )