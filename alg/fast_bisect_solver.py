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
class FastBisectSolver:
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
        return self

    def __modify(self, state):
        residue = state.residue+self.terms[state.path[-1]].cost
        return State(residue=residue, solve=state.solve[:-1], path=state.path[:-1], step=state.path[-1])

    def __get_start_state(self):
        start_step = len(self.terms) - 1
        start_solve = [self.terms[-1]]
        c = self.terms.constraint
        residue = c - start_solve[0].cost
        return State(residue=residue, solve=[start_solve[-1]], path=[start_step], step=start_step)

    def __iter__(self):
        if self.terms is None:
            return
        assert self.terms.constraint > 0, 'constraint must be > 0'
        assert len([item.cost for item in self.terms if item.cost > 0]) == len(self.terms), 'all items must be > 0'
        s = self.__get_start_state()
        while True:
            if abs(s.residue) < self.eps:
                yield s.solve
                s = self.__modify(s)
                continue
            if s.residue < 0:
                s = self.__modify(s)
                continue
            # Interval [l0, hi) is less that length of terms size
            s.step = bisect_right(self.terms, s.residue, lo=0, hi=s.step) - 1
            if s.step < 0 and len(s.solve) == 0:
                break
            if s.step < 0:
                s = self.__modify(s)
                continue
            s.residue -= self.terms[s.step].cost
            s.path.append(s.step)
            s.solve.append(self.terms[s.step])
        self.terms = None
