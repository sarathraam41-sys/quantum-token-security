# Quantum Token Security — Methodology

## 1. Purpose

This document describes the technical methodology used by the Quantum Token Security project.

The project explores a BB84-style quantum-token security model through:

1. Digital token generation
2. Qiskit/Aer circuit simulation
3. Trap-qubit verification
4. Simulated attacker disturbance
5. Monte Carlo security experiments
6. Theoretical probability analysis
7. A classical Flask application demonstrating token lifecycle and banking operations

The implementation is intended for educational and research experimentation.

---

# 2. Quantum Token Model

A token is represented as a collection of `n` qubit positions.

Each position contains:

* a basis
* a binary value

The available bases are:

```text
Z
X
```

The binary values are:

```text
0
1
```

A simplified token can therefore be represented as:

```text
Position     Basis     Value
--------------------------------
0            Z         1
1            X         0
2            Z         0
3            X         1
...
```

A subset of positions is randomly selected as **trap qubits**.

For example, with:

```text
20 total qubits
30% trap ratio
```

the token contains:

```text
6 trap positions
```

These positions are used during verification.

---

# 3. Token Generation

The token-generation process is implemented in:

```text
src/quantum/token.py
```

The generator:

1. validates the requested number of qubits,
2. validates the trap ratio,
3. calculates the number of trap positions,
4. randomly selects trap positions,
5. randomly assigns `Z` or `X` bases,
6. randomly assigns binary values.

The token is represented as a Python dictionary.

Conceptually:

```text
create_quantum_token()
        │
        ├── Number of qubits
        │
        ├── Trap positions
        │
        ├── Basis assignments
        │
        └── Binary values
```

---

# 4. Basis Representation

The implementation uses two basis types.

## Z Basis

The Z basis corresponds to the computational basis:

$$
|0\rangle
$$

and

$$
|1\rangle
$$

These can be represented directly using computational-basis states.

---

## X Basis

The X basis is represented using the Hadamard transformation.

The Hadamard gate is:

$$
H =
\frac{1}{\sqrt{2}}
\begin{bmatrix}
1 & 1 \\
1 & -1
\end{bmatrix}
$$

Applying the Hadamard gate transforms computational-basis states into the X basis:

$$
H|0\rangle = |+\rangle
$$

$$
H|1\rangle = |-\rangle
$$

The implementation uses this transformation when preparing X-basis token states.

---

# 5. Verification Process

Token verification is implemented in:

```text
src/quantum/verification.py
```

The verification circuit follows these stages:

```text
Token
  │
  ▼
Prepare encoded states
  │
  ▼
Optional attacker disturbance
  │
  ▼
Apply inverse basis transformation
  │
  ▼
Measure
  │
  ▼
Check trap positions
  │
  ▼
Calculate error rate
```

---

# 6. X-Basis Verification

A critical part of the implementation is the correct handling of X-basis states.

During preparation:

```text
X-basis state
     │
     ▼
     H
     │
     ▼
Quantum state
```

Before computational-basis measurement, the inverse transformation is applied:

```text
Quantum state
     │
     ▼
     H
     │
     ▼
Computational basis
```

Because the Hadamard gate is self-inverse:

$$
H^{-1} = H
$$

the same gate can be used to rotate an X-basis state back before measurement.

This allows the measured classical value to be compared with the value originally encoded in the token.

---

# 7. Attacker Model

The project contains an educational attack simulation.

When attack simulation is enabled, each qubit has a probability of being disturbed.

The current implementation uses:

```text
30% disturbance probability per qubit
```

The disturbance is modeled using a Hadamard operation.

The purpose is not to represent every possible quantum attack, but to demonstrate the principle that unauthorized interaction with quantum states can introduce detectable inconsistencies.

The attack model is therefore intentionally simplified.

---

# 8. Trap Verification

Only the designated trap positions are used for security verification.

For every trap:

```text
Measured value
      │
      ▼
Compare with expected value
      │
      ├── Match ──────► No detected error
      │
      └── Mismatch ───► Trap error
```

The total trap error rate is:

$$
\text{Error Rate}
=
\frac{\text{Number of Trap Errors}}
{\text{Number of Traps}}
$$

