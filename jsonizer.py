
# this script exists as a slightly more convenient way to make lattice json files
# than just hand-writing the json

import json
from math import sqrt, pi

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

points = \
[
    (0,0,0),
    (1/2, 1/2, 1/2),
    (1/2, 1/2, 0),
    (2/sqrt(6), 1/sqrt(6), 1/sqrt(6)),
    (0,0,0),
]

point_names = \
[
    "$\Gamma$",
    "L",
    "X",
    "K",
    "$\Gamma$",
]

boundary_points = [0, 2, 3, 5]

dim = 2

with open("lattices/3d_FCC.json", "w") as out:
    json.dump(lattice(direct_basis, points, point_names, boundary_points, dim).__dict__, out, indent = 4)

