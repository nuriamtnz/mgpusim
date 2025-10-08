package main

import (
	"flag" //paquete que permite el manejo de argumentos pasados por la linea de comandos

	"github.com/sarchlab/mgpusim/v4/amd/benchmarks/memoryread" //benchmark que lee datos desde la memoria,
	// simula el acceso a memoria en una GPU.
	"github.com/sarchlab/mgpusim/v4/amd/samples/runner" //contiene la clase Runner que maneja la ejecucion del
	// benchmark y la simulación de la GPU.
)

var numData = flag.Int("length", 64, "The length of the array.") //longitud predeterminada del array del benchmark.

func main() {
	flag.Parse() //procesa los argumentos pasados por la linea de comandos.

	runner := new(runner.Runner).Init() //creación y inicialización de un objeto Runner.

	benchmark := memoryread.NewBenchmark(runner.Driver()) //Driver() obtiene el controlador de GPU simulado del objeto Runner.
	benchmark.Length = *numData                           //establece la longitud del array del benchmark.

	runner.AddBenchmark(benchmark) //agrega el benchmark recién creado al Runner.

	runner.Run()
}
