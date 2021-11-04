
import itertools
import numpy as np
import matplotlib.pyplot as p

from math import pi, sqrt
from itertools import product


def energy(position) -> float:
    return np.dot(position, position)

def triple_product(a, b, c) -> float:
    return np.dot(a, np.cross(b, c))

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


reciprocal_range = 1

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

# here's where the third dimension is ignored
points = \
[
    (0,0,0),
    (2*pi/(3*a), 0, 0),
    (4*pi/(3*a), 0, 0),
    (pi/a, pi/(sqrt(3)*a), 0),
    (pi/(2*a), pi/(sqrt(3)*2*a)),
    (0, 0, 0)
]

point_names = \
[
    "$\Gamma$",
    "T",
    "K",
    "M",
    "$\Sigma$",
    "$\Gamma$"
]

resolution = 50

path = np.array()

for start, end in pairwise(points):
    path.append(np.linspace(start, end, num = resolution, endpoint = False))

path.append(np.array(end))

plot_range = np.linspace(0, len(points)-1, num = resolution * (len(points)-1))

