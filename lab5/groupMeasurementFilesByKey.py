import re
from pathlib import Path

def groupMeasurementFilesByKey(path):
    dict = Path(path)
    result = {}

    if not dict.exists() or not dict.is_dir():
        raise NotADirectoryError("Błąd: Przekazana ścieżka nie jest poprawnym katalogiem!")

    pattern = re.compile(r"^(\d{4})_([^_]+)_([^_.]+)\.csv$")

    for element in dict.iterdir():
        if element.is_file():
            match = pattern.match(element.name)
            
            if match:
                year = match.group(1)
                size = match.group(2)
                freq = match.group(3)

                key = (year, size, freq)
                
                result[key] = element

    return result