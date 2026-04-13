import argparse
import os
import sys
import logging
from datetime import datetime

from parseCsvFile import parseCsvFile
from groupMeasurementFilesByKey import groupMeasurementFilesByKey

class StdOutFilter(logging.Filter):
    def filter(self, record):
        return record.levelno <= logging.WARNING

def setup_logging():
    logger = logging.getLogger('logger')
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(levelname)s: %(message)s')

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(formatter)
        stdout_handler.addFilter(StdOutFilter())

        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.ERROR)
        stderr_handler.setFormatter(formatter)

        logger.addHandler(stdout_handler)
        logger.addHandler(stderr_handler)

    return logger

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = f"Nieprawidłowy format daty: '{s}'. Oczekiwany format to rrrr-mm-dd."
        raise argparse.ArgumentTypeError(msg)

def valid_measurement(s):
    base_dir = os.path.join(os.path.dirname(__file__), 'measurements')
    try:
        files_dict = groupMeasurementFilesByKey(base_dir)
        valid_qs = set()
        for k in files_dict.keys():
            q = k[1]
            if q == 'PM25': q = 'PM2.5'
            valid_qs.add(q)
            
        if valid_qs and s not in valid_qs:
            msg = f"Użytkownik podał mierzoną wielkość '{s}', która nie występuje na żadnej stacji."
            raise argparse.ArgumentTypeError(msg)
        return s
    except (NotADirectoryError, FileNotFoundError):
        return s

def get_file_path(quantity, freq):
    q = quantity.replace('.', '')
    base_dir = os.path.join(os.path.dirname(__file__), 'measurements')
    
    try:
        files_dict = groupMeasurementFilesByKey(base_dir)
    except (NotADirectoryError, FileNotFoundError):
        files_dict = {}

    key = ('2023', q, freq)
    
    if key not in files_dict:
        available = [k[1] for k in files_dict.keys() if k[0] == '2023' and k[2] == freq]
        msg = f"Brak dostępnych pomiarów dla zadanych parametrów. Wielkość '{quantity}' lub częstotliwość '{freq}' jest nieprawidłowa."
        if available:
            msg += f" Dostępne wielkości z tą częstotliwością to: {', '.join(sorted(set(available)))}"
        raise argparse.ArgumentTypeError(msg)
        
    return str(files_dict[key])

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%m/%d/%y %H:%M")
    except ValueError:
        pass
    try:
        return datetime.strptime(date_str, "%d.%m.%Y %H:%M")
    except ValueError:
        pass
    return None

def extract_measurements(csv_path, start_date, end_date):
    data = parseCsvFile(csv_path)
    if not data or len(data) < 5:
        return {}
        
    station_row = data[0]
    cols = [k for k in station_row.keys() if k != 'Nr']
    station_codes = [station_row[c] for c in cols]
    
    data_per_station = {code: [] for code in station_codes if code}
    
    for row in data[5:]:
        date_str = row.get('Nr')
        if not date_str: continue
        
        row_date = parse_date(date_str)
        if row_date is None: continue
        
        row_day_start = row_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        if start_date <= row_day_start <= end_date:
            for i, c in enumerate(cols):
                code = station_codes[i] if i < len(station_codes) else None
                val = row.get(c, '').strip()
                if code and val:
                    try:
                        v = float(val.replace(',', '.'))
                        data_per_station[code].append(v)
                    except ValueError:
                        pass
                        
    return data_per_station
