import numpy as np

def accept_move(current, new, temperature):
    """function to accept or reject a move based on the Metropolis criterion"""
    if new > current:
        return True
    else:
        if temperature < 1e-7:
            probability = np.exp((new - current) / temperature)
        else:
            probability = 0

        return np.random.rand() < probability