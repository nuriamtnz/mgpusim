package main

import (
	"flag"

	"github.com/sarchlab/akita/v4/mem/cache/writearound"
	nuria_mac_temporal "github.com/sarchlab/mgpusim/v4/amd/benchmarks/fma"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
)

// Tensor Parameters
var LENGTH = flag.Int("length", 25600, "Specify the size of the vector (must be a multiple of 512).")
var A = flag.Float64("a", 1.5, "Coefficient A for computation (x = a * x + b)")
var B = flag.Float64("b", 0.5, "Coefficient B for computation (x = a * x + b)")
var COMPUTE_ITERS = flag.Uint("compute_iters", 10, "Number of compute iterations")

// cus * workgrpup_size * wavefrontpool_size = total amount of threads

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
	dataSize := uint64(*LENGTH * 4)   // 4 bytes por float32
	writearound.SetDataSize(dataSize) //establece la longitud del array del benchmark.

	runner := new(runner.Runner).Init()

	benchmark := nuria_mac_temporal.NewBenchmark(runner.Driver(), *LENGTH, float32(*A), float32(*B), uint32(*COMPUTE_ITERS))

	runner.AddBenchmark(benchmark)

	runner.Run()
}
