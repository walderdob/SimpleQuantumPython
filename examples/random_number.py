from sqp_quantum import *
import torch

def random_number_gen(n):
    # ψ = |0>^n
    ψ = kronPower(z_state, n)
    # Apply Hadamard to all qubits in the state
    for i in range(n): ψ = applyH(ψ, i)
    
    # Return the measurement of all qubits
    return measureState(ψ)

def main():
    print(random_number_gen(3))
    
    
if __name__ == '__main__':
    main()