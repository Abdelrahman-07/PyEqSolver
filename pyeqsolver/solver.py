"""Gaussian elimination on plain Python lists."""

from .exceptions import (
    DimensionMismatchException,
    InconsistentSystemException,
    InfiniteSolutionsException,
)


class GaussianSolver:
    """Solve a linear system with forward elimination and back substitution.

    Args:
        matrix: Augmented matrix, one row [a1, ..., an, b] per equation.
            It is copied, never modified.
        variables: Variable names in column order.
    """

    TOLERANCE = 1e-9  # a number with absolute value below this counts as zero

    def __init__(self, matrix: list[list[float]], variables: list[str]) -> None:
        self._matrix = matrix
        self._variables = variables

    def solve(self) -> dict[str, float]:
        """Solve the system and return {variable: value}.

        For each column it picks a pivot row makes the pivot 1, and subtracts multiples of
        it from every other row. The number of pivots found is the rank.

        Raises:
            DimensionMismatchException: Fewer equations than variables.
            InconsistentSystemException: A row reduces to 0 = c with c != 0.
            InfiniteSolutionsException: Rank is smaller than the number of variables.
        """
        equations = len(self._matrix)
        num_var = len(self._variables)

        if equations < num_var:
            raise DimensionMismatchException(f"{equations} equations for {num_var} variables")

        augmented = []
        for row in self._matrix:
            augmented.append(row[:])  

        rank = 0
        for column in range(num_var):
            # find a new pivot
            found = None
            for r in range(rank, equations):
                if abs(augmented[r][column]) >= self.TOLERANCE:
                    found = r
                    break

            if found is None:
                continue  
            augmented[rank], augmented[found] = augmented[found], augmented[rank]

            # scale the pivot row so the pivot becomes 1
            pivot = augmented[rank][column]
            for c in range(column, num_var + 1):
                augmented[rank][c] = augmented[rank][c] / pivot

            # make the rest of column entries zero
            for r in range(equations):
                if r != rank:
                    factor = augmented[r][column]
                    for c in range(column, num_var + 1):
                        augmented[r][c] = augmented[r][c] - (factor * augmented[rank][c])
            rank += 1




        # rows below the rank have all-zero coefficients, so each one reads 0 = c
        for row in augmented[rank:]:
            if abs(row[num_var]) >= self.TOLERANCE:
                raise InconsistentSystemException("The system has no solution")

        if rank < num_var:
            raise InfiniteSolutionsException("Infinitely many solutions")

        # the left side is now the identity, so the last column holds the answers
        solution = {}
        for i in range(num_var):
            solution[self._variables[i]] = augmented[i][num_var]
        return solution
    
    
    
    
    def get_metadata(self) -> dict:
        """Return {"num_variables": n, "num_equations": m}."""
        return {
            "num_variables": len(self._variables),
            "num_equations": len(self._matrix),
        }