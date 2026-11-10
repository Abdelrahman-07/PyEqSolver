"""Parser tests: cases 10 to 13 of the specification's test table."""

import unittest
from pathlib import Path

from pyeqsolver import EquationParser
from pyeqsolver.exceptions import InvalidFileFormatException

DATA = Path(__file__).resolve().parent / "data"


class ParserTests(unittest.TestCase):
    def test_case10_missing_equals_sign(self):
        with self.assertRaises(InvalidFileFormatException) as ctx:
            EquationParser(file_path=DATA / "case10_missing_equals.txt").parse()
        self.assertIn("Line 1", str(ctx.exception))

    def test_case11_brackets(self):
        with self.assertRaises(InvalidFileFormatException):
            EquationParser(file_path=DATA / "case11_brackets.txt").parse()

    def test_case12_empty_file_or_only_comments(self):
        for name in ("case12_empty.txt", "case12_only_comments.txt"):
            with self.subTest(file=name):
                with self.assertRaises(InvalidFileFormatException):
                    EquationParser(file_path=DATA / name).parse()

    def test_case13_path_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            EquationParser(file_path=DATA / "does_not_exist.txt").parse()


if __name__ == "__main__":
    unittest.main()
