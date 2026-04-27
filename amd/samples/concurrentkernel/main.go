package main

import (
	"flag"

	_ "net/http/pprof"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/amdappsdk/bitonicsort"
	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/heteromark/fir"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Suma de ambos benchmarks
    firLength := 10240
    bsLength := 64
    dataSize := uint64((firLength + bsLength) * 4)  // 4 bytes aprox
    writearound.SetDataSize(dataSize)

	runner := new(runner.Runner).Init()

	firBenchmark := fir.NewBenchmark(runner.Driver())
	firBenchmark.Length = 10240
	firBenchmark.SelectGPU([]int{1})

	bsBenchmark := bitonicsort.NewBenchmark(runner.Driver())
	bsBenchmark.Length = 64
	bsBenchmark.SelectGPU([]int{1})

	runner.AddBenchmarkWithoutSettingGPUsToUse(firBenchmark)
	runner.AddBenchmarkWithoutSettingGPUsToUse(bsBenchmark)

	runner.Run()
}
