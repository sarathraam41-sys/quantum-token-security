"""
Trap-Ratio Security Experiment

Studies how the proportion of trap qubits affects attack detection.

The experiment compares:

1. Theoretical detection probability
2. Monte Carlo experimental detection probability
3. Attack success probability
4. Average disturbance

A small Qiskit/Aer validation is included separately to demonstrate
the underlying quantum circuit mechanism.

This is an educational security prototype, not a physical quantum
money implementation.
"""

import random
from pathlib import Path

import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


# ---------------------------------------------------------------------
# Experiment configuration
# ---------------------------------------------------------------------

N_QUBITS = 20

TRAP_RATIOS = [
    0.1,
    0.2,
    0.3,
    0.4,
    0.5,
]

TRIALS = 1000

# Probability that an attacker guesses a trap's basis correctly.
ATTACKER_BASIS_GUESS_PROBABILITY = 0.5

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "outputs"


# ---------------------------------------------------------------------
# Theoretical model
# ---------------------------------------------------------------------

def theoretical_detection_probability(
    trap_count: int,
) -> float:
    """
    Calculate the theoretical probability of detecting an attack.

    An attacker has a 50% probability of correctly guessing the basis
    of each trap.

    Therefore:

        P(no detection) = p_correct ^ number_of_traps

        P(detection) = 1 - P(no detection)
    """

    if trap_count <= 0:
        return 0.0

    probability_no_detection = (
        ATTACKER_BASIS_GUESS_PROBABILITY
        ** trap_count
    )

    return 1.0 - probability_no_detection


# ---------------------------------------------------------------------
# Statistical simulation
# ---------------------------------------------------------------------

def simulate_attack(
    trap_ratio: float,
    n_qubits: int = N_QUBITS,
) -> dict:
    """
    Simulate an attack against a token.
    """

    trap_count = int(
        n_qubits * trap_ratio
    )

    if trap_count == 0:
        return {
            "trap_count": 0,
            "detected": False,
            "errors": 0,
        }

    errors = 0

    for _ in range(trap_count):

        correct_guess = (
            random.random()
            < ATTACKER_BASIS_GUESS_PROBABILITY
        )

        if not correct_guess:
            errors += 1

    return {
        "trap_count": trap_count,
        "detected": errors > 0,
        "errors": errors,
    }


def run_experiment() -> list[dict]:
    """
    Run the Monte Carlo experiment for every trap ratio.
    """

    results = []

    for trap_ratio in TRAP_RATIOS:

        trap_count = int(
            N_QUBITS * trap_ratio
        )

        detections = 0
        attacks = 0
        false_negatives = 0
        total_errors = 0

        for _ in range(TRIALS):

            result = simulate_attack(
                trap_ratio=trap_ratio,
            )

            attacks += 1

            total_errors += result["errors"]

            if result["detected"]:
                detections += 1
            else:
                false_negatives += 1

        experimental_detection_rate = (
            detections / attacks
        )

        attack_success_rate = (
            false_negatives / attacks
        )

        average_disturbance = (
            total_errors
            / (
                attacks
                * max(1, trap_count)
            )
        )

        theoretical_detection_rate = (
            theoretical_detection_probability(
                trap_count
            )
        )

        results.append(
            {
                "trap_ratio": trap_ratio,
                "trap_count": trap_count,
                "theoretical_detection_rate":
                    theoretical_detection_rate,
                "experimental_detection_rate":
                    experimental_detection_rate,
                "attack_success_rate":
                    attack_success_rate,
                "false_negative_rate":
                    attack_success_rate,
                "average_disturbance":
                    average_disturbance,
            }
        )

    return results


# ---------------------------------------------------------------------
# Qiskit validation
# ---------------------------------------------------------------------

