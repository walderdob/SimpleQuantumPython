import sys
sys.path.insert(0, '../')
from sqp import *
import torch

def entanglement():
    n = 2
    ψ = kronPower(z_state, n)
    ψ = applyH(ψ, 0)
    ψ = applyCNOT(ψ, 0, 1)
    
    return ψ

def main():
    printState(entanglement())
    printProbabilities(entanglement())
    
if __name__ == '__main__':
    main()