
import numpy as np
import matplotlib.pyplot as p

from math import pi, sqrt
from itertools import product


def energy(position) -> float:
    return np.dot(position, position)

def triple_product(a, b, c) -> float:
    return np.dot(a, np.cross(b, c))


g_range = 1

a = 1
direct_basis = \
np.array([   # these basis vectors are hard-coded for a hexagonal lattice
    # they are 3-d but the 3rd dimension will be ignored later
    [a, 0, 0],
    [a/2, sqrt(3)/2 * a, 0],
    [0, 0, 1] # as the lattice is 2d right now, the height doesn't matter
])
# common symbols for the vectors, for brevity
a1, a2, a3 = direct_basis

direct_triple = triple_product(*direct_basis)

reciprocal_basis = 2*pi* \
np.array([
    np.cross(a2, a3)/direct_triple,
    np.cross(a3, a1)/direct_triple,
    np.cross(a1, a2)/direct_triple
])

b1, b2, b3 = reciprocal_basis

