
# this script exists as a slightly more convenient way to make lattice json files
# than just hand-writing the json

import json
from math import sqrt, pi

import numpy as np

class lattice:
    def __init__(self, basis = [], points = [], point_names = [], line_points = [], dim = 0):
        self.basis = list(basis)
        self.points = list(points)
        self.point_names = list(point_names)
        self.line_points = list(line_points)
        self.dimension = dim

a = 1
direct_basis = \
[   
    [a, a, 0],
    [a, 0, a],
    [0, a, a] 
]

# a, b, c = direct_basis

# direct_triple = np.dot(a, np.cross(b, c))

# inverse_basis = \
# np.array([
#             (np.cross(b, c)/direct_triple),
#             (np.cross(c, a)/direct_triple),
#             (np.cross(a, b)/direct_triple)
# ])*(2*pi)

# l, m, n = inverse_basis
# l = list(l)
# m = list(m)
# n = list(n)


points = \
[
    (0,0,0),
    (1/2, 1/2, 0),
    (1/2, 1/2, 1/2),
    (0,0,0),
    (2/sqrt(6), 1/sqrt(6), 1/sqrt(6)),
]

point_names = \
[
    "$\Gamma$",
    "X",
    "L",
    "$\Gamma$",
    "K",
]

boundary_points = [0, 1, 2, 3, 4]

dim = 3

with open("lattices/3d_FCC.json", "w") as out:
    json.dump(lattice(direct_basis, points, point_names, boundary_points, dim).__dict__, out, indent = 4)

