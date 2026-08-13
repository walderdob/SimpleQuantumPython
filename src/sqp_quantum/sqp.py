import torch
import math

# Basis state
z_state = torch.tensor([[1], [0]])
o_state = torch.tensor([[0], [1]])

# Basic gates
identity = torch.tensor([[1, 0],[0, 1]])
h_gate = 1/(torch.sqrt(torch.tensor(2))) * torch.tensor([[1, 1],[1, -1]])
x_gate = torch.tensor([[0, 1], [1, 0]])
y_gate = torch.tensor([[0, -1j], [1j, 0]], dtype=torch.complex64)
z_gate = torch.tensor([[1, 0], [0, -1]])

def innerProduct(ket0: torch.Tensor, ket1: torch.Tensor) -> torch.Tensor:
    return torch.mm(ket0.mH, ket1)

def outerProduct(ket0: torch.Tensor, ket1: torch.Tensor) -> torch.Tensor:
    return torch.mm(ket0, ket1.mH)

def kronPower(ket: torch.Tensor, times: int) -> torch.Tensor:
    result = ket
    while times > 1:
        result = torch.kron(result, ket)
        times -= 1
    
    return result.to(torch.cfloat)

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
 
# Apply gates
def applyH(ψ: torch.Tensor, i_w: int) -> torch.Tensor:
    return qubitWiseMultiply(ψ, int(math.log2(len(ψ))), h_gate, i_w)

def applyX(ψ: torch.Tensor, i_w: int) -> torch.Tensor:
    return qubitWiseMultiply(ψ, int(math.log2(len(ψ))), x_gate, i_w)

def applyY(ψ: torch.Tensor, i_w: int) -> torch.Tensor:
    return qubitWiseMultiply(ψ, int(math.log2(len(ψ))), y_gate, i_w)

def applyZ(ψ: torch.Tensor, i_w: int) -> torch.Tensor:
    return qubitWiseMultiply(ψ, int(math.log2(len(ψ))), z_gate, i_w)

def applyCNOT(ψ: torch.Tensor, i_w: int, j_w: int) -> torch.Tensor:
    return qubitWiseMultiply(ψ, int(math.log2(len(ψ))), x_gate,
        j_w, [[i_w, True]])

def applyCZ(ψ: torch.Tensor, i_w: int, j_w: int) -> torch.Tensor:
    return qubitWiseMultiply(ψ, int(math.log2(len(ψ))), z_gate, 
        j_w, [[i_w, True]])

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

def probabilities(ψ: torch.Tensor) -> torch.Tensor:
    return torch.abs(ψ.flatten())**2

def measureState(ψ: torch.Tensor) -> int:
    p = probabilities(ψ)
    collapsed = torch.multinomial(p, 1)
    
    return collapsed.item()

def measureQubit(ψ: torch.Tensor, i_w: int):
    p = [0.0, 0.0]
    for i in range(len(ψ)):
        ps = torch.abs(ψ[i])**2
        
        if ((i >> i_w) & 1): p[1] += ps
        else: p[0] += ps
    
    out = torch.multinomial(torch.tensor(p), 1).item()
    
    newψ = ψ.clone()
    for i in range(len(ψ)):
        bit = (i >> i_w) & 1
        if (bit != out): newψ[i] = 0
    
    newψ /= torch.linalg.norm(newψ)
    
    return out, newψ

def printState(ψ: torch.Tensor) -> None:
    out = ""
    
    n = int(math.log2(len(ψ)))
    first = True
    
    for i in range(len(ψ)):
        num = ψ[i].item()
        
        if abs(num) < 1e-10: continue
        
        if (abs(num.real) < 1e-10): 
            value = f"{abs(num.imag):.2f}i"
            sign = "-" if num.imag < 0 else "+"
        elif (abs(num.imag) < 1e-10): 
            value = f"{abs(num.real):.2f}"
            sign = "-" if num.real < 0 else "+"     
        else: 
            value = f"({num.real:.3f}{num.imag:+.3f}i)"
            sign = "+"

        term = f"{value}|{i:0{n}b}⟩"
        
        if (first): out += f" {sign if sign == '-' else ''}{term} "
        else: out += f"{sign} {term} "
        first = False
    
    print("|ψ⟩ =" + out)

def printProbabilities(ψ: torch.Tensor) -> None:
    out = ""
    n = int(math.log2(len(ψ)))
    ψ = probabilities(ψ)
    
    for i in range(len(ψ)):
        value = f"{(ψ[i].item())*100:.2f}"
        
        out += f"|{i:0{n}b}⟩: " + value + "%\n"
    
    print(out[:-1])

def printMeasurement(ψ: torch.Tensor) -> None:
    print(measureState(ψ))