import random


def create_quantum_token(
    n_qubits: int = 20,
    trap_ratio: float = 0.3,
) -> dict:
    """Create a BB84-style quantum token representation."""

    if n_qubits <= 0:
        raise ValueError("n_qubits must be positive.")

    if not 0 <= trap_ratio <= 1:
        raise ValueError("trap_ratio must be between 0 and 1.")

    trap_count = int(n_qubits * trap_ratio)

    return {
        "n": n_qubits,
        "traps": random.sample(
            range(n_qubits),
            trap_count,
        ),
        "bases": {
            index: random.choice(["Z", "X"])
            for index in range(n_qubits)
        },
        "values": {
            index: random.choice([0, 1])
            for index in range(n_qubits)
        },
    }