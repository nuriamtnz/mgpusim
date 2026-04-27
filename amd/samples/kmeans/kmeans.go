package main

import (
	"flag"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/heteromark/kmeans"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

var points = flag.Int("points", 1024, "The number of points.")
var clusters = flag.Int("clusters", 5, "The number of clusters.")
var features = flag.Int("features", 32,
	"The number of features for each point.")
var maxIter = flag.Int("max-iter", 5,
	"The maximum number of iterations to run")

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
    // Puntos: points*features + Centroides: clusters*features
    pointsData := (*points) * (*features)
    clusterData := (*clusters) * (*features)
    dataSize := uint64((pointsData + clusterData) * 4)  // 4 bytes por float32
    writearound.SetDataSize(dataSize)

	runner := new(runner.Runner).Init()

	benchmark := kmeans.NewBenchmark(runner.Driver())
	benchmark.NumPoints = *points
	benchmark.NumClusters = *clusters
	benchmark.NumFeatures = *features
	benchmark.MaxIter = *maxIter

	runner.AddBenchmark(benchmark)

	runner.Run()
}
