import torch

# Basis state
z_state = torch.tensor([[1], [0]])
o_state = torch.tensor([[0], [1]])

# Basic gates
identity = torch.tensor([[1, 0],[0, 1]])
h_gate = 1/(torch.sqrt(torch.tensor(2))) * torch.tensor([[1, 1],[1, -1]])
x_gate = torch.tensor([[0, 1], [1, 0]])
y_gate = torch.tensor([[0, -1j], [1j, 0]], dtype=torch.complex64)
z_gate = torch.tensor([[1, 0], [0, -1]])
cxb_gate = torch.tensor([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
cxa_gate = torch.tensor([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]])

def innerProduct(ket0: torch.Tensor, ket1: torch.Tensor) -> torch.Tensor:
    return torch.mm(ket0.mH, ket1)

def outerProduct(ket0: torch.Tensor, ket1: torch.Tensor) -> torch.Tensor:
    return torch.mm(ket0, ket1.mH)

def kronPower(ket: torch.Tensor, times: int) -> torch.Tensor:
    result = ket
    while times > 1:
        result = torch.kron(result, ket)
        times -= 1
    
    return result

def qubitWiseMultiply(ψ: torch.Tensor, n: int, U: torch.Tensor, i_w: int, listOfControlBits = []) -> torch.Tensor:
    inclusionMask = 0
    desiredValueMask = 0
    
    for i in listOfControlBits:
        wireIndex, flag = i
        bit = 1 << wireIndex
        inclusionMask |= bit
        
        if (flag == True):
            desiredValueMask |= bit
            
    sizeOfStateVector = 1 << n
    sizeOfHalfBlock = 1 << i_w
    sizeOfBlock = sizeOfHalfBlock << 1
    b = ψ.clone()
    
    for i in range(0, sizeOfStateVector, sizeOfBlock):
        for offset in range(0, sizeOfHalfBlock, 1):
            i1 = i | offset
            if ((i1 & inclusionMask) != desiredValueMask):
                continue
            i2 = i1 | sizeOfHalfBlock
            b[i1] = U[0, 0] * ψ[i1] + U[0, 1] * ψ[i2]
            b[i2] = U[1, 0] * ψ[i1] + U[1, 1] * ψ[i2]
    return b
    
def swapBits(k: int, i: int, j: int) -> int:
    if(i == j): return k
    
    bi = (k >> i) & 1
    bj = (k >> j) & 1
    if (bi != bj):
        mask = (1 << i) | (1 << j)
        k ^= mask
    
    return k

def applySwap(ψ: torch.Tensor, n: int, i_w: int, j_w: int, listOfControlBits = []) -> torch.Tensor:
    inclusionMask = 0
    desiredValueMask = 0
    
    for i in listOfControlBits:
        wireIndex, flag = i
        bit = 1 << wireIndex
        inclusionMask |= bit
        
        if (flag == True):
            desiredValueMask |= bit

    sizeOfStateVector = 1 << n
    b = ψ.clone()
    
    if (i_w == j_w): return b
    maskj = 1 << j_w
    antimaski = ~(1 << i_w)
    
    for k in range(0, sizeOfStateVector, 1):
        if ((k & inclusionMask) != desiredValueMask):
                continue
        ithBitK = (k >> i_w) & 1
        if (ithBitK == 1):
            jthBitK = (k >> j_w) & 1
            if (jthBitK == 0):
                k2 = (k & antimaski) | maskj
                b[k2] = ψ[k]
                b[k]  = ψ[k2]
    
    return b

def test_circuit() -> torch.Tensor:
    n = 3
    ψ = kronPower(z_state, n).to(torch.cfloat)
    ψ = qubitWiseMultiply(ψ, n,h_gate,1)
    ψ = qubitWiseMultiply(ψ, n,x_gate,2)
    ψ = qubitWiseMultiply(ψ, n,x_gate,0,[[1,True]])
    ψ = qubitWiseMultiply(ψ, n,z_gate,0)
    ψ = qubitWiseMultiply(ψ, n,x_gate,2,[[1,True]])
    
    return ψ

def test_circuit2() -> torch.Tensor:
    n = 2
    ψ = kronPower(z_state, 2).to(torch.cfloat)
    ψ = qubitWiseMultiply(ψ, n, y_gate, 0)
    ψ = qubitWiseMultiply(ψ, n, h_gate, 0)
    ψ = qubitWiseMultiply(ψ, n, x_gate, 1, [[0, True]])
    ψ = qubitWiseMultiply(ψ, n, z_gate, 1)
    
    return ψ

def test_circuit3() -> torch.Tensor:
    ψ = kronPower(z_state, 3).to(torch.cfloat)
    ψ = qubitWiseMultiply(ψ, 3, h_gate, 0)
    ψ = applySwap(ψ, 3, 0, 2)
    ψ = qubitWiseMultiply(ψ, 3, x_gate, 1, [[2, False]])
    ψ = qubitWiseMultiply(ψ, 3, x_gate, 0, [[1, True]])
    ψ = qubitWiseMultiply(ψ, 3, y_gate, 0)
    ψ = applySwap(ψ, 3, 1, 2, [[0, True]])
    ψ = qubitWiseMultiply(ψ, 3, z_gate, 1)
    
    return ψ

def main() -> None:
    print(test_circuit3())

if __name__ == '__main__':
    main()