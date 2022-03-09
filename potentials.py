

from collections import defaultdict
from numpy import unique
from numpy import ndarray


# let it take a dummy scale argument to simplify potential settings implementation elsewhere for the moment
def empty_v(g: ndarray, scale: float):
    """The potential that is 0 everywhere"""
    return 0

def simple_v(g: ndarray, scale: float = 1):
    """A very simple potential where e.g. in 2 dimensions
    U(1,0) == U(0,1) == U(-1,0) == U(0,-1) == 1, 
    and U == 0 otherwise."""
    e = defaultdict(lambda: 0, zip(*unique(g, return_counts = True)))
    if (e[1] == 1) ^ (e[-1] == 1) and e[0] == len(g) - 1:
        return scale
    else:
        return 0

def typical_v(g: ndarray, scale: float= 1):
    """A lattice potential that is in some sense "typical":
    it has U ~ 1/G**2"""
    if all(gn == 0 for gn in g):
        return 0
    return scale/sum(gn**2 for gn in g)
