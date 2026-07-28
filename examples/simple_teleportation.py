import sys
sys.path.insert(0, '../')
from sqp import *
import torch

def simple_teleportation():
    n = 3
    α = 3/5
    β = 4/5
    # ψ is representing the qubit Q
    ψ = α*z_state + β*o_state
    ϕ = kronPower(z_state, 2)
    
    # Entangling qubits A and B
    ϕ = qubitWiseMultiply(ϕ, 2, h_gate, 0)
    ϕ = qubitWiseMultiply(ϕ, 2, x_gate, 1, [[0, True]])
    
    # Transforming ψ in the full circuit
    ψ = torch.kron(ψ, ϕ)
    ψ = qubitWiseMultiply(ψ, n, x_gate, 1, [[0, True]])
    ψ = qubitWiseMultiply(ψ, n, h_gate, 0)
    q, ψ = measureQubit(ψ, n, 0)
    a, ψ = measureQubit(ψ, n, 1)
    
    # Applying X and Z gates depending on the bits a, and q
    if (a == 1): ψ = qubitWiseMultiply(ψ, n, x_gate, 2)
    if (q == 1): ψ = qubitWiseMultiply(ψ, n, z_gate, 2)
    
    b1 = q + (a << 1)
    b2 = b1 + (1 << (n-1))
    
    # Qubit that Bob has (should be the same as qubit Q in the beginning)
    print(f"B = {torch.abs(ψ[b1]).item()}|0> + {torch.abs(ψ[b2]).item()}|1>")
    
    return ψ
    

def main():
    infoPrint(simple_teleportation())
    
    
if __name__ == '__main__':
    main()