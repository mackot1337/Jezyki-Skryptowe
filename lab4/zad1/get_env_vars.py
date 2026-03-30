import os
import sys

from get_filtered_env_vars import get_filtered_env_vars

def get_env_vars(env_vars, args):
    # Zmienne powinny być wyświetlone w porządku alfabetycznym
    sorted_vars = sorted(env_vars.items())

    # Jeśli nie podano argumentów, zwracamy wszystkie zmienne
    if not args:
        return sorted_vars

    # Jeśli podano argumenty, filtrujemy zmienne środowiskowe na podstawie przekazanych argumentów
    return get_filtered_env_vars(sorted_vars, args)

def main():
    # Jeżeli uruchomiono z flagą --test, wykonaj testy
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        from test_zad1 import test_zad1
        test_zad1()
    else:
        # sys.argv[0] to nazwa skryptu, więc bierzemy parametry od indeksu 1
        arguments = sys.argv[1:]
        
        # Pobieramy słownik zmiennych środowiskowych z os.environ
        results = get_env_vars(os.environ, arguments)
        
        # Wyświetlamy wynik na wyjście standardowe
        for var_name, var_value in results:
            print(f"{var_name}={var_value}")

if __name__ == "__main__":
    main()