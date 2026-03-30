import os
import sys

from get_dirs_from_path import get_directories_from_path
from test_zad2 import zad2_test
from get_exec_in_dir import get_executables_in_dir

def main():
    # Pobieramy argumenty z pominięciem nazwy skryptu
    args = sys.argv[1:]
    
    if "--test" in args:
        zad2_test()
        return

    # Pobieramy zawartość zmiennej środowiskowej PATH
    path_env = os.environ.get("PATH", "")
    directories = get_directories_from_path(path_env)

    if "--dirs" in args:
        # a. Wypisanie katalogów z PATH, każdy w osobnej linii
        print("Katalogi w zmiennej PATH:")
        for d in directories:
            print(d)
            
    elif "--execs" in args:
        # b. Wypisanie katalogów wraz z listą plików wykonywalnych
        for d in directories:
            print(f"\nKatalog: {d}")
            execs = get_executables_in_dir(d)
            if execs:
                for exe in execs:
                    print(f"  - {exe}")
            else:
                print("  (Brak plików wykonywalnych lub brak dostępu)")
    else:
        print("Użycie:")
        print("  python path_explorer.py --dirs   -> Wypisuje tylko katalogi z PATH")
        print("  python path_explorer.py --execs  -> Wypisuje katalogi i pliki wykonywalne")
        print("  python path_explorer.py --test   -> Uruchamia testy jednostkowe")

if __name__ == "__main__":
    main()