"""Solver tests: cases 1 to 9 of the specification's test table."""

import unittest
import os
from pyeqsolver import EquationParser, GaussianSolver
from pyeqsolver.exceptions import (
    DimensionMismatchException,
    InconsistentSystemException,
    InfiniteSolutionsException,
)

DATA = "tests/data"


def solve_file(name):
    matrix, variables = EquationParser(file_path=os.path.join(DATA, name)).parse()
    return GaussianSolver(matrix=matrix, variables=variables).solve()


class SolverTests(unittest.TestCase):
    def assertSolution(self, actual, expected):
        self.assertEqual(list(actual), list(expected))
        for name, value in expected.items():
            self.assertAlmostEqual(actual[name], value, places=4)

    def test_case1_unique_solution(self):
        self.assertSolution(solve_file("case01_unique.txt"), {"x1": 0, "x2": 1, "x3": 2})

    def test_case2_needs_a_row_swap(self):
        self.assertSolution(solve_file("case02_row_swap.txt"), {"x": 1, "y": 2, "z": 3})

    def test_case3_decimal_coefficients(self):
        self.assertSolution(solve_file("case03_decimals.txt"), {"a": 1, "b": 2})

    def test_case4_single_equation(self):
        self.assertSolution(solve_file("case04_single.txt"), {"x": 0.3333})

    def test_case5_repeated_variable(self):
        self.assertSolution(solve_file("case05_repeated.txt"), {"x": 2})

    def test_case6_extra_consistent_equation(self):
        self.assertSolution(solve_file("case06_extra_equation.txt"), {"x": 2, "y": 1})

    def test_case7_inconsistent(self):
        with self.assertRaises(InconsistentSystemException):
            solve_file("case07_inconsistent.txt")

    def test_case8_infinite_solutions(self):
        with self.assertRaises(InfiniteSolutionsException):
            solve_file("case08_infinite.txt")

    def test_case9_dimension_mismatch(self):
        with self.assertRaises(DimensionMismatchException):
            solve_file("case09_dimension.txt")


if __name__ == "__main__":
    unittest.main()
