
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

    a = _inv_index(band_count - 1)[0]

    energy_idx = 0
    for k in path:
        matrix = np.zeros((band_count, band_count))
        for row in range(len(matrix)): 
            G = np.array(_inv_index(row))
            for G_prime in product(range(-a, a+1), repeat = 2):
                G_prime = np.array(G_prime)
                try:
                    matrix[row][_index(*G_prime)] += fourier_coefficients[_index(*(G - G_prime))]
                except IndexError:
                    # if the matrix index is out of range, that term is thrown out
                    # if the fourier coefficient is out of bounds, we assume it is 0 and thus adds nothing
                    pass
        for i in range(len(matrix)):
            G = np.array(_inv_index(i))
            matrix[i][i] += np.dot(k - G, k - G)
        energies = np.sort(np.linalg.eigvals(matrix))
        for i in range(len(energies)):
            energy_bands[i][energy_idx] = energies[i]
        energy_idx += 1

    return energy_bands


if __name__ == "__main__":
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

    for i in range(len(paths)):
        path = paths[i]
        bands = get_bands(path, [0, 0, 0, 1, 0, 1, 0, 1, 1])
        for band in bands:
            ax.plot(plot_ranges[i], band, "-k")

p.show()
