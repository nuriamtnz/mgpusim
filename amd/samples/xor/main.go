package main

import (
	"flag"
	"math/rand"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/dnn/training_benchmarks/xor"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

func main() {
	rand.Seed(1)

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
    // XOR: problema simple, 4 ejemplos de entrenamiento (2 entradas cada uno)
    dataSize := uint64(4 * 2 * 4)  // 4 ejemplos x 2 entradas x 4 bytes
    writearound.SetDataSize(dataSize)

	flag.Parse()

	runner := new(runner.Runner).Init()

	benchmark := xor.NewBenchmark(runner.Driver())

	runner.AddBenchmark(benchmark)

	runner.Run()
}
