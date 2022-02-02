
from __future__ import annotations

from itertools import product, tee
from numbers import Number

import numpy as np
import matplotlib.pyplot as p

from json_interface import load_lattice
from indexing import int_index as index
from indexing import inv_int_index as inv_index

np.set_printoptions(linewidth = 100000)


def get_energies(k, band_count, fourier_coefficients: list):
    # temporarily set to 1, here to change later if it matters
    l = 1

    matrix = np.zeros((band_count, band_count))
    for row in range(len(matrix)): 
        for column in range(len(matrix[0])):
            # with vector indices, the (a,b)th entry in the matrix is U[a-b], remembering that a and b are vectors
            # when a = b, there is an additional h^2/2m * (k + b)^2 term added in
            a = np.array(inv_index(row, len(k)))
            b = np.array(inv_index(column, len(k)))
            try:
                matrix[row, column] = fourier_coefficients[index(a - b)]
            except IndexError:
                pass # an index error means the fourier coefficient is outside the defined set, so we assume it is 0

            if all(a == b):
                matrix[row, column] += l * np.dot(k + b, k + b)
    return np.linalg.eigvals(matrix)


def get_bands(path, fourier_coefficients: list, band_count: int = 9) -> list:
    energy_bands = []
    for i in range(band_count):
        energy_bands.append(np.zeros(len(path)))

    energy_idx = 0
    for k in path:
        energies = get_energies(k, band_count, fourier_coefficients)
        energies = np.sort(energies)
        for i, energy in enumerate(energies):
            energy_bands[i][energy_idx] = energy
        energy_idx += 1

    return energy_bands


if __name__ == "__main__":
    # temp code to test a "more physical" potential
    class typical_v(list):
        def __init__(self, scale: Number = 1, dimension = 2):
            super().__init__()
            self.scale = scale
            self.dimension = dimension

        def __getitem__(self, idx):
            x, y = inv_index(idx, self.dimension)
            if x == y == 0:
                return 0
            else:
                return self.scale/(x**2 + y**2)


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
        p.axvline(point, linestyle = "--", color = (.5, .5, .5, .5))

    v_simple = [0, 0, 0, 1, 0, 1, 0, 1, 1]
    vt = typical_v(10)
    zero_v = []

    band_count = 9

    for i, path in enumerate(paths):
        bands = get_bands(path, vt, band_count)
        bands_0 = get_bands(path, zero_v, band_count)
        for band_0, band in zip(bands_0, bands):
            ax.plot(plot_ranges[i], band_0, color = (.5, .5, .5), linestyle = "dashed")
            ax.plot(plot_ranges[i], band, "-k")

    p.show()
