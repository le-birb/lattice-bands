
# this script exists as a slightly more convenient way to make lattice json files
# than just hand-writing the json

import json
from math import sqrt, pi

class lattice:
    def __init__(self, basis = [], points = [], point_names = [], line_points = []):
        self.basis = list(basis)
        self.points = list(points)
        self.point_names = list(point_names)
        self.line_points = list(line_points)

a = 1
direct_basis = \
[   
    [a, 0, 0],
    [0, a, 0],
    [0, 0, 1] 
]

points = \
[
    (0,0,0),
    (pi/(2*a), 0,0),
    (pi/a, 0, 0),
    (pi/a, pi/(2*a), 0),
    (pi/a, pi/a, 0),
    (pi/(2*a), pi/(2*a), 0),
    (0,0,0)
]

point_names = \
[
    "$\Gamma$", 
    "$\Delta$", 
    "X", 
    "Z", 
    "M", 
    "$\Sigma$", 
    "$\Gamma$"
]

boundary_points = [0, 2, 4, 6]

with open("lattices/2d_square.json", "w") as out:
    json.dump(lattice(direct_basis, points, point_names, boundary_points).__dict__, out, indent = 4)

