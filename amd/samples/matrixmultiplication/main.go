package main

import (
	"flag"

	_ "net/http/pprof"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/amdappsdk/matrixmultiplication"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

var xFlag = flag.Uint("x", 64, "The height of the first matrix.")
var yFlag = flag.Uint("y", 64, "The width of the first matrix and the height of the second matrix.")
var zFlag = flag.Uint("z", 64, "The width of the second matrix.")

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
    // Matriz A (X x Y) + Matriz B (Y x Z) + Matriz C (X x Z)
    x := uint64(*xFlag)
    y := uint64(*yFlag)
    z := uint64(*zFlag)
    dataSize := (x*y + y*z + x*z) * 4  // 4 bytes por float32
    writearound.SetDataSize(dataSize)

	runner := new(runner.Runner).Init()

	benchmark := matrixmultiplication.NewBenchmark(runner.Driver())
	benchmark.X = uint32(*xFlag)
	benchmark.Y = uint32(*yFlag)
	benchmark.Z = uint32(*zFlag)

	runner.AddBenchmark(benchmark)

	runner.Run()
}
