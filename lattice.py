
from itertools import tee
import numpy as np
from math import pi

def _triple_product(a, b, c) -> float:
    return np.dot(a, np.cross(b, c))

def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

class lattice:
    def __init__(self, basis = [], dimension = 0, points = [], point_names = [], vertical_lines = []):
        self.basis = list(basis)
        self._a1, self._a2, self._a3 = self.basis
        self._direct_triple = _triple_product(*self.basis)
        
        self.points = list(points)
        self.point_names = list(point_names)
        self.vertical_lines = list(vertical_lines)
        
        self.reciprocal_basis = np.array(
        [
            (np.cross(self._a2, self._a3)/self._direct_triple)[0:dimension],
            (np.cross(self._a3, self._a1)/self._direct_triple)[0:dimension],
            (np.cross(self._a1, self._a2)/self._direct_triple)[0:dimension]
        ])[0:dimension]*(2*pi)
        
    # TODO: express path points in terms of reciprocal basis
    def get_paths(self, resolution: int) -> list[np.ndarray]:
        paths = []
        for start, end in _pairwise(self.points):
            paths.append(np.linspace(start, end, resolution))
        return paths