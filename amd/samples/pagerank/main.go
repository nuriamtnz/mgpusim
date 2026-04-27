package main

import (
	"flag"
	"fmt"
	"os"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/heteromark/pagerank"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

var numNode = flag.Int("node", 16, "The number of nodes")
var sparsity = flag.Float64("sparsity", 0.001, "The sparsity of the graph")
var maxIterations = flag.Int("iterations", 16, "The number of iterations")

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
    numN := *numNode  // Declara una variable LOCAL, no redelares
    if *sparsity > 1 {
        *sparsity = 1
    }
    numConn := int(float64(numN*numN) * *sparsity)
    if numConn < numN {
        numConn = numN
    }
    fmt.Fprintf(os.Stderr, "Number node %d, number connection %d\n", numN, numConn)

    // Nodos + Conexiones (aristas)
    dataSize := uint64((numN + numConn) * 8)  // 8 bytes aprox por entrada
    writearound.SetDataSize(dataSize)

	runner := new(runner.Runner).Init()

	benchmark := pagerank.NewBenchmark(runner.Driver())
	benchmark.NumNodes = uint32(numN)
	benchmark.NumConnections = uint32(numConn)
	benchmark.MaxIterations = uint32(*maxIterations)

	runner.AddBenchmark(benchmark)

	runner.Run()
}
