package main

import (
	"flag"
	"log"
	"math"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/shoc/bfs"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

var path = flag.String("load-graph", "", "Path to file from which graph to be loaded. "+
	"Currently only supports text files.\nThe graph is considered directed and edges are "+
	"needed to described in single line \nwith format: <node from> <node to>. You can add "+
	"comment preceded by #")
var numNode = flag.Int("node", 64, "The width of the matrix.")
var degree = flag.Int("degree", 3, "The height of the matrix.")
var maxDepth = flag.Int("depth", 0, "The max depth to search, 0 means unlimited")

func main() {
	flag.Parse()
	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
    // Aproximación: nodos + aristas (numNode * degree)
    numNodes := *numNode
    numEdges := numNodes * (*degree)
    dataSize := uint64((numNodes*8 + numEdges*8))  // 8 bytes aprox por entrada
    writearound.SetDataSize(dataSize)

	runner := new(runner.Runner).Init()

	benchmark := bfs.NewBenchmark(runner.Driver())
	benchmark.Path = *path
	benchmark.NumNode = *numNode
	benchmark.Degree = *degree
	if *maxDepth == 0 {
		*maxDepth = math.MaxInt32
	}
	benchmark.MaxDepth = *maxDepth

	if (isFlagPassed("degree") || isFlagPassed("node")) && isFlagPassed("load-graph") {
		log.Panic("cannot specify number or degree of nodes for manually provided graph")
	}

	runner.AddBenchmark(benchmark)

	runner.Run()
}

func isFlagPassed(name string) bool {
	found := false
	flag.Visit(func(f *flag.Flag) {
		if f.Name == name {
			found = true
		}
	})
	return found
}
