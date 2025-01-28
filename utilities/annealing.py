import numpy as np

def accept_move(current, new, temperature):
    """Function to accept or reject a move based on the Metropolis criterion"""
    if new > current:
        return True
    else:
        if temperature > 1e-7:
            delta = new - current
            if abs(delta) < 1e-7:
                probability = 1
            else:
                exponent = delta / temperature
                exponent = np.clip(exponent, -700, 700)
                probability = np.exp(exponent)
        else:
            probability = 0
        return np.random.rand() < probability