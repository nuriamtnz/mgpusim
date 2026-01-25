package main

import (
	"flag"

	"github.com/sarchlab/akita/v4/mem/cache/writearound"
	nuria_memoryread_loop_temporal "github.com/sarchlab/mgpusim/v4/amd/benchmarks/memoryread_temporal"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
)

// Tensor Parameters
var LENGTH = flag.Int("length", 25600, "Specify the size of the vector (must be a multiple of 512).")

// cus * workgrpup_size * wavefrontpool_size = total amount of threads

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
	dataSize := uint64(*LENGTH * 4)   // 4 bytes por float32
	writearound.SetDataSize(dataSize) //establece la longitud del array del benchmark.

	runner := new(runner.Runner).Init()

	benchmark := nuria_memoryread_loop_temporal.NewBenchmark(runner.Driver(), *LENGTH)

	runner.AddBenchmark(benchmark)

	runner.Run()
}
