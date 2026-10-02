import random

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def verify_token(
    token: dict,
    malicious: bool = False,
) -> dict:
    """
    Verify token trap qubits using Qiskit Aer simulation.

    The token uses two BB84-style bases:

    - Z: computational basis
    - X: Hadamard basis

    During verification, the corresponding basis transformation
    is applied before measurement so that the encoded value can
    be compared correctly.

    This is an educational simulation of a quantum-token protocol.
    """

    n_qubits = int(token["n"])
    traps = token["traps"]

    if not traps:
        return {
            "valid": True,
            "error_rate": 0.0,
            "errors": 0,
            "traps": 0,
            "malicious": malicious,
        }

    circuit = QuantumCircuit(
        n_qubits,
        n_qubits,
    )

    # -------------------------------------------------------------
    # Prepare the token states.
    # -------------------------------------------------------------

    for index in range(n_qubits):

        # Encode the classical bit.
        if token["values"][index] == 1:
            circuit.x(index)

        # Encode an X-basis state.
        if token["bases"][index] == "X":
            circuit.h(index)

    # -------------------------------------------------------------
    # Simulate an attacker disturbing the token.
    # -------------------------------------------------------------

    if malicious:

        for index in range(n_qubits):

            if random.random() < 0.3:
                circuit.h(index)

    # -------------------------------------------------------------
    # Apply the inverse basis transformation.
    #
    # Z basis:
    #     No transformation is required.
    #
    # X basis:
    #     Apply H again to rotate the state back into the
    #     computational basis before measurement.
    # -------------------------------------------------------------

    for index in range(n_qubits):

        if token["bases"][index] == "X":
            circuit.h(index)

    # -------------------------------------------------------------
    # Measure all qubits.
    # -------------------------------------------------------------

    circuit.measure(
        range(n_qubits),
        range(n_qubits),
    )

    simulator = AerSimulator()

    compiled = transpile(
        circuit,
        simulator,
    )

    result = simulator.run(
        compiled,
        shots=1,
    ).result()

    measured = list(
        result.get_counts().keys()
    )[0][::-1]

    # -------------------------------------------------------------
    # Check trap qubits.
    # -------------------------------------------------------------

    errors = sum(
        int(measured[index])
        != token["values"][index]
        for index in traps
    )

    error_rate = errors / len(traps)

    return {
        "valid": errors == 0,
        "error_rate": error_rate,
        "errors": errors,
        "traps": len(traps),
        "malicious": malicious,
    }