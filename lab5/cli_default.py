import argparse
import os
import random
import statistics

from cli_helper import setup_logging, get_file_path, extract_measurements, valid_date, valid_measurement
from getAddressesByCode import getAddressesByCode

logger = setup_logging()

def cmd_random_station(args):
    try:
        csv_path = get_file_path(args.quantity, args.freq)
    except argparse.ArgumentTypeError as e:
        logger.warning(f"Błąd argumentu: {e}")
        return
        
    data_per_station = extract_measurements(csv_path, args.start, args.end)
    
    valid_codes = [code for code, vals in data_per_station.items() if vals]
    
    if not valid_codes:
        logger.warning("Brak dostępnych pomiarów dla zadanych parametrów.")
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
        print(f"Województwo: {county}")
    else:
        logger.warning(f"Znaleziono stacje, ale nie ma jej w pliku stacje.csv (Kod: {random_code})")

def cmd_stats(args):
    try:
        csv_path = get_file_path(args.quantity, args.freq)
    except argparse.ArgumentTypeError as e:
        logger.warning(f"Błąd argumentu: {e}")
        return
        
    data_per_station = extract_measurements(csv_path, args.start, args.end)
    
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
    
    parser.add_argument('--quantity', '-q', required=True, type=valid_measurement, 
                        help="Mierzona wielkość (np. PM10, PM2.5, NO2)")
    parser.add_argument('--freq', '-f', required=True, type=str, choices=['1g', '24g', '1m'], 
                        help="Częstotliwość (1g, 24g, 1m)")
    parser.add_argument('--start', '-s', required=True, type=valid_date, 
                        help="Początek przedziału czasowego (rrrr-mm-dd)")
    parser.add_argument('--end', '-e', required=True, type=valid_date, 
                        help="Koniec przedziału czasowego (rrrr-mm-dd)")

    subparsers = parser.add_subparsers(title="podkomendy", dest="command", required=True)

    parser_random = subparsers.add_parser('random-station', 
                                          help="Wypisz nazwę i adres losowej stacji mierzącej tę wielkość w danym czasie")
    parser_random.set_defaults(func=cmd_random_station)

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

    try:
        get_file_path(args.quantity, args.freq)
    except argparse.ArgumentTypeError as e:
        logger.warning(f"Błąd argumentu: {e}")
        return

    args.func(args)

if __name__ == "__main__":
    main()