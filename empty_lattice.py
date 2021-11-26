
from __future__ import annotations
from collections import defaultdict

import numpy as np

from math import ceil, isclose
from itertools import product, zip_longest, dropwhile, tee

from lattice import lattice

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
            self.max = ceil((x+(x-self.max)/2)/self.bin_size) * self.bin_size  + 10 # add a constant to buffer some for small x - self.max
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

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def get_g_vectors(reciprocal_basis, distance: int):
    multiples = np.array(list(product(range(-distance, distance + 1), repeat = len(reciprocal_basis))))
    # matrix multiplication is a shortcut here, I don't know if there's a good reason to use it other than it works
    # basically, it adds up the contributions of each reciprocal basis vector according to each 'multiple' tuple
    offsets = multiples @ reciprocal_basis
    max_distance = max(distance * np.linalg.norm(base) for base in reciprocal_basis)
    return list(filter(lambda x: np.linalg.norm(x) <= max_distance, offsets))

# TODO: remove density of states plotting from this function, and change it to take axes rather than a figure
def plot_bands(lat: lattice, axes, reciprocal_range = 1, resolution = 50, plot_density = False):
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

    g_offsets = get_g_vectors(lat.reciprocal_basis, reciprocal_range)

    # TODO: make sure there's a handler for if this ever runs out
    # if that situation is hit, come up with a better solution
    # position 0 is None as it should never come up
    degeneracy_colors = [None, "black", "red", "orange", "yellow", "green", "blue", "purple"]
    
    if plot_density:
        # bin_size here is a total guess, gonna have to tweak it
        state_densities = histogram(init_range = reciprocal_range**2 * np.dot(sum(lat.reciprocal_basis), sum(lat.reciprocal_basis)), bin_size = 50/resolution)

    axes.vlines(lat.vertical_lines, 0, 1, transform = axes.get_xaxis_transform(), linestyle = "--", color = (0, 0, 0, .5))

    for i in range(len(paths)):
        path = paths[i]
        plot_range = plot_ranges[i]
        degeneracies = seen_endpoints[i]

        for offset in g_offsets:
            energies = energy(path + offset)
            endpoints = (energies[0], energies[-1])

            # degeneracy is checked for at the endpoints of bands, since there is only one
            # possible path between 2 endpoints
            degeneracies[endpoints] += 1

            if plot_density:
                # add energies to density of states plot
                for e in energies:
                    state_densities.add(e)

            axes.plot(plot_range, energies, color = degeneracy_colors[degeneracies[endpoints]])
