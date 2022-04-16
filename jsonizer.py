
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
    [a, 0, 0],
    [-a/2, a*sqrt(3)/2, 0],
    [0, 0, 1] 
]

points = \
[
    (0,0,0),
    (1/6, 1/6, 0),
    (1/3, 1/3, 0),
    (0, .5, 0),
    (0, .25, 0),
    (0,0,0)
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

boundary_points = [0, 2, 3, 5]

dim = 2

with open("lattices/2d_hexagonal.json", "w") as out:
    json.dump(lattice(direct_basis, points, point_names, boundary_points, dim).__dict__, out, indent = 4)

