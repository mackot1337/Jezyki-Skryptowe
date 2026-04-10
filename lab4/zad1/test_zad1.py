from get_env_vars import get_env_vars

def test_zad1():
    mock_env = {
        "PATH": "/usr/bin",
        "USER": "admin",
        "HOME": "/home/admin",
        "OS_VERSION": "10",
        "TEMP": "/tmp"
    }

    # 1. Test braku argumentów (powinno zwrócić wszystko, posortowane alfabetycznie)
    res_empty = get_env_vars(mock_env, [])
    assert len(res_empty) == 5, "Błąd: Brak argumentów powinien zwrócić wszystkie zmienne."
    assert res_empty[0][0] == "HOME", "Błąd: Zmienne nie są posortowane alfabetycznie."
    print("Test 1 zakończony pomyślnie.")

    # 2. Test dopasowania nieczułego na wielkość liter (case-insensitive)
    res_case = get_env_vars(mock_env, ["path"])
    assert len(res_case) == 1, "Błąd: Oczekiwano dopasowania jednej zmiennej."
    assert res_case[0][0] == "PATH", "Błąd: Parametr 'path' nie dopasował zmiennej 'PATH'."
    print("Test 2 zakończony pomyślnie.")

    # 3. Test wielu argumentów i częściowego dopasowania
    res_multiple = get_env_vars(mock_env, ["user", "temp"])
    # "er" pasuje do "USER", "tem" pasuje do "TEMP"
    assert len(res_multiple) == 2, "Błąd: Oczekiwano dopasowania dwóch zmiennych."
    keys = [k for k, v in res_multiple]
    assert "USER" in keys and "TEMP" in keys, "Błąd: Niewłaściwe filtrowanie wielu argumentów."
    print("Test 3 zakończony pomyślnie.")

    print("Wszystkie testy zakończone pomyślnie!")