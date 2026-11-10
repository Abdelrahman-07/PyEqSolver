"""Entry point: read data/input_equations.txt, solve, write data/solution.json."""

import sys

from pyeqsolver import EquationParser, GaussianSolver, JSONExporter
from pyeqsolver.exceptions import PyEqSolverError

INPUT_FILE = "data/input_equations.txt"
OUTPUT_FILE = "data/solution.json"


def main(input_file: str = INPUT_FILE, output_file: str = OUTPUT_FILE) -> int:
    """Run the whole pipeline. Returns 0 on success and 1 on any error."""
    exporter = JSONExporter(output_path=output_file)

    try:
        # 1. Parse equations from the file
        parser = EquationParser(file_path=input_file)
        matrix, variables = parser.parse()

        # 2. Solve with Gaussian Elimination
        solver = GaussianSolver(matrix=matrix, variables=variables)
        solutions = solver.solve()

        # 3. Export the result
        exporter.save(solutions=solutions, metadata=solver.get_metadata())
        print(f"Solved. Results written to {output_file}")
        return 0

    except (PyEqSolverError, FileNotFoundError) as e:
        exporter.save_error(e)
        print(f"Could not solve the system: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
