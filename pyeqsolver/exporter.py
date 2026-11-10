"""Writing solutions and errors to a JSON file."""

import json
from pathlib import Path


class JSONExporter:
    """Write the outcome of a run to one JSON file.

    Args:
        output_path: Where to write. Missing folders are created.
    """

    PRECISION = 4

    def __init__(self, output_path: str | Path) -> None:
        self.output_path = Path(output_path)

    def save(self, solutions: dict[str, float], metadata: dict) -> None:
        """Write a SUCCESS file; values are rounded and -0.0 becomes 0.0."""

        cleaned = {}
        for name, value in solutions.items():

            rounded = round(value, self.PRECISION)
            # turns -0.0 into 0.0
            if rounded == 0:
                rounded = 0.0  

            cleaned[name] = rounded

        self._write({
            "status": "SUCCESS",
            "system_info": metadata,
            "solution": cleaned,
        })

    def save_error(self, exc: BaseException) -> None:
        """Write an ERROR file; error_type is the exception's class name."""

        self._write({
            "status": "ERROR",
            "error_type": type(exc).__name__,
            "message": str(exc),
        })

    def _write(self, data: dict) -> None:
        """Create the output folder if needed and dump data as indented JSON."""

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with self.output_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
