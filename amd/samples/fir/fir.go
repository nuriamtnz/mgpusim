package main

import (
	"flag"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/heteromark/fir"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

var numData = flag.Int("length", 16384, "The number of samples to filter.")

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
    dataSize := uint64(*numData * 4)  // 4 bytes por float32
    writearound.SetDataSize(dataSize)

	runner := new(runner.Runner).Init()

	benchmark := fir.NewBenchmark(runner.Driver())
	benchmark.Length = *numData

	runner.AddBenchmark(benchmark)

	runner.Run()
}
