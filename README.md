# PyEqSolver: Linear System Solver via Gaussian Elimination

Reads a system of linear equations from a text file, solves it with a hand-written
Gaussian elimination, and writes the result to a JSON file. If the system cannot be
solved, it explains why instead of crashing.

```
10x1 + 5x2 = 5          ->   x1 = 0.0
4x2 + 3x3 = 10          ->   x2 = 1.0
x1 + 6x3 = 12           ->   x3 = 2.0
```

Pure Python 3.10+, standard library only. No `pip install`.

## Run the program

From the project root:

```bash
python main.py
# reads data/input_equations.txt and writes data/solution.json
```

The exit status is 0 when the system is solved and 1 on any error. Either way
`data/solution.json` is written (a `SUCCESS` or an `ERROR` object).

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The 13 required cases use the files in `tests/data/`.

## Sample inputs

`data/` holds one success case and one case per error type:

| File | Result |
|---|---|
| `data/sample_success.txt` | solves: x = 5, y = 3, z = -2 |
| `data/sample_invalid_format.txt` | `InvalidFileFormatException` |
| `data/sample_dimension_mismatch.txt` | `DimensionMismatchException` |
| `data/sample_inconsistent.txt` | `InconsistentSystemException` |
| `data/sample_infinite.txt` | `InfiniteSolutionsException` |

`main.py` always reads `data/input_equations.txt`. To try a sample, either copy it
over that file, or call the function with a file name:

```bash
python -c "import main; main.main('data/sample_inconsistent.txt')"
```

## Input format

One equation per line, variables on the left of `=` and a single number on the right.

- Variable names: a letter or `_`, then letters, digits or `_` (`x`, `x1`, `price_2`).
  Variables are ordered by first appearance in the file.
- Coefficients may be integers or decimals, positive or negative: `3x`, `-2.5y`,
  `+ 0.75z`. A bare `x` means 1 and `-x` means -1. An optional `*` is allowed: `3*x`.
- Spaces around operators are optional: `2x+3y=5` and `2x + 3y = 5` are the same.
- A variable missing from a line gets coefficient 0. Repeated variables are added:
  `2x + 3x = 10` gives coefficient 5.
- Blank lines and lines starting with `#` are skipped.

A line is invalid (`InvalidFileFormatException`, naming the line number and the text) if it has
no `=` or more than one, an empty side, a character other than digits, letters, `_ . + - * =`
and spaces (brackets are not supported), two operators in a row, or a number with no
variable on the left side. Example message:

```
Line 2: missing '=' in "4x2 + 3x3 10"
```

## Output

Success:

```json
{
  "status": "SUCCESS",
  "system_info": {
    "num_variables": 3,
    "num_equations": 3
  },
  "solution": {
    "x1": 0.0,
    "x2": 1.0,
    "x3": 2.0
  }
}
```

Error (`error_type` is the exception's class name):

```json
{
  "status": "ERROR",
  "error_type": "InconsistentSystemException",
  "message": "The system has no solution (row reduces to 0 = 5)"
}
```

## How no-solution and infinite-solution systems are detected

The solver first compares the number of equations with the number of variables and raises DimensionMismatchException if there are fewer equations. It then runs Gauss-Jordan elimination. For each column it picks a pivot (swapping a zero pivot with the first lower row that has a non-zero entry), scales the pivot row so the pivot is 1, and subtracts multiples of it from every other row, treating any value below 1e-9 as zero. The number of pivots found is the rank. A row below the rank whose constant is not zero reads 0 = c, which raises InconsistentSystemException. If the rank is smaller than the number of variables, it raises InfiniteSolutionsException. Otherwise every column has a pivot, the left side has become the identity matrix, and the last column holds the solution.

## Project layout

```
PyEqSolver/
├── pyeqsolver/
│   ├── __init__.py      exports EquationParser, GaussianSolver, JSONExporter
│   ├── exceptions.py    PyEqSolverError and its 4 subclasses
│   ├── parser.py        EquationParser
│   ├── solver.py        GaussianSolver
│   └── exporter.py      JSONExporter
├── tests/ 
│   ├──data/          
│   ├──test_parser.py
│   └──test_solver.py
├── data/                input_equations.txt and the sample files
├── main.py              entry point
└── README.md
```
