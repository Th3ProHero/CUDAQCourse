import cudaq

# Definir el kernel cuántico
@cudaq.kernel
def kernel(qubit_count: int):
    # Asignar qubits
    qvector = cudaq.qvector(qubit_count)
    # Aplicar Hadamard al primer qubit para crear superposición
    h(qvector[0])
    # Aplicar CNOT en cadena para generar entrelazamiento
    for qubit in range(qubit_count - 1):
        x.ctrl(qvector[qubit], qvector[qubit + 1])
    # Medir los qubits
    mz(qvector)

# Especificar el número de qubits y visualizar el circuito
qubit_count = 10
print(cudaq.draw(kernel, qubit_count))  # Dibujar el circuito

# Ejecutar el kernel y obtener resultados de medición
results = cudaq.sample(kernel, qubit_count)

# Deberíamos ver una distribución aproximadamente 50/50 entre los estados |00> y |11>
print("Measurement distribution: " + str(results))
