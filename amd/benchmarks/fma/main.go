// Package vectoradd implements the addition of a vector as a benchmark.
package nuria_mac_temporal

import (
	"log"
	"math/rand"

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
	Stride              uint64
	Length              uint64
	A                   float32
	B                   float32
	ComputeIterations   uint32
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

	// Vector data
	Length      int
	inputData   []float32
	outputData  []float32
	gInputData  driver.Ptr
	gOutputData driver.Ptr

	// Compute parameters
	A                 float32
	B                 float32
	ComputeIterations uint32

	useUnifiedMemory bool
}

//go:embed kernels.hsaco
var hsacoBytes []byte

// NewBenchmark returns a benchmark
func NewBenchmark(driver *driver.Driver, length int, a_val, b_val float32, computeIterations uint32) *Benchmark {
	b := new(Benchmark)

	b.driver = driver
	b.context = driver.Init()
	b.hsaco = kernels.LoadProgramFromMemory(hsacoBytes, "memoryread_loop")
	b.Length = length
	b.A = a_val
	b.B = b_val
	b.ComputeIterations = computeIterations

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
		b.gOutputData = b.driver.AllocateMemory(b.context, uint64(b.Length*4))
	}

	b.inputData = make([]float32, b.Length)
	b.outputData = make([]float32, b.Length)

	for i := 0; i < b.Length; i++ {
		b.inputData[i] = float32(rand.Intn(100))
	}

	b.driver.MemCopyH2D(b.context, b.gInputData, b.inputData)
}

func (b *Benchmark) exec() {
	b.driver.SelectGPU(b.context, b.gpus[0])
	q := b.driver.CreateCommandQueue(b.context)

	if b.Length%512 != 0 {
		log.Panicf("Length must be multiple of 512 (to gain temporal locality)")
	}

	kernArg := KernelArgs{
		b.gInputData,
		b.gOutputData,
		uint64(512),
		uint64(b.Length),
		b.A,
		b.B,
		b.ComputeIterations,
		0, 0, 0,
	}

	b.driver.EnqueueLaunchKernel(
		q,
		b.hsaco,
		[3]uint32{uint32(512), 1, 1}, // Global grid size (number of WorkItems)
		[3]uint16{uint16(512), 1, 1}, // Work-group size (how many workitems a workgroup will have, assuming 64 workItems = 1 wavefront)
		&kernArg,
	)
	b.driver.DrainCommandQueue(q)

	b.driver.MemCopyD2H(b.context, b.outputData, b.gOutputData)
}

// Verify verifies
func (b *Benchmark) Verify() {
	for i := 0; i < b.Length; i++ {
		// Calculate expected output: apply compute_iterations of x = a * x + b
		expected := b.inputData[i]
		for j := uint32(0); j < b.ComputeIterations; j++ {
			expected = b.A*expected + b.B
		}
		if b.outputData[i] != expected {
			log.Panicf("Mismatch at %d, expected %f, output %f", i, expected, b.outputData[i])
		}
	}

	log.Printf("Passed!\n")
}
