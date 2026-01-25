#!/bin/bash

set -e

MGPUSIM_HOME=~/tfg/mgpusim

MODES=(
    "none"
    "next" 
    "two"
    "far"
    "loop"
)

OUTDIR="$MGPUSIM_HOME/results_prefetch"
mkdir -p "$OUTDIR"


#basename se queda con el nombre final del path
#p.e. de amd/samples/memoryread_math -> memoryread_math
bench=amd/samples/memoryread_temporal
BENCH_NAME=$(basename "$bench")
BENCH_DIR="$MGPUSIM_HOME/${bench}"

echo "Benchmark: $BENCH_NAME"

cd "$BENCH_DIR"
go build

RUN_DIR="$OUTDIR/${BENCH_NAME}"
mkdir -p "$RUN_DIR"

for mode in "${MODES[@]}"; do
    echo "-> Modo: $mode"

    ./$(basename "$BENCH_DIR") -timing --report-all -prefetch.mode "$mode"

    # Buscar el .sqlite3 más reciente
    LATEST_DB=$(ls -1t akita_sim_*.sqlite3 | head -n 1)

    mv "$LATEST_DB" "$RUN_DIR/metrics_${mode}.sqlite3"
done