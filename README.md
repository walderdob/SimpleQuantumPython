# Simple Quantum in Python
Library that creates simple quantum circuits simulations\

**Variables and gates:**\
`z_state:` $\lvert 0 \rangle$\
`o_state:` $\lvert 1 \rangle$\
`h_gate:` Hadamard gate\
`x_gate:` Pauli-X gate\
`y_gate:` Pauli-Y gate\
`z_gate:` Pauli-Z gate\

**Functions:**\
`innerProduct(ket0, ket1):` Generates the outer product of the quantum states. Inputs are $\lvert \psi_0 \rangle$ and  $\lvert \psi_1 \rangle$ and return  $\langle \psi_0 \lvert \psi_1 \rangle$.\
`outerProduct(ket0, ket1):` Generates the outer product of the quantum states. Inputs are $\lvert \psi_0 \rangle$ and  $\lvert \psi_1 \rangle$ and return $\lvert \psi_0 \rangle \langle \psi_1 \lvert$.\
`kronPower(ket, times):` Computes the tensor power of a quantum state. Inputs are $\lvert \psi \rangle$ and a positive integer and return $\lvert \psi \rangle^{\otimes times}$.\
`qubitWiseMultiply(ψ, n, U, i_w, listOfControlBits):` Apply a single-qubit gate to qubit i_w. Inputs are $\psi$, quantum state, $n$, number of qubits in simulation, $U$, gate being applied, i_w, index of line where gate is being applied and listOfControlBits, array with array in the format [qubit, True or False] apply a control bit to a line.\
`applySwap(ψ, n, i_w, j_w, listOfControlBits):` Swap the values of qubit *i_w* and *j_w*. Inputs are $\psi$, quantum state, n, number of bits, i_w, qubit 1, j_w, qubit 2, and also a control bits.\
`testCircuitx():` Example circuits (1, 2, and 3).
