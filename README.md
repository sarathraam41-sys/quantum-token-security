# Quantum Token Security

A research-oriented educational prototype exploring **quantum-inspired digital token security**, BB84-style trap qubits, attack detection, and quantum-circuit verification using **Qiskit Aer**.

The project combines a quantum-token security model with a Flask-based banking demonstration and a statistical experiment that studies how the proportion of trap qubits affects attack detection.

> **Educational prototype:** This project is intended for learning, experimentation, and research demonstration. It is not a production banking system, a physical quantum-money implementation, or a claim of practical quantum-secure financial infrastructure.

---

## Overview

Digital financial systems rely heavily on cryptographic mechanisms to protect transactions and prevent unauthorized manipulation.

This project explores a different security model inspired by quantum information principles:

* A digital token contains multiple qubit-like states.
* Some positions are designated as **trap qubits**.
* The token uses two measurement bases, `Z` and `X`, following a BB84-style representation.
* An attacker attempting to inspect or modify the token may disturb trap states.
* Verification checks the trap positions for inconsistencies.
* Increasing the number of trap qubits increases the probability of detecting an attack.

The repository contains both:

1. A **Qiskit/Aer circuit simulation** for token verification.
2. A **statistical Monte Carlo experiment** for studying attack-detection probabilities.

---

## Key Features

### Quantum Token Generation

Tokens contain:

* configurable number of qubits
* randomly selected trap positions
* randomly selected `Z` / `X` bases
* randomly selected binary values

Example:

```text
20 qubits
6 trap qubits
30% trap ratio
```

---

### Qiskit-Based Verification

The verification layer uses:

* Qiskit
* Qiskit Aer
* quantum circuits
* basis transformations
* simulated measurements

The verifier:

1. prepares the token states,
2. optionally introduces an attacker disturbance,
3. applies the appropriate inverse basis transformation,
4. measures the qubits,
5. checks the trap positions,
6. calculates the observed trap error rate.

---

### Attack Simulation

The project includes an educational attack model.

An attacker can disturb token qubits with a configurable probability.

The resulting disturbance can produce errors in trap positions.

This allows the project to demonstrate the relationship between:

```text
Attack
  ↓
Quantum-state disturbance
  ↓
Trap errors
  ↓
Attack detection
```

---

## Security Model

The project uses a simplified BB84-style model.

Each token position has:

```text
Basis:
    Z or X

Value:
    0 or 1
```

Some positions are selected as traps.

During verification, X-basis states are rotated back into the computational basis before measurement.

Conceptually:

```text
Token preparation
       │
       ▼
  ┌───────────┐
  │ Z / X     │
  │ basis     │
  └───────────┘
       │
       ▼
Possible attacker
       │
       ▼
Basis-aware verification
       │
       ▼
Trap measurement
       │
       ▼
 ┌─────┴─────┐
 │           │
No errors   Errors
 │           │
 ▼           ▼
Valid      Attack detected
```

---

## Why Trap Qubits?

Suppose an attacker has a `50%` probability of correctly guessing the basis of each trap.

For `T` independent traps:

$$
P(\text{no detection}) = (0.5)^T
$$

Therefore:

$$
P(\text{detection}) = 1-(0.5)^T
$$

For example:

| Trap count | Theoretical detection |
| ---------: | --------------------: |
|          2 |                 75.0% |
|          4 |                93.75% |
|          6 |                98.44% |
|          8 |                99.61% |
|         10 |                99.90% |

The experiment in this repository compares these theoretical probabilities with Monte Carlo simulation results.

---

# Experimental Results

The trap-ratio experiment uses:

```text
Qubits per token: 20
Trials per ratio: 1000
Attacker basis guess probability: 50%
```

A representative run produced:

| Trap ratio | Traps | Theory | Experiment | Attack success |
| ---------: | ----: | -----: | ---------: | -------------: |
|        10% |     2 |  75.0% |      75.1% |          24.9% |
|        20% |     4 |  93.8% |      93.7% |           6.3% |
|        30% |     6 |  98.4% |      98.7% |           1.3% |
|        40% |     8 |  99.6% |      99.6% |           0.4% |
|        50% |    10 |  99.9% |      99.9% |           0.1% |

