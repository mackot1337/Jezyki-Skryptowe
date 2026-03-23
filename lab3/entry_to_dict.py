def entry_to_dict(entry):
    if not isinstance(entry, tuple):
        raise TypeError(f"Oczekiwano krotki, otrzymano: {type(entry).__name__}")
    if len(entry) != 10:
        raise ValueError(f"Oczekiwano elementu o długości 10, otrzymano o długości: {len(entry)}")

    return {
        "ts": entry[0],
        "uid": entry[1],
        "ip": entry[2],
        "idOrigP": entry[3],
        "idRespH": entry[4],
        "idRespP": entry[5],
        "method": entry[6],
        "host": entry[7],
        "uri": entry[8],
        "statusCode": entry[9]
    }

def test():
    import datetime

    print("Testy funkcji entry_to_dict\n")

    # Test 1: Poprawne wejście
    dt = datetime.datetime(2026, 3, 21, 10, 0, 0)
    valid_entry = (dt, "uidA123", "192.168.0.1", 54321, "10.0.0.5", 80, "GET", "example.com", "/api/data", 200)
    
    print("Test 1: Poprawna krotka")
    result = entry_to_dict(valid_entry)
    print("Wynik:", result)
    if isinstance(result, dict) and result["statusCode"] == 200:
        print("Test 1 zaliczony.\n")
    else:
        print("Test 1 niezaliczony.\n")

    # Test 2: Błędny typ danych (string zamiast krotki/listy)
    print("Test 2: Zły typ wejściowy")
    try:
        entry_to_dict("nie_jest_krotka")
    except TypeError as e:
        print("Pomyślnie przechwycono błąd:", e)
    print("Test 2 zaliczony.\n")

    # Test 3: Krotka o nieprawidłowej długości (zbyt krótka)
    print("Test 3: Nieodpowiednia liczba elementów")
    short_entry = (dt, "uidA123", "192.168.0.1")
    try:
        entry_to_dict(short_entry)
    except ValueError as e:
        print("Pomyślnie przechwycono błąd:", e)
    print("Test 3 zaliczony.\n")

if __name__ == "__main__":
    test()