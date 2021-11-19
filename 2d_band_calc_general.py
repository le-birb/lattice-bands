
from __future__ import annotations
from collections import defaultdict

import itertools
import numpy as np
import matplotlib.pyplot as p

from math import ceil, pi, isclose
from itertools import product, zip_longest, dropwhile
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

class histogram:
    def __init__(self, init_range: float, bin_size: float):
        self.bin_size = bin_size
        self.max = ceil(init_range/bin_size) * bin_size
        self.bin_count = ceil(self.max/bin_size)
        self._bins: dict = {idx*bin_size: 0 for idx in range(1, self.bin_count + 1)}

        self.items = self._bins.items

    def add(self, x: float):
        if x > self.max:
            pass
        
        for key in self._bins:
            if key > x:
                self._bins[key] += 1
                break
        else:
            self.max = ceil((x+(x-self.max)/2)/self.bin_size) * self.bin_size
            new_bin_count = ceil(self.max/self.bin_size)
            new_entries = {idx*self.bin_size: 0 for idx in range(self.bin_count + 1, new_bin_count + 1)}
            self._bins.update(new_entries)
            for key in dropwhile(lambda k: k/self.bin_size < self.bin_count, self._bins):
                if key > x:
                    self._bins[key] += 1
                    break
            self.bin_count = new_bin_count

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
    
    # bin_size here is a total guess, gonna have to tweak it
    state_densities = histogram(init_range = reciprocal_range**2 * np.dot(lat.b1 + lat.b2, lat.b1 + lat.b2), bin_size = 50/resolution)

    fig = p.figure()
    ax  = fig.add_subplot(2, 1, 1)

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

            # add energies to density of states plot
            for e in energies:
                state_densities.add(e)

            ax.plot(plot_range, energies, color = degeneracy_colors[degeneracies[endpoints]])

    ax.set_xlabel("High Symmetry Points")
    ax.set_xticks(list(range(len(lat.points))))
    ax.set_xticklabels(lat.point_names)
    ax.set_ylabel(r"Energy, in units of $\frac{ħ^2}{2m}(\frac{π}{a})^2$")
    
    dax = fig.add_subplot(2, 1, 2)
    dax.set_xlabel(r"Energy, in units of $\frac{ħ^2}{2m}(\frac{π}{a})^2$")
    dax.set_ylabel("Density")
    
    density_data = np.array(list(state_densities.items()))
    dax.plot(density_data[:,0], density_data[:,1])

    p.show()

# TODO: figure out how to make the script end on its own
# either that or wait until the problem isn't a problem anymore
# when a fuller GUI is made

if __name__ == "__main__":
    lat = _get_lattice()
    plot_bands(lat)