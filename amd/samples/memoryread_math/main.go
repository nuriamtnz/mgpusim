package main

import (
	"flag" //paquete que permite el manejo de argumentos pasados por la linea de comandos

	//benchmark que lee datos desde la memoria,
	"github.com/sarchlab/akita/v4/mem/cache/writearound"
	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/memoryread_math"

	// simula el acceso a memoria en una GPU.
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner" //contiene la clase Runner que maneja la ejecucion del
	// benchmark y la simulación de la GPU.
)

var numData = flag.Int("length", 512, "The length of the array.") //longitud predeterminada del array del benchmark.

func main() {
	flag.Parse() //procesa los argumentos pasados por la linea de comandos.

	// PREFETCH IMPLEMENTATION NURIA - Informar al caché el tamaño de datos
	dataSize := uint64(*numData * 4)  // 4 bytes por float32
	writearound.SetDataSize(dataSize) //establece la longitud del array del benchmark.

	runner := new(runner.Runner).Init() //creación y inicialización de un objeto Runner.

	benchmark := memoryread_math.NewBenchmark(runner.Driver()) //Driver() obtiene el controlador de GPU simulado del objeto Runner.
	benchmark.Length = *numData                                //establece la longitud del array del benchmark.

	runner.AddBenchmark(benchmark) //agrega el benchmark recién creado al Runner.

	runner.Run()
}
