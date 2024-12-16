import numpy as np

def accept_move(current, new, temperature):
    """function to accept or reject a move based on the Metropolis criterion"""
    if new > current:
        return True
    else:
        probability = np.exp((new - current) / temperature)
        return np.random.rand() < probability
    