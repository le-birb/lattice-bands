
from __future__ import annotations

from collections.abc import Sequence


def _index2(t: Sequence[int, int]) -> int:
    m = max(t)
    if t[0] == m:
        return m*m + m + t[1]
    elif t[1] == m:
        return m*m + t[0]

def _index3(t: Sequence[int, int, int]) -> int:
    m = max(t)
    if t[0] == m:
        return m**3 + 2*m*m + m + (m + 1)*t[1] + t[2]
    elif t[1] == m:
        return m**3 + m + (2*m + 1)*t[0] + t[2]
    elif t[2] == m:
        return m**3 + (2*m + 1)*t[0] + t[1]

def index(t: Sequence[int]) -> int:
    match len(t):
        case 1:
            return t[0]
        case 2:
            return _index2(t)
        case 3:
            return _index3(t)
        case _:
            raise ValueError(f"index not implemented for inputs of length {len(t)}")


def int_to_n(i: int) -> int:
    "Maps the input integer (-inf to inf range) onto a natural number (0 to inf range)"
    if i < 0:
        return -2*i - 1
    else:
        return 2*i

def n_to_int(n: int) -> int:
    "Maps the input natural number onto an integer. Is the inverse function of int_to_n()."
    if n < 0:
        raise ValueError("Input must be a natural number")
    if n%2 == 0:
        return n/2
    else:
        return -(n-1)/2


def int_index(t: Sequence[int])  -> int:
    return index( (int_to_n(i) for i in t) )

