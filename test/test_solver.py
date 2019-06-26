from tabeltests import utils
from tabeltests.utils import SubTest

from alg.brute_force import BruteForceSolver
from alg.fast_bisect_solver import FastBisectSolver
from alg.knapsack import KnapsackSolver
from alg.util import Terms


class TestsGenerator:
    @staticmethod
    def __postprocessing(solve):
        s = [[term.cost for term in terms] for terms in solve]
        return sorted([sorted(terms) for terms in s])

    def __call__(self, obj_factory):
        self.__obj_factory = obj_factory
        return self

    def __iter__(self):
        self.tests = (
            SubTest(
                name="Single solve",
                description="This test returns the only solve",
                object=self.__obj_factory(),
                args={'terms': Terms(terms=[1, 2, 3], constraint=5)},
                answer_processors=[self.__postprocessing],
                want=[[2, 3]],
            ),
            SubTest(
                name="Two the same solves",
                description="This test returns two the same solves, which generate with a different items",
                object=self.__obj_factory(),
                args={'terms': Terms(terms=[2, 2, 3], constraint=5)},
                answer_processors=[self.__postprocessing],
                want=[[2, 3], [2, 3]],
            ),
            SubTest(
                name="Three solves",
                description="This test returns three solves",
                object=self.__obj_factory(),
                args={'terms': Terms(terms=[1, 2, 2, 3], constraint=5)},
                answer_processors=[self.__postprocessing],
                want=[[1, 2, 2], [2, 3], [2, 3]],
            ),
            SubTest(
                name="Zero item",
                description="This test returns two solves. Zero item doesn't uses",
                object=self.__obj_factory(),
                args={'terms': Terms(terms=[0, 1, 2, 3], constraint=5)},
                exception=AssertionError,
            ),
            SubTest(
                name="Item more constraint",
                description="This test returns two solves. There is an element which more constraint. This item skips",
                object=self.__obj_factory(),
                args={'terms': Terms(terms=[1, 2, 3, 6], constraint=5)},
                answer_processors=[self.__postprocessing],
                want=[[2, 3]],
            ),
            SubTest(
                name="Not sorted input",
                description="Algorithm sorts elements before executing. This test checks this case",
                object=self.__obj_factory(),
                args={'terms': Terms(terms=[6, 2, 3, 1], constraint=5)},
                answer_processors=[self.__postprocessing],
                want=[[2, 3]],
            ),
            SubTest(
                name="Zero constraint",
                description="Assertion",
                object=self.__obj_factory(),
                args={'terms': Terms(terms=[1, 2, 3], constraint=0)},
                exception=AssertionError
            ),
            SubTest(
                name="Not positive element",
                description="Assertion",
                object=self.__obj_factory(),
                args={'terms': Terms(terms=[-11, 2, 3], constraint=5)},
                exception=AssertionError
            ),
            SubTest(
                name="Big test",
                description="This test contains a big count of solves",
                object=self.__obj_factory(),
                args={'terms': Terms(terms=[1, 2, 3, 6, 6, 8, 10, 15], constraint=22)},
                answer_processors=[self.__postprocessing],
                want=[
                    [1, 2, 3, 6, 10],
                    [1, 2, 3, 6, 10],
                    [1, 3, 8, 10],
                    [1, 6, 15],
                    [1, 6, 15],
                    [2, 6, 6, 8],
                    [6, 6, 10]
                ],
            ),
            SubTest(
                name="Big test",
                description="This test contains an element equals constrain",
                object=self.__obj_factory(),
                args={'terms': Terms(terms=[10, 10, 2, 22], constraint=22)},
                answer_processors=[self.__postprocessing],
                want=[
                    [2, 10, 10],
                    [22],
                ],
            ),
        )
        for test in self.tests:
            yield test


class TestFastBisectSolver(utils.BaseTestClass):

    def setUp(self):
        generator = TestsGenerator()
        self.tests = generator(FastBisectSolver)

    def test(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: [item for item in obj(**kwargs)])


class TestBruteForceSolver(utils.BaseTestClass):

    def setUp(self):
        generator = TestsGenerator()
        self.tests = generator(BruteForceSolver)

    def test(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: [item for item in obj(**kwargs)])


class TestKnapsackSolver(utils.BaseTestClass):

    def setUp(self):
        generator = TestsGenerator()
        self.tests = generator(KnapsackSolver)

    def test(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: [item for item in obj(**kwargs)])



