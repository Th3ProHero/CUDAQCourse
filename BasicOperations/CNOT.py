import cudaq


@cudaq.kernel
def kernel():
    # 2 qubits both initialized to the ground/ zero state.
    qvector = cudaq.qvector(2)

    x(qvector[0])

    # Controlled-not gate operation.
    x.ctrl(qvector[0], qvector[1])

    mz(qvector[0])
    mz(qvector[1])


result = cudaq.sample(kernel)
print(result)