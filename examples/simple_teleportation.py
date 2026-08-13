from sqp_quantum import *
import torch

def simple_teleportation():
    n = 3
    α = 1/torch.sqrt(torch.tensor(2.0))
    β = 1j/torch.sqrt(torch.tensor(2.0))
    # ψ is representing the qubit Q
    ψ = α*z_state + β*o_state
    ϕ = kronPower(z_state, 2)
    
    # Entangling qubits A and B
    ϕ = applyH(ϕ, 0)
    ϕ = applyCNOT(ϕ, 0, 1)
    
    # Transforming ψ in the full circuit
    ψ = torch.kron(ψ, ϕ)
    ψ = applyCNOT(ψ, 0, 1)
    ψ = applyH(ψ, 0)
    q, ψ = measureQubit(ψ, 0)
    a, ψ = measureQubit(ψ, 1)
    
    # Applying X and Z gates depending on the bits a, and q
    if (a == 1): ψ = applyX(ψ, 2)
    if (q == 1): ψ = applyZ(ψ, 2)
    
    b1 = q + (a << 1)
    b2 = b1 + (1 << (n-1))
    
    # Qubit that Bob has (should be the same as qubit Q in the beginning)
    print(f"B = {ψ[b1].item():.4f}|0> + {ψ[b2].item():.4f}|1>")
    
    return ψ
    

def main():
    printState(simple_teleportation())
    
    
if __name__ == '__main__':
    main()