package main

import (
	"flag"

	"github.com/sarchlab/akita/v4/mem/cache/writearound"
	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/memoryread_loop"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
)

// Tensor Parameters
var LENGTH = flag.Int("length", 1024, "Specify the size of the vector.")

// cus * workgrpup_size * wavefrontpool_size = total amount of threads

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
	dataSize := uint64(*LENGTH * 4)   // 4 bytes por float32
	writearound.SetDataSize(dataSize) //establece la longitud del array del benchmark.

	runner := new(runner.Runner).Init()

	benchmark := memoryread_loop.NewBenchmark(runner.Driver(), *LENGTH)

	runner.AddBenchmark(benchmark)

	runner.Run()
}
