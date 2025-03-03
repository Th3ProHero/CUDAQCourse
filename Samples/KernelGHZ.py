import cudaq
import sys
import timeit
from cudaq import spin

# -------------------------------
# 1. Definir el Kernel GHZ
# -------------------------------
@cudaq.kernel
def kernel(qubit_count: int):
    # Asignar qubits
    qvector = cudaq.qvector(qubit_count)
    # Superposición en el primer qubit
    h(qvector[0])
    # Entrelazamiento con CNOT
    for qubit in range(qubit_count - 1):
        x.ctrl(qvector[qubit], qvector[qubit + 1])
    # Medir el estado final
    mz(qvector)


# -------------------------------
# 2. Visualizar el circuito
# -------------------------------
qubit_count = 2  # Número de qubits
print("\n🔹 Circuito generado:")
print(cudaq.draw(kernel, qubit_count))

# -------------------------------
# 3. Ejecución con sample()
# -------------------------------
results = cudaq.sample(kernel, qubit_count)
print("\n🔹 Distribución de mediciones (1000 shots):")
print(results)

# Ejecutando con más shots
results_high_shots = cudaq.sample(kernel, qubit_count, shots_count=10000)
print("\n🔹 Distribución con 10,000 mediciones:")
print(results_high_shots)

# -------------------------------
# 4. Obtener el resultado más probable
# -------------------------------
most_probable_result = results.most_probable()
probability = results.probability(most_probable_result)
print("\n🔹 Resultado más probable:", most_probable_result)
print("🔹 Probabilidad medida:", probability)

# -------------------------------
# 5. Paralelización con sample_async()
# -------------------------------
@cudaq.kernel
def kernel2(qubit_count: int):
    qvector = cudaq.qvector(qubit_count)
    h(qvector)  # Superposición total
    mz(qvector)

num_gpus = cudaq.num_available_gpus()
if num_gpus > 1:
    cudaq.set_target("nvidia", option="mqpu")
    result_1 = cudaq.sample_async(kernel, qubit_count, shots_count=1000, qpu_id=0)
    result_2 = cudaq.sample_async(kernel2, qubit_count, shots_count=1000, qpu_id=1)
else:
    result_1 = cudaq.sample_async(kernel, qubit_count, shots_count=1000, qpu_id=0)
    result_2 = cudaq.sample_async(kernel2, qubit_count, shots_count=1000, qpu_id=0)

print("\n🔹 Distribución de mediciones en paralelo:")
print("Kernel 1:", result_1.get())
print("Kernel 2:", result_2.get())

# -------------------------------
# 6. Expectation Value con observe()
# -------------------------------
operator = spin.z(0)  # Operador Pauli-Z en el qubit 0
print("\n🔹 Operador de medición:", operator)

# Kernel para expectation value (sin medición)
@cudaq.kernel
def kernel_expectation():
    qubit = cudaq.qubit()
    h(qubit)

result_observe = cudaq.observe(kernel_expectation, operator)
print("\n🔹 Valor esperado:", result_observe.expectation())

# Con más shots
result_observe_high_shots = cudaq.observe(kernel_expectation, operator, shots_count=1000)
print("\n🔹 Valor esperado con 1000 shots:", result_observe_high_shots.expectation())

# -------------------------------
# 7. Comparación CPU vs GPU
# -------------------------------
code_to_time = 'cudaq.sample(kernel, qubit_count, shots_count=1000000)'
qubit_count = int(sys.argv[1]) if 1 < len(sys.argv) else 25

# En CPU
cudaq.set_target('qpp-cpu')
print("\n⏳ CPU time:")
print(timeit.timeit(stmt=code_to_time, globals=globals(), number=1))

# En GPU (si hay disponible)
if cudaq.num_available_gpus() > 0:
    cudaq.set_target('nvidia')
    print("\n⚡ GPU time:")
    print(timeit.timeit(stmt=code_to_time, globals=globals(), number=1))