A token is considered valid when:

$$
\text{Trap Errors} = 0
$$

Otherwise, the verification reports the token as invalid.

---

# 9. Trap-Ratio Experiment

The experimental component is implemented in:

```text
experiments/trap_ratio_experiment.py
```

The experiment investigates the relationship between:

```text
Trap ratio
      ↓
Number of traps
      ↓
Probability of detecting an attack
```

The experiment uses:

```text
20 qubits per token
1000 trials per configuration
50% attacker basis-guess probability
```

The tested trap ratios are:

```text
10%
20%
30%
40%
50%
```

---

# 10. Theoretical Detection Model

The experiment assumes that an attacker has a 50% probability of correctly guessing the basis of each trap.

For `T` independent traps:

$$
P(\text{correctly guess all traps})
=
(0.5)^T
$$

Therefore:

$$
P(\text{no detection})
=
(0.5)^T
$$

and:

$$
P(\text{detection})
=
1-(0.5)^T
$$

---

## Example

For two traps:

$$
P(\text{detection})
=
1-(0.5)^2
$$

$$
=1-0.25
$$

$$
=0.75
$$

Therefore:

```text
2 traps → 75% theoretical detection probability
```

For six traps:

$$
P(\text{detection})
=
1-(0.5)^6
$$

$$
=0.984375
$$

Therefore:

```text
6 traps → 98.4375% theoretical detection probability
```

---

# 11. Theoretical Results

For a 20-qubit token:

| Trap Ratio | Trap Count | Theoretical Detection |
| ---------: | ---------: | --------------------: |
|        10% |          2 |                75.00% |
|        20% |          4 |                93.75% |
|        30% |          6 |                98.44% |
|        40% |          8 |                99.61% |
|        50% |         10 |                99.90% |

These values are generated directly from the theoretical probability model.

---

# 12. Monte Carlo Experiment

The theoretical model is compared against randomized experimental trials.

For each trap ratio:

```text
1000 attacks
      │
      ├── Attack detected
      │
      └── Attack not detected
```

The experimental detection probability is calculated as:

$$
P_{\text{experimental}}
=
\frac{\text{Detected Attacks}}
{\text{Total Attacks}}
$$

Because the experiment uses random sampling, the experimental result will not necessarily equal the theoretical value exactly.

However, increasing the number of trials should generally produce closer agreement.

---

# 13. Experimental Results

A representative execution produced:

| Trap Ratio | Traps | Theory | Experiment | Attack Success |
| ---------: | ----: | -----: | ---------: | -------------: |
|        10% |     2 |  75.0% |      75.1% |          24.9% |
|        20% |     4 |  93.8% |      93.7% |           6.3% |
|        30% |     6 |  98.4% |      98.7% |           1.3% |
|        40% |     8 |  99.6% |      99.6% |           0.4% |
|        50% |    10 |  99.9% |      99.9% |           0.1% |

The results demonstrate close agreement between the theoretical model and the Monte Carlo simulation for the tested configurations.

---

# 14. Attack Success

Attack success in the experiment is defined as a trial in which no trap error is detected.

Therefore:

$$
P(\text{attack success})
=
1-P(\text{detection})
$$

Under the current theoretical model:

$$
P(\text{attack success})
=
(0.5)^T
$$

This produces the inverse relationship observed in the experiment:

```text
More traps
    ↓
Higher detection probability
    ↓
Lower probability of undetected attack
```

---

# 15. Disturbance Measurement

The experiment also records average trap disturbance.

The disturbance metric is calculated from the number of trap errors observed across trials.

Conceptually:

$$
\text{Average Disturbance}
=
\frac{\text{Total Trap Errors}}
{\text{Total Trap Measurements}}
$$

For the current attacker model, the expected disturbance is approximately 50% because the attacker has a 50% probability of guessing the correct basis.

This metric describes the simulated attack model and should not be interpreted as a universal physical quantum-noise measurement.

---

# 16. Qiskit/Aer Validation

The experiment includes a separate Qiskit/Aer validation.

The purpose of this component is to demonstrate that the underlying circuit operations execute through an actual quantum-circuit simulator.

