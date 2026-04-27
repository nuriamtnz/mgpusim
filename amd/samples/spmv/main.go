package main

import (
	"flag"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/shoc/spmv"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

// Dim is dimension
var Dim = flag.Int("dim", 128, "The number of rows in the input matrix.")

// Sparsity is sparsity
var Sparsity = flag.Float64("sparsity", 0.01,
	"The ratio between non-zero elements to all the elelements in the matrix")

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
    dim := *Dim
    numNonZero := int(float64(dim*dim) * (*Sparsity))
    // Valores no cero + índices + vector
    dataSize := uint64((numNonZero*2 + dim) * 4)  // 4 bytes aprox
    writearound.SetDataSize(dataSize)

	runner := new(runner.Runner).Init()

	benchmark := spmv.NewBenchmark(runner.Driver())
	benchmark.Dim = int32(*Dim)
	benchmark.Sparsity = *Sparsity

	runner.AddBenchmark(benchmark)

	runner.Run()
}
