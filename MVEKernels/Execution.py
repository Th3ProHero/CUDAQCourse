import cudaq
import numpy as np
from cudaq import spin

# Definir el número de qubits
qubit_count = 2

# Configurar el target de simulación
cudaq.set_target("qpp-cpu")

# 🔹 Kernel con medición (Para sample)
@cudaq.kernel
def kernel_with_measurement(qubit_count: int):
    qvector = cudaq.qvector(qubit_count)
    h(qvector[0])  
    for i in range(1, qubit_count):
        x.ctrl(qvector[0], qvector[i])
    mz(qvector)  # Medición solo para sample()

# 🔹 Kernel sin medición (Para observe y get_state)
@cudaq.kernel
def kernel_no_measurement(qubit_count: int):
    qvector = cudaq.qvector(qubit_count)
    h(qvector[0])  
    for i in range(1, qubit_count):
        x.ctrl(qvector[0], qvector[i])
    # ❌ No hay medición aquí (necesario para observe y get_state)

# 🔹 Dibujar los circuitos
print("Circuito con medición (Sample):")
print(cudaq.draw(kernel_with_measurement, qubit_count))

print("\nCircuito sin medición (Observe / Get State):")
print(cudaq.draw(kernel_no_measurement, qubit_count))

# 🔹 Ejecución con sample() (Mide y obtiene distribuciones de estados)
print("\nEjecución con Sample (Distribución de estados):")
sample_result = cudaq.sample(kernel_with_measurement, qubit_count, shots_count=1000)
print(sample_result)

# 🔹 Ejecución con observe() (Calcula el valor esperado del Hamiltoniano)
print("\nEjecución con Observe (Valor esperado del Hamiltoniano):")
hamiltonian = spin.z(0) + spin.y(1) + spin.x(0) * spin.z(0)
observe_result = cudaq.observe(kernel_no_measurement, hamiltonian, qubit_count).expectation()
print('<H> =', observe_result)

# 🔹 Ejecución con get_state() (Obtiene el estado cuántico completo)
print("\nEjecución con Get State (Estado cuántico completo):")
state_result = cudaq.get_state(kernel_no_measurement, qubit_count)
print(np.array(state_result))

# 🔹 Paralelización con observe_async()
print("\nEjecución Asíncrona con Observe (Paralelización con QPUs/GPU):")
hamiltonian_1 = spin.x(0) + spin.y(1) + spin.z(0) * spin.y(1)
observe_async_result = cudaq.observe_async(kernel_no_measurement, hamiltonian_1, qubit_count, qpu_id=0)
print(observe_async_result.get().expectation())

# 🔹 Paralelización con sample_async()
print("\nEjecución Asíncrona con Sample (Distribución de estados en paralelo):")
sample_async_result = cudaq.sample_async(kernel_with_measurement, qubit_count, shots_count=1000)
print(sample_async_result.get())

# 🔹 Paralelización con get_state_async()
print("\nEjecución Asíncrona con Get State (Estado cuántico en paralelo):")
get_state_async_result = cudaq.get_state_async(kernel_no_measurement, qubit_count)
print(np.array(get_state_async_result.get()))
