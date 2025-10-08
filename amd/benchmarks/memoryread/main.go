// Package vectoradd implements the addition of a vector as a benchmark.
package memoryread

import (
	"log"

	// embed hsaco files
	_ "embed"

	"github.com/sarchlab/mgpusim/v4/amd/driver"
	"github.com/sarchlab/mgpusim/v4/amd/insts"
	"github.com/sarchlab/mgpusim/v4/amd/kernels"
)

// KernelArgs defines kernel arguments
type KernelArgs struct {
	Input               driver.Ptr
	Output              driver.Ptr
	HiddenGlobalOffsetX int64
	HiddenGlobalOffsetY int64
	HiddenGlobalOffsetZ int64
}

// Benchmark defines a benchmark
type Benchmark struct {
	driver  *driver.Driver
	context *driver.Context
	gpus    []int
	hsaco   *insts.HsaCo

	Length      int
	inputData   []float32
	outputData  []float32
	gInputData  driver.Ptr
	gOutputData driver.Ptr

	useUnifiedMemory bool
}

//go:embed kernels.hsaco
var hsacoBytes []byte

// NewBenchmark returns a benchmark
func NewBenchmark(driver *driver.Driver) *Benchmark {
	b := new(Benchmark)

	b.driver = driver
	b.context = driver.Init()
	b.hsaco = kernels.LoadProgramFromMemory(hsacoBytes, "vectorRead")

	return b
}

// SelectGPU selects GPU
func (b *Benchmark) SelectGPU(gpus []int) {
	b.gpus = gpus
}

// SetUnifiedMemory uses Unified Memory
func (b *Benchmark) SetUnifiedMemory() {
	b.useUnifiedMemory = true
}

// Run runs
func (b *Benchmark) Run() {
	b.driver.SelectGPU(b.context, b.gpus[0])
	b.initMem()
	b.exec()
}

func (b *Benchmark) initMem() {
	if b.useUnifiedMemory {
		b.gInputData = b.driver.AllocateUnifiedMemory(b.context, uint64(b.Length*4))
		b.gOutputData = b.driver.AllocateUnifiedMemory(b.context, uint64(b.Length*4))
	} else {
		b.gInputData = b.driver.AllocateMemory(b.context, uint64(b.Length*4))
		b.driver.Distribute(b.context, b.gInputData, uint64(b.Length*4), b.gpus)
		b.gOutputData = b.driver.AllocateMemory(b.context, uint64(b.Length*4))
		b.driver.Distribute(b.context, b.gOutputData, uint64(b.Length*4), b.gpus)
	}

	b.inputData = make([]float32, b.Length)
	b.outputData = make([]float32, b.Length)
	for i := 0; i < b.Length; i++ {
		b.inputData[i] = float32(i)
		b.outputData[i] = -1.0
	}

	b.driver.MemCopyH2D(b.context, b.gInputData, b.inputData)
}

func (b *Benchmark) exec() {
	queues := make([]*driver.CommandQueue, len(b.gpus))

	for i, gpu := range b.gpus {
		b.driver.SelectGPU(b.context, gpu)
		q := b.driver.CreateCommandQueue(b.context)
		queues[i] = q

		if b.Length > 512 || b.Length%64 != 0 {
			log.Panicf("Length must be <= 512 and multiple of 64")
		}

		kernArg := KernelArgs{
			b.gInputData,
			b.gOutputData,
			0, 0, 0, // HiddenGlobalOffsetX/Y/Z
		}

		b.driver.EnqueueLaunchKernel(
			q,
			b.hsaco,
			[3]uint32{uint32(b.Length), 1, 1}, // Global grid size (number of WorkItems)
			[3]uint16{uint16(b.Length), 1, 1}, // Work-group size (64 workItems = 1 wavefront).
			&kernArg,
		)
	}

	for _, q := range queues {
		b.driver.DrainCommandQueue(q)
	}

	b.driver.MemCopyD2H(b.context, b.outputData, b.gOutputData)
}

// Verify verifies
func (b *Benchmark) Verify() {
	for i := 0; i < b.Length; i++ {
		if b.outputData[i] != b.inputData[i] {
			log.Panicf("Mismatch at %d, input %f, output %f", i, b.inputData[i], b.outputData[i])
		}
	}

	log.Printf("Passed!\n")
}
