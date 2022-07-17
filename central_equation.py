
from __future__ import annotations
from functools import partial

from itertools import chain, product, repeat, tee
from numbers import Number
from typing import Callable

import numpy as np
import matplotlib.pyplot as p

from json_interface import load_lattice
from indexing import int_index as index
from indexing import inv_int_index as inv_index
from potentials import *

np.set_printoptions(linewidth = 100000)


def get_energies(k, matrix_size, fourier_coefficients: Callable):
    # temporarily set to 1, here to change later if it matters
    l = 1

    matrix = np.zeros((matrix_size, matrix_size))

    for row, column in np.ndindex(matrix.shape):
        # with vector indices, the (a,b)th entry in the matrix is U[a-b], remembering that a and b are vectors
        # when a = b, there is an additional h^2/2m * (k + b)^2 term added in
        a = np.array(inv_index(row, len(k)))
        b = np.array(inv_index(column, len(k)))
        u = fourier_coefficients(a - b)
        matrix[row, column] = u

        if all(a == b):
            matrix[row, column] += l * np.dot(k + b, k + b)
    return np.linalg.eigvals(matrix)


def get_bands(path, fourier_coefficients: Callable, band_count: int = 9) -> list[np.ndarray]:
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

