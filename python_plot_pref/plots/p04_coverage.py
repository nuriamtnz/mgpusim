#p04_coverage.py
from plot_utils import plot_bars


def run(data):
    plot_bars(
        data, "coverage_pct",
        title="Cobertura del prefetcher\n(first-hits / misses baseline)",
        ylabel="Cobertura (%)",
        filename="04_coverage.png",
        force_zero=True,
    )