import sys
import time
import os

from test_zad3 import test_zad3
from tail_util import tail_logic

def main():
    args = sys.argv[1:]
    
    # Domyślne wartości
    n_lines = 10  # brak parametru oznacza 10 ostatnich linii
    follow = False
    filepath = None

    # Parsowanie argumentów
    for arg in args:
        # Dla --test uruchamiamy testy i kończymy program
        if arg == "--test":
            test_zad3()
            sys.exit(0)
        elif arg.startswith("--lines="):
            parts = arg.split("=")
            # Upewniamy się, że są dokładnie dwie części: '--lines' oraz wartość
            if len(parts) != 2:
                print("Błąd: Nieprawidłowy format parametru --lines", file=sys.stderr)
                sys.exit(1)
            # Próba konwersji wartości na liczbę całkowitą
            try:
                n_lines = int(parts[1])
            # Obsługa sytuacji, gdy wartość nie jest liczbą całkowitą
            except ValueError:
                print("Błąd: Wartość dla --lines musi być liczbą całkowitą", file=sys.stderr)
                sys.exit(1)
        elif arg == "--follow":
            follow = True  # Aktywacja trybu follow tylko dla "python tail.py plik.txt --follow" bo cat plik.txt | python tail.py --follow nie ma sensu 
            #bo konczy od razu po przeczytaniu danych z wejścia standardowego
        else:
            filepath = arg  # Ostatni nierozpoznany argument traktujemy jako ścieżkę do pliku

    # Zgodnie z poleceniem: podanie argumentu pliku ignoruje wejście standardowe
    if filepath:
        if not os.path.isfile(filepath):
            print(f"Błąd: Plik '{filepath}' nie istnieje.", file=sys.stderr)
            sys.exit(1)
            
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in tail_logic(lines, n_lines):
                print(line, end="")
            
            # Wersja rozszerzona na 10 pkt: nasłuchiwanie na nowe linie 
            if follow:
                while True:
                    line = f.readline()
                    if not line:
                        time.sleep(0.1)  # Krótka pauza, by nie przeciążać procesora, mozna pominac
                        continue
                    print(line, end="")
    else:
        if sys.stdin.isatty():
            print("Błąd: Brak pliku oraz danych na wejściu standardowym.")
            print("Użycie: python tail.py [--lines=N] [--follow] [ścieżka_do_pliku]")
            sys.exit(1)
            
        lines = sys.stdin.readlines()
        for line in tail_logic(lines, n_lines):
            print(line, end="")

if __name__ == "__main__":
    main()