Because the experiment uses randomized Monte Carlo trials, individual runs can produce slightly different values.

The important observation is that the experimental detection probability closely follows the theoretical model.

---

## Experiment Output

Running the experiment generates:

```text
outputs/
├── detection_theoretical_vs_experimental.png
├── attack_success_rate.png
└── average_disturbance.png
```

The main comparison is:

```text
Theoretical model
       │
       │
       ├───────────────┐
       │               │
       ▼               ▼
Expected probability   Monte Carlo result
       │               │
       └───────┬───────┘
               ▼
       Experimental agreement
```

---

# Qiskit Validation

The project also performs a small independent Qiskit/Aer validation.

The validation prepares a state, performs a Hadamard basis transformation, and measures it repeatedly.

A representative result:

```text
Measurement counts:
{'0': 49, '1': 51}
```

The approximately balanced distribution demonstrates the expected probabilistic behavior of the simulated basis transformation.

This validation is intentionally kept separate from the larger statistical experiment.

---

# Application Demo

The repository also contains a Flask-based demonstration application called **QuantumBank**.

The application provides:

* wallet creation
* simulated balances
* token generation
* token verification
* transaction transfers
* transaction history
* token collapse demonstration
* token reissuance
* administrator demonstration interface
* real-time UI events through Flask-SocketIO

The application uses SQLite for persistence.

---

## Application Architecture

```text
                         Flask Application
                                │
                    ┌───────────┴───────────┐
                    │                       │
                Web UI                 REST endpoints
                    │                       │
                    └───────────┬───────────┘
                                │
                       Application Services
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
          Wallet Service   Transaction Service  Quantum
                                                    │
                                                    ▼
                                               Qiskit/Aer
                                │
                                ▼
                             SQLite
```

---

# Project Structure

```text
quantum-token-security/
│
├── app.py
├── requirements.txt
├── LICENSE
├── .gitignore
├── README.md
│
├── src/
│   ├── __init__.py
│   │
│   ├── quantum/
│   │   ├── __init__.py
│   │   ├── token.py
│   │   ├── verification.py
│   │   └── demo.py
│   │
│   ├── banking/
│   │   ├── __init__.py
│   │   ├── wallet.py
│   │   └── transactions.py
│   │
│   └── database/
│       ├── __init__.py
│       └── database.py
│
├── experiments/
│   └── trap_ratio_experiment.py
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   └── admin.html
│
├── static/
│   └── style.css
│
├── outputs/
│   └── generated experiment plots
│
└── docs/
    └── methodology.md
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/quantum-token-security.git
cd quantum-token-security
```

Create a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Quantum Demonstration

Run:

```bash
python -m src.quantum.demo
```

The program performs:

1. token generation
2. honest verification
3. simulated attack
4. trap-error analysis

Example:

```text
QUANTUM TOKEN SECURITY DEMO
--------------------------------

Token size: 20 qubits
Trap count: 6

Honest verification:
{'valid': True, ...}

Attack simulation:
{'valid': False, ...}
```

---

# Running the Security Experiment

Run:

```bash
python experiments\trap_ratio_experiment.py
```

The experiment:

* evaluates multiple trap ratios
* runs 1,000 trials per configuration
* calculates theoretical detection probability
* calculates experimental detection probability
* measures attack success
* measures average disturbance
* generates plots
* performs a Qiskit/Aer validation

---

# Running the Flask Application

Start the server:

```bash
python app.py
```

Then open:

```text
http://localhost:5000
```

The administrator demonstration is available at:

```text
http://localhost:5000/admin
```

---

# Demonstration Workflow

### 1. Create a wallet

Enter a UPI-style identifier such as:

```text
sarath@upi
```

The application generates a token automatically.

---

### 2. View the wallet

The dashboard displays:

* balance
* token information
* trap ratio
* verification controls
* transaction history

---

### 3. Perform a transaction

Enter:

