import re
from pathlib import Path

from .exceptions import InvalidFileFormatException


_VAR = "[A-Za-z_][A-Za-z0-9_]*"
_NUM = "\d+\.?\d*"
_TOKEN = rf"{_NUM}|{_VAR}|[+\-*]"
class EquationParser:
    """Parse a text file of linear equations into (matrix, variables).

    Expected Input:
        A file containing one equation per line, Blank lines and comments are skipped. 
        Variables follow Python's naming conventions and are ordered by first appearance in the file.

    Args:
        file_path: Path of the input file.
        
    """

    def __init__(self, file_path: str | Path) -> None:
        
        self.file_path = Path(file_path)
        

    
    
    def parse(self) -> tuple[list[list[float]], list[str]]:
        """
        Read the file and build the augmented matrix.

        Returns:
            A tuple (matrix, variables) where the matrix stores the coefficients and variables store equation variables

        Raises:
            FileNotFoundError: If the input file does not exist.
            InvalidFileFormatException: If a line breaks the syntax rules or the file contains no equations.
        """
        
        try:
            lines = self.file_path.read_text(encoding="utf-8").splitlines()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Input file not found: {self.file_path}") from e 

        variables = []
        equations = []

        for line_number, line in enumerate(lines, start=1):
            text = line.strip()

            if not text or text.startswith("#"):
                continue

            coefficients, constant = self._parse_equation(line_number ,text)

            for name in coefficients:

                if name not in variables:
                    variables.append(name)

            equations.append((coefficients, constant))

        if not equations:
            raise InvalidFileFormatException(f"No equations found in {self.file_path}")


        matrix=[]

        for coefficients, constant in equations:
            row = []
            for name in variables:
                row.append(coefficients.get(name, 0.0))

            row.append(constant)
            matrix.append(row)
        return matrix, variables

    
    
    
    def _parse_equation(self, line_number, text: str) -> tuple[dict[str, float], float]:

        """Validate text and turn it into coefficients and a constant."""

        if "(" in text:
            raise InvalidFileFormatException(f"Line {line_number}:  Brackets")

        if text.count("=") != 1:
            if "=" not in text:
                raise InvalidFileFormatException(f" Line {line_number}: missing = sign")
            raise InvalidFileFormatException(f"Line {line_number}: more than one = sign")

        left, right = text.split("=")

        if not left.strip():
            raise InvalidFileFormatException(f"Line {line_number}: empty left side of = sign")
        
        if not right.strip():
            raise InvalidFileFormatException(f"Line {line_number}: empty right side of = sign")

        left_terms = self._parse_side(left)
        
        coefficients = {}
        for value, variable in left_terms:

            if variable is None:
                raise InvalidFileFormatException("number with no variable on the left side")
            
            coefficients[variable] = coefficients.get(variable, 0.0) + value

        try:
            res = float(right)
        except:
            raise InvalidFileFormatException(f"Line {line_number}: the right side must be a single number")
        
        return coefficients, float(right.replace(" ", ""))
       
        
        




    
    def _parse_side(self, side: str) -> list[tuple[float, str]]:
        """Split the left side of '=' into (signed coefficient, variable) terms."""
        terms_out = []
        sign = 1
        terms_in = re.findall(_TOKEN, side)
        number = None

        for i in range(len(terms_in)):
            if i >= 1:

                previous = terms_in[i-1]  
            else:
                previous = None    

            if terms_in[i] in ("+", "-"):

                if previous in ("+", "-"):
                    raise InvalidFileFormatException("repeating operators")
                
                if number is not None:
                    raise InvalidFileFormatException("number with no variable on the left side")
                
                if terms_in[i] == "-":
                    sign = -1
                else:
                    sign = 1

            elif re.fullmatch(_NUM, terms_in[i]):
                if previous not in (None, "+", "-"):
                    raise InvalidFileFormatException(f"expected operator before {terms_in[i]}")
                number = float(terms_in[i]) * sign
            
            elif re.fullmatch(_VAR, terms_in[i]):
                if previous not in (None, "+", "-") and not re.fullmatch(_NUM, previous):
                    raise InvalidFileFormatException(f"expected operator before {terms_in[i]}")

                if number is None:
                    number = 1 * sign

                terms_out.append((number, terms_in[i]))
                number = None
            
        
        
            
        if number is not None:
            raise InvalidFileFormatException("number with no variable on the left side")  

        return terms_out      


            

            

            

                
                
            
           



