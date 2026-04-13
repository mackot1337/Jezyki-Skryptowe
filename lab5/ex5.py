import argparse
import csv
import os
import random
import statistics
import sys
import logging
from datetime import datetime

class StdOutFilter(logging.Filter):
    def filter(self, record):
        return record.levelno <= logging.WARNING

def setup_logging():
    logger = logging.getLogger('zad5')
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

logger = setup_logging()

from parseCsvFile import parseCsvFile
from groupMeasurementFilesByKey import groupMeasurementFilesByKey
from getAddressesByCode import getAddressesByCode

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
        return [], {}
        
    # data[0] contains stacja codes
    station_row = data[0]
    cols = [k for k in station_row.keys() if k != 'Nr']
    station_codes = [station_row[c] for c in cols]
    
    data_per_station = {code: [] for code in station_codes if code}
    
    # Rows starting from data[5] are measurement data rows
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
                        
    return station_codes, data_per_station

def cmd_random_station(args):
    try:
        csv_path = get_file_path(args.quantity, args.freq)
    except argparse.ArgumentTypeError as e:
        logger.warning(f"Błąd argumentu: {e}")
        return
        
    station_codes, data_per_station = extract_measurements(csv_path, args.start, args.end)
    
    valid_codes = [code for code, vals in data_per_station.items() if vals]
    
    if not valid_codes:
        logger.warning("Brak dostępnych pomiarów dla zadanych parametrów (filtr zwrócił pustą listę).")
        return
        
    random_code = random.choice(valid_codes)
    
    stacje_path = os.path.join(os.path.dirname(__file__), 'stacje.csv')
    addr_list = getAddressesByCode(stacje_path, random_code)
    
    if addr_list:
        county, city, street, number, name = addr_list[0]
        adres = f"{street} {number}".strip() if street else 'Brak adresu'
        print(f"Losowa stacja: {name}")
        print(f"Adres: {city}, {adres}")
        print(f"Kod stacji: {random_code}")
    else:
        logger.warning(f"Znaleziono stacje, ale nie ma jej w pliku stacje.csv (Kod: {random_code})")

def cmd_stats(args):
    try:
        csv_path = get_file_path(args.quantity, args.freq)
    except argparse.ArgumentTypeError as e:
        logger.warning(f"Błąd argumentu: {e}")
        return
        
    station_codes, data_per_station = extract_measurements(csv_path, args.start, args.end)
    
    if args.station not in data_per_station:
        logger.warning(f"Częstotliwość lub wielkość nie jest wspierana przez daną stację. (Stacja '{args.station}' nie mierzy tej wielkości).")
        return
        
    vals = data_per_station[args.station]
    if not vals:
        logger.warning(f"Brak poprawnych pomiarów dla zadanych parametrów (stacja '{args.station}' w podanym przedziale czasowym).")
        return
        
    mean = statistics.mean(vals)
    stdev = statistics.stdev(vals) if len(vals) > 1 else 0.0
    
    print(f"Stacja: {args.station}")
    print(f"Wielkość: {args.quantity}")
    print(f"Czas: {args.start.strftime('%Y-%m-%d')} do {args.end.strftime('%Y-%m-%d')}")
    print(f"Liczba pomiarów: {len(vals)}")
    print(f"Średnia: {mean:.2f}")
    if len(vals) > 1:
        print(f"Odchylenie standardowe: {stdev:.2f}")
    else:
        print("Odchylenie standardowe: Brak (wymagane min. 2 pomiary)")

def create_parser():
    parser = argparse.ArgumentParser(description="CLI do obróbki danych o jakości powietrza z 2023 r.")
    
    # Global arguments (we will parse them as main parser arguments)
    parser.add_argument('--quantity', '-q', required=True, type=valid_measurement, 
                        help="Mierzona wielkość (np. PM10, PM2.5, NO2)")
    parser.add_argument('--freq', '-f', required=True, type=str, choices=['1g', '24g', '1m'], 
                        help="Częstotliwość (1g, 24g, 1m)")
    parser.add_argument('--start', '-s', required=True, type=valid_date, 
                        help="Początek przedziału czasowego (rrrr-mm-dd)")
    parser.add_argument('--end', '-e', required=True, type=valid_date, 
                        help="Koniec przedziału czasowego (rrrr-mm-dd)")

    subparsers = parser.add_subparsers(title="podkomendy", dest="command", required=True)

    # Subcommand: random-station
    parser_random = subparsers.add_parser('random-station', 
                                          help="Wypisz nazwę i adres losowej stacji mierzącej tę wielkość w danym czasie")
    parser_random.set_defaults(func=cmd_random_station)

    # Subcommand: stats
    parser_stats = subparsers.add_parser('stats', 
                                         help="Oblicz średnią i odchylenie standardowe dla danej stacji")
    parser_stats.add_argument('station', type=str, help="Kod stacji (np. DsGlogWiStwo)")
    parser_stats.set_defaults(func=cmd_stats)

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    if args.start > args.end:
        logger.error("Błąd krytyczny: Data początkowa nie może być późniejsza niż data końcowa.")
        return

    # Try mapping/checking before running
    try:
        get_file_path(args.quantity, args.freq)
    except argparse.ArgumentTypeError as e:
        logger.warning(f"Błąd argumentu: {e}")
        return

    args.func(args)

if __name__ == "__main__":
    main()