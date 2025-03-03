import cudaq

@cudaq.kernel
def kernel():
    qubits = cudaq.qvector(2)  # 1️⃣ Creamos 2 qubits en |00⟩
    mz()  # 2️⃣ Medimos en la base Z (toda la memoria cuántica)

print(cudaq.sample(kernel))  # 3️⃣ Ejecutamos el circuito

#Ejemplo 2:
@cudaq.kernel
def kernel():
    qubits_a = cudaq.qvector(2)  # 1️⃣ Creamos 2 qubits
    qubit_b = cudaq.qubit()      # 2️⃣ Creamos un qubit adicional

    mz(qubits_a)  # 3️⃣ Medimos los 2 primeros en la base Z
    mx(qubit_b)   # 4️⃣ Medimos el tercer qubit en la base X

print(cudaq.sample(kernel))  # 5️⃣ Ejecutamos el circuito

#Mediciones en medio del circuito.
@cudaq.kernel
def kernel():
    q = cudaq.qvector(2)  # 1️⃣ Creamos 2 qubits

    h(q[0])        # 2️⃣ Aplicamos Hadamard al primer qubit (superposición)
    b0 = mz(q[0])  # 3️⃣ Medimos el primer qubit y guardamos el resultado
    reset(q[0])    # 4️⃣ Reiniciamos el primer qubit a |0⟩
    x(q[0])        # 5️⃣ Aplicamos X al primer qubit (lo cambia a |1⟩)

    if b0:         # 6️⃣ Si el resultado de la medición fue 1...
        h(q[1])    #     Aplicamos Hadamard al segundo qubit

print(cudaq.sample(kernel))  # 7️⃣ Ejecutamos el circuito