```text
Receiver: alice@upi
Amount: 10000
```

The application records the transaction in SQLite.

---

### 4. Verify the token

Use:

```text
Honest Verification
```

to verify an undisturbed token.

Then use:

```text
Simulate Attack
```

to demonstrate token disturbance.

---

### 5. Demonstrate token collapse

The administrator interface can force the application-level token state into a collapsed state.

The user can then issue a replacement token.

> In this project, **"collapse" is an application-level demonstration state**. It should not be interpreted as a physical quantum measurement collapse occurring on real quantum hardware.

---

# Technology Stack

| Component               | Technology              |
| ----------------------- | ----------------------- |
| Language                | Python                  |
| Quantum framework       | Qiskit                  |
| Quantum simulator       | Qiskit Aer              |
| Web framework           | Flask                   |
| Real-time communication | Flask-SocketIO          |
| Database                | SQLite                  |
| Numerical analysis      | NumPy                   |
| Visualization           | Matplotlib              |
| Frontend                | HTML / CSS / JavaScript |

---

# Design Principles

The second-generation implementation separates the project into distinct layers.

### Quantum layer

Responsible for:

* token generation
* basis representation
* quantum-circuit verification
* attack simulation

### Banking layer

Responsible for:

* wallet management
* balances
* transactions
* token lifecycle

### Database layer

Responsible for:

* SQLite persistence
* wallet storage
* transaction history

### Experiment layer

Responsible for:

* Monte Carlo simulation
* theoretical calculations
* statistical analysis
* visualization

This separation makes the project easier to extend and test.

---

# Limitations

This project has several important limitations.

### 1. It is not physical quantum money

The token is represented digitally inside a classical software system.

The project does not create or distribute physical quantum states.

---

### 2. Qiskit Aer is a simulator

The quantum circuits run using a simulator rather than physical quantum hardware.

---

### 3. Simplified attacker model

The attacker model assumes a simplified basis-guessing strategy.

Real quantum attack models can be significantly more complex.

---

### 4. Educational banking application

The Flask application is a demonstration system.

It does not implement:

* real authentication
* production authorization
* secure financial APIs
* real UPI integration
* production-grade cryptographic key management
* regulatory compliance
* distributed transaction infrastructure

---

### 5. Application-level token state

The dashboard's token "collapse" mechanism is a software state used to demonstrate a security response.

It is not equivalent to observing an actual physical quantum state.

---

# Future Work

Possible extensions include:

* physical quantum hardware execution
* more rigorous BB84 protocol modeling
* configurable attacker strategies
* intercept-resend attack simulation
* noise-channel experiments
* quantum error-rate analysis
* larger statistical experiments
* confidence intervals
* additional quantum authentication mechanisms
* cryptographic token binding
* stronger application authentication
* production-style database architecture
* API authentication and authorization
* integration with quantum-safe classical cryptography
* benchmarking against classical security mechanisms

---

# Research Questions

The project can be extended to investigate questions such as:

1. How does trap density affect attack-detection probability?
2. How does increasing token size affect detection reliability?
3. How does attacker basis-selection strategy affect detection?
4. How does simulated quantum noise affect verification?
5. What trade-offs exist between trap density and usable token capacity?
6. How do different attack models affect observed trap error rates?

---

# Disclaimer

This repository is an **educational and research prototype**.

It should not be used to process real financial transactions, store real financial credentials, or make claims about production quantum-secure banking.

The term "quantum token" refers to the security model implemented in this project and does not imply that the software represents physically realizable quantum money.

---

# License

This project is licensed under the MIT License.

See [`LICENSE`](LICENSE) for details.

---

# Author

**Sarath B Raam**

Artificial Intelligence & Machine Learning
SRM Institute of Science and Technology, Ramapuram

---

## Project Focus

```text
Quantum Information
        +
Security
        +
Statistical Modeling
        +
Qiskit Simulation
        +
Software Engineering
```

The project demonstrates how concepts from quantum information can be explored through a combination of quantum-circuit simulation, probabilistic modeling, and a classical application layer.
