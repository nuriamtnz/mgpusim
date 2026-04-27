package main

import (
	"flag"

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/dnn/training_benchmarks/vgg16"
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner"
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
)

var epochFlag = flag.Int("epoch", 1, "Number of epoch to run.")
var maxBatchPerEpochFlag = flag.Int("max-batch-per-epoch", 2,
	"Number of epochs to run.")
var batchSizeFlag = flag.Int("batch-size", 8,
	"Number of images per batch")
var enableTestingFlag = flag.Bool("enable-testing", false,
	"If set, the trainer will evaluate the trained model after each epoch")
var enableVerification = flag.Bool("enable-verification", false,
	`If set, all tenser operations will be verified against CPU results. Do not 
turn on if you care about the final results. This flag will introduce extra
GPU-to-CPU memory copies.`)

func main() {
	flag.Parse()

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
    // VGG16: imágenes típicamente 224x224x3 (RGB)
    imageSize := 224 * 224 * 3
    batchSize := *batchSizeFlag
    dataSize := uint64(batchSize * imageSize * 4)  // 4 bytes por float32
    writearound.SetDataSize(dataSize)

	runner := new(runner.Runner).Init()

	benchmark := vgg16.NewBenchmark(runner.Driver())
	benchmark.Epoch = *epochFlag
	benchmark.MaxBatchPerEpoch = *maxBatchPerEpochFlag
	benchmark.BatchSize = *batchSizeFlag
	benchmark.EnableTesting = *enableTestingFlag
	benchmark.EnableVerification = *enableVerification

	runner.AddBenchmark(benchmark)

	runner.Run()
}
