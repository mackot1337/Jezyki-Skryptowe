import os

from get_dirs_from_path import get_directories_from_path
from get_exec_in_dir import get_executables_in_dir, is_executable

def zad2_test():
    """
    Testy sprawdzające poprawność działania funkcji dla wartości skrajnych i błędnych.
    """
    # 1. Testowanie wartości skrajnych (pusty ciąg znaków)
    assert get_directories_from_path("") == [], "Błąd: Pusty ciąg PATH powinien zwrócić pustą listę."
    
    # 2. Testowanie poprawnego dzielenia ścieżek
    test_path = f"/usr/bin{os.pathsep}/usr/local/bin"
    dirs = get_directories_from_path(test_path)
    assert len(dirs) == 2, "Błąd: Niepoprawne dzielenie zmiennej PATH."
    assert dirs[0] == "/usr/bin", "Błąd: Zła wartość pierwszego katalogu."
    
    # 3. Testowanie wartości problematycznych (katalog nieistniejący)
    # Funkcja nie powinna rzucić wyjątkiem, tylko zwrócić pustą listę.
    fake_dir = "/sciezka/ktora/na/pewno/nie/istnieje_12345"
    assert get_executables_in_dir(fake_dir) == [], "Błąd: Nieistniejący katalog powinien zwrócić pustą listę."

    # 4. Testowanie czy funkcja is_executable poprawnie odrzuca katalogi
    current_dir = os.path.abspath(os.path.dirname(__file__))
    assert not is_executable(current_dir), "Błąd: Katalog nie powinien być rozpoznany jako plik wykonywalny."
    
    print("Wszystkie testy zakończone pomyślnie!")