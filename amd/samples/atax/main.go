package main

import (
	"flag"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/polybench/atax"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

var xFlag = flag.Int("x", 4096, "The width of the matrix.")
var yFlag = flag.Int("y", 4096, "The height of the matrix.")

func main() {
	flag.Parse()
	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
	// Matriz A (NX x NY) + vector x (NX) + vector y (NY) + vector tmp (NX)
    nx := *xFlag
    ny := *yFlag
	dataSize := uint64((nx*ny + nx + ny + nx)* 4)   // 4 bytes por float32
	writearound.SetDataSize(dataSize) //establece la longitud del array del benchmark.


	runner := new(runner.Runner).Init()

	benchmark := atax.NewBenchmark(runner.Driver())
	benchmark.NX = *xFlag
	benchmark.NY = *yFlag

	runner.AddBenchmark(benchmark)

	runner.Run()
}
