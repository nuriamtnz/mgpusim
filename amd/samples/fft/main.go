package main

import (
	"flag"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/shoc/fft"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

var mb = flag.Int("MB", 8, "data size (in megabytes)")
var passes = flag.Int("passes", 2, "number of passes")

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
    dataSize := uint64(*mb * 1024 * 1024)  // Convertir MB a bytes
    writearound.SetDataSize(dataSize)

	runner := new(runner.Runner).Init()

	benchmark := fft.NewBenchmark(runner.Driver())
	benchmark.Bytes = int32(*mb)
	benchmark.Passes = int32(*passes)

	runner.AddBenchmark(benchmark)

	runner.Run()
}