The validation:

1. creates a quantum circuit,
2. prepares a state,
3. applies a Hadamard transformation,
4. measures the qubit,
5. executes the circuit using AerSimulator,
6. collects measurement counts.

A representative result was:

```text
Measurement counts:
{'0': 49, '1': 51}
```

The approximate 50/50 distribution is consistent with the expected probabilistic outcome of the demonstrated basis transformation.

---

# 17. Statistical Simulation vs Quantum Simulation

The project deliberately separates two different types of computation.

## Qiskit/Aer simulation

Used for:

* quantum-circuit construction
* basis transformations
* measurement
* circuit-level validation

## Monte Carlo simulation

Used for:

* large numbers of trials
* attack-detection statistics
* trap-ratio analysis
* theoretical-vs-experimental comparison

The Monte Carlo experiment should therefore not be described as running 1,000 full quantum circuits.

Instead:

```text
Qiskit/Aer
    → circuit-level validation

Monte Carlo
    → statistical security experiment
```

This distinction is important when interpreting the results.

---

# 18. Banking Demonstration

The Flask application provides a classical software layer around the quantum-token model.

The banking layer contains:

```text
WalletService
TransactionService
Database
```

Wallets contain:

* UPI-style identifier
* simulated balance
* serialized token
* application-level collapse state

Transactions contain:

* sender
* receiver
* amount
* timestamp

SQLite provides persistence.

---

# 19. Token Lifecycle

The application demonstrates the following token lifecycle:

```text
Wallet creation
      │
      ▼
Token generation
      │
      ▼
Token verification
      │
      ├───────────────┐
      │               │
      ▼               ▼
Valid token       Attack/collapse
                      │
                      ▼
                 Token invalidated
                      │
                      ▼
                 Token reissued
```

The collapse state is an application-level security demonstration.

It does not represent physical quantum wavefunction collapse.

---

# 20. Security Interpretation

The experiment demonstrates an important conceptual property of trap-based quantum-inspired authentication:

> Increasing the number of independently checked trap positions reduces the probability that a basis-guessing attacker can modify a token without being detected.

However, the result depends on the assumptions of the attacker model.

The experiment does not establish security against arbitrary adversaries or demonstrate security of a production financial system.

---

# 21. Reproducibility

The experiment can be reproduced using:

```bash
python experiments/trap_ratio_experiment.py
```

Each execution uses randomized trials, so small differences between runs are expected.

For more stable statistical estimates, the number of trials can be increased.

For example:

```python
TRIALS = 10000
```

would provide a larger sample than:

```python
TRIALS = 1000
```

at the cost of additional execution time.

---

# 22. Limitations

The current methodology has several limitations.

### Simplified quantum model

The token is a classical data structure representing quantum-state information.

### Simulated quantum hardware

Qiskit Aer provides simulation rather than execution on physical quantum hardware.

### Simplified attack

The attacker model uses a simple randomized disturbance mechanism.

### Simplified banking layer

The Flask application is not designed for real financial use.

### No production authentication

The demonstration does not provide production-grade authentication, authorization, key management, or regulatory controls.

### No physical quantum memory

The implementation does not store quantum states in physical quantum memory.

---

# 23. Potential Extensions

Future experiments could investigate:

* intercept-resend attacks
* different attacker basis strategies
* varying attacker disturbance probabilities
* different token sizes
* different trap distributions
* simulated quantum noise
* depolarizing channels
* bit-flip errors
* phase-flip errors
* measurement noise
* confidence intervals
* larger Monte Carlo samples
* physical quantum hardware execution
* comparison with classical authentication mechanisms

---

# 24. Summary

The methodology combines three levels of analysis:

```text
                    Quantum Token Security
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
     Token Model        Qiskit/Aer         Statistical Model
          │                   │                   │
          │                   │                   │
          ▼                   ▼                   ▼
     BB84-style          Circuit-level       Monte Carlo
     representation      validation          experiment
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ▼
                    Security Analysis
```

The resulting project provides a software-based environment for studying how trap-based quantum-inspired tokens can be modeled, simulated, and experimentally evaluated.
