package main

import (
	"flag"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/amdappsdk/nbody"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

var numIter = flag.Int("iter", 8, "The number of iterations to run.")
var particles = flag.Int("particles", 1024, "The number of particles in the body.")

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
    // Cada partícula: posición (x,y,z) + velocidad (vx,vy,vz) = 6 floats
    numParticles := *particles
    dataSize := uint64(numParticles * 6 * 4)  // 6 floats x 4 bytes
    writearound.SetDataSize(dataSize)

	runner := new(runner.Runner).Init()

	benchmark := nbody.NewBenchmark(runner.Driver())
	benchmark.NumIterations = int32(*numIter)
	benchmark.NumParticles = int32(*particles)

	runner.AddBenchmark(benchmark)

	runner.Run()
}
