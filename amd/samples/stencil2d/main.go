package main

import (
	"flag"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/shoc/stencil2d"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

var numRow = flag.Int("row", 64, "The number of rows in the input matrix.")
var numCol = flag.Int("col", 64, "The number of columns in the input matrix.")
var numIter = flag.Int("iter", 5, "The number of iterations to run.")

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
    // Matriz: (numRow+2) x (numCol+2)
    rows := *numRow + 2
    cols := *numCol + 2
    dataSize := uint64(rows * cols * 4)  // 4 bytes por float32
    writearound.SetDataSize(dataSize)

	runner := new(runner.Runner).Init()

	benchmark := stencil2d.NewBenchmark(runner.Driver())
	benchmark.NumIteration = *numIter
	benchmark.NumRows = *numRow + 2
	benchmark.NumCols = *numCol + 2

	runner.AddBenchmark(benchmark)

	runner.Run()
}
