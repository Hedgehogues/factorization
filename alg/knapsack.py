from dataclasses import dataclass
from typing import Optional

from alg.util import Terms


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
class KnapsackSolver:
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

    def __rec(self, k, residue):
        if k < 0 or residue < 0:
            return []
        if residue == 0:
            return [[]]
        solves_0 = self.__rec(k - 1, residue - self.terms[k - 1].cost)
        solves_1 = self.__rec(k - 1, residue)
        answ = []
        for i, s in enumerate(solves_0):
            s.append(self.terms[k - 1])
            answ.append(s)
        return answ + solves_1

    def __iter__(self):
        if self.terms is None:
            return
        assert self.terms.constraint > 0, 'constraint must be > 0'
        assert len([item.cost for item in self.terms if item.cost > 0]) == len(self.terms), 'all items must be > 0'
        for item in self.__rec(len(self.terms), self.terms.constraint):
            yield item
