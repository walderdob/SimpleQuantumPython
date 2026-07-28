import sys
sys.path.insert(0, '../')
from sqp import *
import torch

def entanglement():
    n = 2
    ψ = kronPower(z_state, n)
    # Entangling qubits q1 and q0
    ψ = qubitWiseMultiply(ψ, n, h_gate, 0)
    ψ = qubitWiseMultiply(ψ, n, x_gate, 1, [[0, True]])
    
    return ψ    

def main():
    infoPrint(entanglement())
    
    
if __name__ == '__main__':
    main()
