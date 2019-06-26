from dataclasses import dataclass
from typing import Optional

from alg.util import Terms


@dataclass
class State:
    residue: float
    step: int
    solve: [float]
    path: [int]


def bisect_right(a, x, lo=0, hi=None):
    """
    This function we extract from bisect package of python3.7. We needs custom field of input array

    Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e <= x, and all e in
    a[i:] have e > x.  So if x already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if x < a[mid].cost:
            hi = mid
        else:
            lo = mid+1
    return lo


@dataclass
class BruteForceSolver:
    terms: Optional[Terms]

    def __init__(self, eps=0.00001):
        """
        FastSolver implements solve of problem factorisation number by array of addend
        :param eps: machine epsilon
        """
        self.terms = None
        self.eps = eps

    def __call__(self, terms):
        self.terms = terms
        self.__mask = [0] * len(self.terms)
        return self

    def __get_solve(self):
        return [self.terms[i] for i, b in enumerate(self.__mask) if b == 1]

    def __check_solve(self, solve):
        residue = self.terms.constraint
        for item in solve:
            residue -= item.cost
        return residue == 0

    def __iter__(self):
        if self.terms is None:
            return
        assert self.terms.constraint > 0, 'constraint must be > 0'
        assert len([item.cost for item in self.terms if item.cost > 0]) == len(self.terms), 'all items must be > 0'
        while True:
            j = 0
            while j < len(self.terms) and self.__mask[j] == 1:
                self.__mask[j] = 0
                j += 1
            if j == len(self.terms):
                break
            self.__mask[j] = 1
            solve = self.__get_solve()
            if self.__check_solve(solve):
                yield solve