def qiskit_validation() -> None:
    """
    Run a small Qiskit/Aer basis-change validation.

    This is separate from the statistical experiment.
    """

    circuit = QuantumCircuit(1, 1)

    # Prepare |1>
    circuit.x(0)

    # Transform to the X basis.
    circuit.h(0)

    # Measure.
    circuit.measure(0, 0)

    simulator = AerSimulator()

    compiled = transpile(
        circuit,
        simulator,
    )

    result = simulator.run(
        compiled,
        shots=100,
    ).result()

    counts = result.get_counts()

    print()
    print("QISKIT VALIDATION")
    print("-----------------")
    print(
        f"Measurement counts: {counts}"
    )


# ---------------------------------------------------------------------
# Console output
# ---------------------------------------------------------------------

def print_results(
    results: list[dict],
) -> None:
    """Print experiment results."""

    print()

    print(
        f"{'Ratio':<10}"
        f"{'Traps':<10}"
        f"{'Theory':<12}"
        f"{'Experiment':<15}"
        f"{'Attack Success':<17}"
        f"{'Disturbance':<15}"
    )

    print("-" * 79)

    for result in results:

        print(
            f"{result['trap_ratio']:<10.1f}"
            f"{result['trap_count']:<10}"
            f"{result['theoretical_detection_rate']:<12.3f}"
            f"{result['experimental_detection_rate']:<15.3f}"
            f"{result['attack_success_rate']:<17.3f}"
            f"{result['average_disturbance']:<15.3f}"
        )


# ---------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------

def create_plots(
    results: list[dict],
) -> None:
    """Generate experiment plots."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    ratios = [
        result["trap_ratio"]
        for result in results
    ]

    theoretical_detection = [
        result["theoretical_detection_rate"]
        for result in results
    ]

    experimental_detection = [
        result["experimental_detection_rate"]
        for result in results
    ]

    attack_success = [
        result["attack_success_rate"]
        for result in results
    ]

    disturbance = [
        result["average_disturbance"]
        for result in results
    ]

    # -------------------------------------------------------------
    # Detection: theoretical vs experimental
    # -------------------------------------------------------------

    plt.figure()

    plt.plot(
        ratios,
        theoretical_detection,
        marker="o",
        label="Theoretical",
    )

    plt.plot(
        ratios,
        experimental_detection,
        marker="x",
        label="Experimental",
    )

    plt.xlabel("Trap Ratio")
    plt.ylabel("Attack Detection Probability")

    plt.title(
        "Theoretical vs Experimental Attack Detection"
    )

    plt.legend()
    plt.grid(True)

    plt.savefig(
        OUTPUT_DIR
        / "detection_theoretical_vs_experimental.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    # -------------------------------------------------------------
    # Attack success
    # -------------------------------------------------------------

    plt.figure()

    plt.plot(
        ratios,
        attack_success,
        marker="o",
    )

    plt.xlabel("Trap Ratio")
    plt.ylabel("Attack Success Probability")

    plt.title(
        "Trap Ratio vs Attack Success Probability"
    )

    plt.grid(True)

    plt.savefig(
        OUTPUT_DIR / "attack_success_rate.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    # -------------------------------------------------------------
    # Disturbance
    # -------------------------------------------------------------

    plt.figure()

    plt.plot(
        ratios,
        disturbance,
        marker="o",
    )

    plt.xlabel("Trap Ratio")
    plt.ylabel("Average Trap Disturbance")

    plt.title(
        "Trap Ratio vs Average Disturbance"
    )

    plt.grid(True)

    plt.savefig(
        OUTPUT_DIR / "average_disturbance.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:

    print()
    print(
        "QUANTUM TOKEN TRAP-RATIO EXPERIMENT"
    )
    print("=" * 40)

    print(
        f"Qubits per token : {N_QUBITS}"
    )

    print(
        f"Trials per ratio : {TRIALS}"
    )

    print(
        "Attacker basis guess probability : "
        f"{ATTACKER_BASIS_GUESS_PROBABILITY:.0%}"
    )

    results = run_experiment()

    print_results(results)

    create_plots(results)

    print()
    print(
        f"Plots saved to: {OUTPUT_DIR}"
    )

    qiskit_validation()

    print()
    print(
        "Experiment completed successfully."
    )


if __name__ == "__main__":
    main()