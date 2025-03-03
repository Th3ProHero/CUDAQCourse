import sys

import cudaq
import numpy as np

@cudaq.kernel
def kernel(angles: np.ndarray):
    qubit = cudaq.qubit()
    rz(angles[0], qubit)  # Rotación alrededor del eje Z
    rx(angles[1], qubit)  # Rotación alrededor del eje X
    rz(angles[2], qubit)  # Otra rotación alrededor del eje Z

# Generamos un estado cuántico con ángulos aleatorios
rng = np.random.default_rng(seed=11)
angleList = rng.random(3) * 2 * np.pi

# Convertimos el estado a una esfera de Bloch
blochSphere = cudaq.add_to_bloch_sphere(cudaq.get_state(kernel, angleList))

# Mostramos la esfera de Bloch
cudaq.show(blochSphere)

blochSphereList = []
for _ in range(4):
    angleList = rng.random(3) * 2 * np.pi
    sph = cudaq.add_to_bloch_sphere(cudaq.get_state(kernel, angleList))
    blochSphereList.append(sph)

# Mostrar las primeras dos esferas en una sola fila
cudaq.show(blochSphereList[:2], nrows=1, ncols=2)

# Mostrar todas las esferas en una grilla 2x2
cudaq.show(blochSphereList, nrows=2, ncols=2)

import qutip

blochSphere = qutip.Bloch()
for _ in range(10):
    angleList = rng.random(3) * 2 * np.pi
    sph = cudaq.add_to_bloch_sphere(cudaq.get_state(kernel, angleList), blochSphere)

# Mostrar la esfera de Bloch con múltiples estados
blochSphere.show()

@cudaq.kernel
def circuito_visual():
    q = cudaq.qvector(3)  # Creamos 3 qubits
    h(q[0])  # Puerta Hadamard en q0
    cx(q[0], q[1])  # CNOT controlado por q0 y aplicado en q1
    x(q[2])  # Puerta X en q2
    mz(q)  # Medición en todos los qubits

# Dibujar el circuito en formato ASCII
print(cudaq.draw(circuito_visual))

print(cudaq.draw('latex', circuito_visual))
