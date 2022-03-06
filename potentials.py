

from typing import Sequence


# let it take a dummy scale argument to simplify potential settings implementation elsewhere for the moment
def empty_v(g: Sequence[int], scale: float):
    """The potential that is 0 everywhere"""
    return 0

def simple_v(g: Sequence[int], scale: float = 1):
    """A very simple potential where 
    U(1,0) == U(0,1) == U(-1,0) == U(0,-1) == 1, 
    and U == 0 otherwise."""
    return sum(map(lambda x: abs(x) == 1, g)) == 1

def typical_v(g: Sequence[int], scale: float= 1):
    """A lattice potential that is in some sense "typical":
    it has U ~ 1/G**2"""
    if all(gn == 0 for gn in g):
        return 0
    return scale/sum(gn**2 for gn in g)
