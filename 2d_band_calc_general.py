
import itertools
import numpy as np
import matplotlib.pyplot as p

from math import pi, sqrt
from itertools import product


def energy(positions):
    "Takes a list of vector positions and returns a list of energies"
    # squares each element of each vector, then sums the terms of each vector
    return (positions**2).sum(1)

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
    (pi/(2*a), pi/(sqrt(3)*2*a), 0),
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

boundary_points = [0, 2, 3, 5]

resolution = 50

paths = []
plot_ranges = []
curr_range_start = 0
seen_endpoints: list[set] = []

for start, end in pairwise(points):
    paths.append(np.linspace(start, end, num = resolution))
    plot_ranges.append(np.linspace(curr_range_start, curr_range_start + 1, num = resolution))
    curr_range_start += 1
    seen_endpoints.append({})

g_range = range(-reciprocal_range, reciprocal_range + 1)
# here is the second place to ignore the third dimension
g_offsets = tuple(product(g_range, g_range, (0,)))

# TODO: make sure there's a handler for if this ever runs out
# if that situation is hit, come up with a better solution
degeneracy_colors = ["black", "red", "orange", "yellow", "green", "blue", "purple"]

fig = p.figure()
ax  = fig.add_subplot()

for point in boundary_points:
    p.axvline(point, linestyle = "--", color = (0, 0, 0, .5))

for i in range(len(paths)):
    path = paths[i]
    plot_range = plot_ranges[i]
    degeneracies = seen_endpoints[i]

    for offset in g_offsets:
        actual_k = (offset*reciprocal_basis).sum(0)
        energies = energy(path + actual_k)
        endpoints = (energies[0], energies[-1])

        # degeneracy is checked for at the endpoints of bands, since there is only one
        # possible path between 2 endpoints
        if endpoints in degeneracies:
            degeneracies[endpoints] += 1
        else:
            degeneracies[endpoints] = 0

        ax.plot(plot_range, energies, color = degeneracy_colors[degeneracies[endpoints]])

ax.set_xlabel("High Symmetry Points")
ax.set_xticks(list(range(len(points))))
ax.set_xticklabels(point_names)
ax.set_ylabel(r"Energy, in units of $\frac{ħ^2}{2m}(\frac{π}{a})^2$")
p.show()
