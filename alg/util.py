from dataclasses import dataclass


def get_cost_default(x):
    return x


class Term:
    def __init__(self, data, get_cost):
        self.__data = data
        self.get_cost = get_cost

    @property
    def cost(self):
        return self.get_cost(self.__data)

    def __call__(self):
        return self.__data


@dataclass
class Terms:
    __terms: [Term]
    constraint: float

    def __init__(self, terms, constraint, get_cost=get_cost_default):
        t = [Term(term, get_cost) for term in terms]
        self.__terms = sorted(t, key=lambda x: x.cost)
        self.constraint = constraint

    def __len__(self):
        return len(self.__terms)

    def __getitem__(self, index):
        """
        This method returns cost of term.
        :param index: indexes of term
        :return: cost
        """
        return self.__terms[index]