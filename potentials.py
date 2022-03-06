

from typing import Sequence


# let it take a dummy scale argument to simplify potential settings implementation elsewhere for the moment
def empty_v(g: Sequence[int], scale: float):
    """The potential that is 0 everywhere"""
    return 0

def simple_v(g: Sequence[int], scale: float = 1):
    """A very simple potential where e.g. in 2 dimensions
    U(1,0) == U(0,1) == U(-1,0) == U(0,-1) == 1, 
    and U == 0 otherwise."""
    # U is scale if exactly one element of g is 1 or -1 and everything else is 0, otherwise it is 0
    return scale if (g.count(1) == 1 or g.count(-1) == 1) and (g.count(0) == len(g) - 1) else 0

def typical_v(g: Sequence[int], scale: float= 1):
    """A lattice potential that is in some sense "typical":
    it has U ~ 1/G**2"""
    if all(gn == 0 for gn in g):
        return 0
    return scale/sum(gn**2 for gn in g)
