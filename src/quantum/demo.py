from src.quantum.token import create_quantum_token
from src.quantum.verification import verify_token


def main():
    token = create_quantum_token()

    honest_result = verify_token(
        token,
        malicious=False,
    )

    attack_result = verify_token(
        token,
        malicious=True,
    )

    print("\nQUANTUM TOKEN SECURITY DEMO")
    print("-" * 32)

    print(
        f"Token size: {token['n']} qubits"
    )

    print(
        f"Trap count: {len(token['traps'])}"
    )

    print("\nHonest verification:")
    print(honest_result)

    print("\nAttack simulation:")
    print(attack_result)


if __name__ == "__main__":
    main()