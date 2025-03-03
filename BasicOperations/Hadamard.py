import cudaq


@cudaq.kernel
def kernel():
    # A single qubit initialized to the ground/ zero state.
    qubit = cudaq.qubit()

    # Apply Hadamard gate to single qubit to put it in equal superposition.
    h(qubit)

    # Measurement operator.
    mz(qubit)


result = cudaq.sample(kernel)
print("Measured |0> with probability " +
      str(result["0"] / sum(result.values())))
print("Measured |1> with probability " +
      str(result["1"] / sum(result.values())))