
from __future__ import annotations

from collections.abc import Sequence
from math import isqrt

from itertools import count


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
    """Maps an n-length sequence of natural numbers onto a single natural number in a bijective fashion.
    
    Currently only implementd for 1 <= n <= 3"""
    # TODO: add checks for negative inputs
    match len(t):
        case 1:
            return t[0]
        case 2:
            return _index2(t)
        case 3:
            return _index3(t)
        case 0:
            raise ValueError("Index not meaningful for 0-length inputs")
        case _:
            raise ValueError(f"index not implemented for inputs of length {len(t)}")


def _inv_index2(n: int) -> tuple[int, int]:
    s = isqrt(n)
    if (a := n - s*s) < s:
        b = s
    else:
        a, b = s, n - s*s - s
    return a, b

def _icbrt(n: int) -> int:
    r = 0
    for i in count(1):
        if i**3 > n:
            return r
        else:
            r = i

def _euclidean_divide(quotient: int, dividend: int) -> tuple[int, int]:
    return quotient//dividend, quotient%dividend

def _inv_index3(n: int) -> int:
    c = _icbrt(n)
    if (m := n - c**3 - 2*c*c - c) >= 0:
        x, y = _euclidean_divide(m, c+1)
        return c, x, y
    else:
        m = n - c**3
        if m % (2*c+1) >= c:
            x, y = _euclidean_divide(m, 2*c+1)
            y = y - c
            return x, c, y
        else:
            x, y = _euclidean_divide(m, 2*c+1)
            return x, y, c

def inv_index(n: int, dim: int) -> tuple[int, ...]:
    """Maps a natural number n to a tuple of natural numbers of length dim. inv_index() is the inverse of index() when called with a tuple of length dim."""
    match dim:
        case 1:
            return n
        case 2:
            return _inv_index2(n)
        case 3:
            return _inv_index3(n)
        case a if a < 1:
            raise ValueError("Dimensions less than 1 are invalid")
        case _:
            raise ValueError("Indices not implemented for dim > 3")


def int_to_n(i: int) -> int:
    """Maps the input integer onto a natural number by mapping positive integers onto even natural numbers and negative integers onto odd natural numbers."""
    if i < 0:
        return -2*i - 1
    else:
        return 2*i

def n_to_int(n: int) -> int:
    """Maps the input natural number onto an integer. n_to_int() the inverse function of int_to_n()."""
    if n < 0:
        raise ValueError("Input must be a natural number (nonnegative integer)")
    if n%2 == 0:
        return n//2
    else:
        return -(n+1)//2


def int_index(t: Sequence[int])  -> int:
    """Extends index() to apply to tuples of integers by composing index() with int_to_n()"""
    return index( tuple(int_to_n(i) for i in t) )

def inv_int_index(n: int, dim: int) -> tuple[int, ...]:
    """This function is the inverse of int_index() with an input of length dim"""
    return tuple(n_to_int(m) for m in inv_index(n, dim))

