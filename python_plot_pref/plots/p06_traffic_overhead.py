#p06_traffic_overhead.py
from plot_utils import plot_bars


def run(data):
    plot_bars(
        data, "traffic_overhead_pct",
        title="Overhead de tráfico de memoria\n"
              "(accesos extra de prefetch a DRAM / misses de demanda baseline)",
        ylabel="Overhead (%)",
        filename="06_traffic_overhead.png",
        force_zero=True,
    )