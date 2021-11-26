
import numpy as np
from math import pi

def _triple_product(a, b, c) -> float:
    return np.dot(a, np.cross(b, c))

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
        
