# Simple Quantum in Python
Library that facilitates the creation and simulation of simple quantum circuits.

## Variables and gates:
`z_state:` $\lvert 0 \rangle$\
`o_state:` $\lvert 1 \rangle$\
`h_gate:` Hadamard gate\
`x_gate:` Pauli-X gate\
`y_gate:` Pauli-Y gate\
`z_gate:` Pauli-Z gate

## Methods:
`innerProduct(ket0, ket1):` Generates the outer product of the quantum states. Inputs are $\lvert \psi_0 \rangle$ and  $\lvert \psi_1 \rangle$ and return  $\langle \psi_0 \lvert \psi_1 \rangle$.\
`outerProduct(ket0, ket1):` Generates the outer product of the quantum states. Inputs are $\lvert \psi_0 \rangle$ and  $\lvert \psi_1 \rangle$ and return $\lvert \psi_0 \rangle \langle \psi_1 \lvert$.\
`kronPower(ket, times):` Computes the tensor power of a quantum state. Inputs are $\lvert \psi \rangle$ and a positive integer and return $\lvert \psi \rangle^{\otimes times}$.\
`qubitWiseMultiply(ψ, n, U, i_w, listOfControlBits):` Apply a single-qubit gate to qubit i_w. Inputs are $\psi$, quantum state, $n$, number of qubits in simulation, $U$, gate being applied, i_w, index of line where gate is being applied and listOfControlBits, array with array in the format [qubit, True or False] apply a control bit to a line.\
`applySwap(ψ, n, i_w, j_w, listOfControlBits):` Swap the values of qubit *i_w* and *j_w*. Inputs are $\psi$, quantum state, n, number of bits, i_w, qubit 1, j_w, qubit 2, and also a list of the control bits.\
`probabilities(ψ):` Return the probability of each qubit in state $\psi$. Input is $\psi$, quantum state.\
`measureState(ψ):` Collapse the quantum state $\psi$ and return its final value. Input is $\psi$, quantum state.\
`measureQubit(ψ, n, i_w):` Measure a specific qubit from the $\psi$, return the value of the qubit and the new quantum state. Inputs are $psi$, quantum state, $n$, number of qubits, i_w, index of qubit being measured.\
`infoPrint(ψ):` Print the quantum state, the probabilities of each qubit, and the final measured state. Input is $\psi$, quantum state. (It will collapse all the qubits in the circuit due to the measureState method).

# Examples
## Entanglement
**`examples/entanglement.py`**

## Random number generator
**`examples/random_number.py`**

## Simple quantum teleportation:
Diagram I used to design the quantum teleportation method example [2]:
![Teleportation circuit](https://quantum.cloud.ibm.com/learning/images/courses/basics-of-quantum-information/entanglement-in-action/teleportation-time-steps.svg?dpl=0-1-1564-8eac441376a9)
**`examples/simple_teleportation.py`**

# Future additions
- More gates, and changing gates
- $\text{QFT}$ and $\text{QFT}^{\dagger}$
- Then, more example circuits!

# References
[1] https://arxiv.org/pdf/2506.08142 \
[2] https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/quantum-teleportation
