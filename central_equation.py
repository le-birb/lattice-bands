
from __future__ import annotations

from itertools import product, tee
from math import isqrt

import numpy as np
import matplotlib.pyplot as p

from json_interface import load_lattice

np.set_printoptions(linewidth = 100000)

def _index(x: int, y: int) -> int:
    "Maps 2 integers into a unique natural number, or 0"
    # maps all integers onto the nonnegative integers
    a = 2*x if x >= 0 else -2*x-1
    b = 2*y if y >= 0 else -2*y-1
    return a*a + a + b if a >= b else a + b*b

def _inv_index(n: int) -> tuple[int, int]:
    s = isqrt(n)
    if n - s*s < s:
        # we landed in the else case above, s = b
        a, b = n - s*s, s
    else:
        # in the if, s = a
        a, b = s, n - s*s - s
    # now we undo the mapping of integers onto nonnegative integers
    if a % 2 == 0:
        a = a//2
    else:
        a = -(a+1)//2
    if b % 2 == 0:
        b = b//2
    else:
        b = -(b+1)//2
    return a, b


def get_bands(path, fourier_coefficients: list, band_count: int = 9) -> list:
    energy_bands = []
    for i in range(band_count):
        energy_bands.append(np.zeros(len(path)))

    # TODO: decide how to handle this coefficient
    l = 1

    energy_idx = 0
    for k in path:
        matrix = np.zeros((band_count, band_count))
        for row in range(len(matrix)): 
            for column in range(len(matrix[0])):
                # with vector indices, the (a,b)th entry in the matrix is U[a-b], remembering that a and b are vectors
                # when a = b, there is an additional h^2/2m * (k + b)^2 term added in
                a = np.array(_inv_index(row))
                b = np.array(_inv_index(column))
                try:
                    matrix[row, column] = fourier_coefficients[_index(*(a - b))]
                except IndexError:
                    pass # an index error means the fourier coefficient is outside the defined set, so we assume it is 0

                if all(a == b):
                    matrix[row, column] += l * np.dot(k + b, k + b)
        energies = np.sort(np.linalg.eigvals(matrix))
        for i in range(len(energies)):
            energy_bands[i][energy_idx] = energies[i]
        energy_idx += 1

    return energy_bands


if __name__ == "__main__":
    # temp code to test a "more physical" potential
    class typical_v(list):
        def __getitem__(self, idx):
            x, y = _inv_index(idx)
            if x == y == 0:
                return 0
            else:
                return 1/(x**2 + y**2)


    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    lat = load_lattice("lattices/2d_square.json")

    resolution = 50

    paths = []
    plot_ranges = []
    curr_range_start = 0

    for start, end in pairwise(lat.points):
        paths.append(np.linspace(start, end, num = resolution))
        plot_ranges.append(np.linspace(curr_range_start, curr_range_start + 1, num = resolution))
        curr_range_start += 1

    fig = p.figure()
    ax = fig.add_subplot(1,1,1)
    for point in lat.vertical_lines:
        p.axvline(point, linestyle = "--", color = (0, 0, 0, .5))

    # v = [0, 0, 0, 1, 0, 1, 0, 1, 1]
    v = typical_v()

    for i in range(len(paths)):
        path = paths[i]
        bands = get_bands(path, v)
        for band in bands:
            ax.plot(plot_ranges[i], band, "-k")

    p.show()
