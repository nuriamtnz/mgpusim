package main

import (
	"flag"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/rodinia/nw"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

var length = flag.Int("length", 64, "The number bases in the gene sequence")

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
    // Needleman-Wunsch: matriz length x length
    len := *length
    dataSize := uint64(len * len * 4)  // 4 bytes por int32
    writearound.SetDataSize(dataSize)

	runner := new(runner.Runner).Init()

	benchmark := nw.NewBenchmark(runner.Driver())
	benchmark.SetLength(*length)

	runner.AddBenchmark(benchmark)

	runner.Run()
}
