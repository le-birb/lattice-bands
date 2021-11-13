
from __future__ import annotations
from collections import defaultdict

import itertools
import numpy as np
import matplotlib.pyplot as p

from math import pi, isclose
from itertools import product, zip_longest
import tkinter
from tkinter import filedialog
import json


class lattice:
    def __init__(self, basis = [], points = [], point_names = [], vertical_lines = []):
        self.basis = list(basis)
        self.a1, self.a2, self.a3 = self.basis
        self._direct_triple = triple_product(*self.basis)
        
        self.points = list(points)
        self.point_names = list(point_names)
        self.vertical_lines = list(vertical_lines)
        
        self.reciprocal_basis = np.array(
        [
            np.cross(self.a2, self.a3)/self._direct_triple,
            np.cross(self.a3, self.a1)/self._direct_triple,
            np.cross(self.a1, self.a2)/self._direct_triple
        ])*(2*pi)
        self.b1, self.b2, self.b3 = self.reciprocal_basis

class degeneracy_tracker(defaultdict):
    __sentinel = object()

    def __init__(self):
        super().__init__(lambda : 0)

    def __contains__(self, other: object) -> bool:
        if isinstance(other, tuple):
            return any(
                all(
                    isclose(a, b) for a, b in zip_longest(member, other, fillvalue = self.__sentinel)
                )
                for member in self
            )
        else:
            return super().__contains__(other)

    def __getitem__(self, key):
        if isinstance(key, tuple):
            for member in self:
                if all(isclose(a, b) for a, b in zip_longest(member, key)):
                    return super().__getitem__(member)
            else:
                ret = self.default_factory()
                self[key] = ret
                return ret

        else:
            return super().__getitem__(key)

    def __setitem__(self, key, v) -> None:
        if isinstance(key, tuple):
            for member in self:
                if all(isclose(a, b) for a, b in zip_longest(member, key)):
                    return super().__setitem__(member, v)
            else:
                return super().__setitem__(key, v)
        else:
            return super().__setitem__(key, v)

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

def _get_lattice() -> lattice:
    # this script doesn't use any part of tkinter than the file dialog,
    # so the other window that pops up is closed with withdraw()
    root = tkinter.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(initialdir = "lattices")
    with open(filename, "r") as f:
        lattice_data: dict = json.load(f)
    return lattice(lattice_data["basis"], lattice_data["points"], lattice_data["point_names"], lattice_data["line_points"])

def plot_bands(lat: lattice, reciprocal_range = 1, resolution = 50):
    reciprocal_range = 1

    resolution = 50

    paths = []
    plot_ranges = []
    curr_range_start = 0
    seen_endpoints: list[degeneracy_tracker] = []

    for start, end in pairwise(lat.points):
        paths.append(np.linspace(start, end, num = resolution))
        plot_ranges.append(np.linspace(curr_range_start, curr_range_start + 1, num = resolution))
        curr_range_start += 1
        seen_endpoints.append(degeneracy_tracker())

    # TODO: rework this to visit only nth nearest-neighbors instead of
    # all the points within n reciprocal basis vectors away in each direction
    # this will help make sure that degeneracy is consistent
    g_range = range(-reciprocal_range, reciprocal_range + 1)
    # here is the second place to ignore the third dimension
    g_offsets = set(product(g_range, g_range, (0,)))
    g_offsets.remove((-1, 1, 0))
    g_offsets.remove((1,-1,0))

    # TODO: make sure there's a handler for if this ever runs out
    # if that situation is hit, come up with a better solution

    # position 0 is None as it should never come up
    degeneracy_colors = [None, "black", "red", "orange", "yellow", "green", "blue", "purple"]

    fig = p.figure()
    ax  = fig.add_subplot()

    for point in lat.vertical_lines:
        p.axvline(point, linestyle = "--", color = (0, 0, 0, .5))

    for i in range(len(paths)):
        path = paths[i]
        plot_range = plot_ranges[i]
        degeneracies = seen_endpoints[i]

        for offset in g_offsets:
            actual_k = (offset*lat.reciprocal_basis).sum(0)
            energies = energy(path + actual_k)
            endpoints = (energies[0], energies[-1])

            # degeneracy is checked for at the endpoints of bands, since there is only one
            # possible path between 2 endpoints
            degeneracies[endpoints] += 1

            ax.plot(plot_range, energies, color = degeneracy_colors[degeneracies[endpoints]])

    ax.set_xlabel("High Symmetry Points")
    ax.set_xticks(list(range(len(lat.points))))
    ax.set_xticklabels(lat.point_names)
    ax.set_ylabel(r"Energy, in units of $\frac{ħ^2}{2m}(\frac{π}{a})^2$")
    p.show()

# TODO: figure out how to make the script end on its own
# either that or wait until the problem isn't a problem anymore
# when a fuller GUI is made

if __name__ == "__main__":
    lat = _get_lattice()
    plot_bands(lat)