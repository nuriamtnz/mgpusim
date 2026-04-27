package main

import (
	"flag"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/heteromark/aes"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

var lenInput = flag.Int("length", 65536, "The length of array to sort.")

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
	dataSize := uint64(*lenInput * 4)   // 4 bytes por float32
	writearound.SetDataSize(dataSize) //establece la longitud del array del benchmark.

	runner := new(runner.Runner).Init()

	benchmark := aes.NewBenchmark(runner.Driver())
	benchmark.Length = *lenInput

	runner.AddBenchmark(benchmark)

	runner.Run()
}
