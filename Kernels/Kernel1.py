import cudaq

@cudaq.kernel
def kernel():
    '''
    Este es nuestro primer kernel en CUDA-Q.
    '''
    # Asignamos un qubit al kernel
    qubit = cudaq.qubit()

    # Aplicamos una serie de puertas cuánticas
    h(qubit)  # Puerta Hadamard
    x(qubit)  # Puerta X (NOT cuántico)
    y(qubit)  # Puerta Y
    z(qubit)  # Puerta Z
    t(qubit)  # Puerta T (raíz de Z)
    s(qubit)  # Puerta S (raíz de T)

    # Medimos el qubit en la base computacional
    mz(qubit)

# Ejecutamos el kernel y obtenemos los resultados
print("Ejecutando el kernel cuántico...")

# `cudaq.sample` ejecuta el circuito varias veces para obtener estadísticas
results = cudaq.sample(kernel)

print("Resultados de la medición:")
print(results)
