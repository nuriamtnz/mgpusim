#!/bin/bash

set -e

MGPUSIM_HOME=~/tfg/mgpusim

BENCHES=(
    "amd/samples/relu"
    "amd/samples/memoryread"
    "amd/samples/memcopy"
    "amd/samples/memoryread_math"
    "amd/samples/memoryread_loop"

    "amd/samples/fir"
    "amd/samples/stencil2d"
    "amd/samples/simpleconvolution"
    
    "amd/samples/matrixtranspose"
    "amd/samples/matrixmultiplication"
    # "amd/samples/atax"
    # "amd/samples/bicg"

    # "amd/samples/bitonicsort"
    # "amd/samples/fft"
    # "amd/samples/fastwaslshtransform"

    # "amd/samples/spmv"
    # "amd/samples/bfs"
    # "amd/samples/pagerank"

    # "amd/samples/kmeans"
    # "amd/samples/nw"
    # "amd/samples/floydwarshall"

    # "amd/samples/conv2d"
    # "amd/samples/im2col"

    # "amd/samples/aes"
    # "amd/samples/nbody"

    ## despues de casi 6h el kernerl lenet en modo far no avanzaba
    # "amd/samples/xor"
    # "amd/samples/lenet"
    # "amd/samples/vgg16"
    # "amd/samples/minerva"

    # "amd/samples/runner"
    # "amd/samples/server"

    # "amd/samples/concurrentkernel"
    # "amd/samples/concurrentworkload"
)

MODES=(
    "none"
    "next" 
    "two"
    "far"
    "loop"
)

OUTDIR="$MGPUSIM_HOME/results_prefetch"
mkdir -p "$OUTDIR"

#recorrido de benchmarcks
for bench in "${BENCHES[@]}"; do
    #basename se queda con el nombre final del path
    #p.e. de amd/samples/memoryread_math -> memoryread_math
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
done