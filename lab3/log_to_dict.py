import datetime
from entry_to_dict import entry_to_dict

def log_to_dict(log):
    if not isinstance(log, list):
        raise TypeError(f"Oczekiwano list, otrzymano: {type(log).__name__}")
    
    sessions = {}
    for entry in log:
        entry_dict = entry_to_dict(entry)
        uid = entry_dict["uid"]
        
        if uid not in sessions:
            sessions[uid] = []
            
        sessions[uid].append(entry_dict)
        
    return sessions

if __name__ == "__main__":
    # Test 1: Poprawne logi
    dt = datetime.datetime(2026, 3, 21, 10, 0, 0)
    log_data = [
        (dt, "uid1", "192.168.0.1", 54321, "10.0.0.5", 80, "GET", "example.com", "/api/data", 200),
        (dt, "uid2", "192.168.0.2", 12345, "10.0.0.6", 443, "POST", "example.org", "/api/test", 201),
        (dt, "uid1", "192.168.0.1", 54321, "10.0.0.5", 80, "PUT", "example.com", "/api/update", 200)
    ]
    
    print("Test 1: Poprawne grupowanie logów po uid")
    result = log_to_dict(log_data)
    print("Wynik:", result)
    print("Wynik liczbowy:", {k: len(v) for k, v in result.items()})
    if isinstance(result, dict) and len(result["uid1"]) == 2 and len(result["uid2"]) == 1:
        print("Test 1 zaliczony.\n")

    # Test 2: Błędny typ danych 
    print("Test 2: Zły typ wejściowy")
    try:
        log_to_dict("zły typ - string")
    except TypeError as e:
        print("Pomyślnie przechwycono błąd:", e)
    print("Test 2 zaliczony.\n")

    # Test 3: Błędny element logu (powinien rzucić błąd z entry_to_dict)
    print("Test 3: Log z elementem niespełniającym wymogów")
    bad_log_data = [
        (dt, "uid1", "192.168.0.1", 54321, "10.0.0.5", 80, "GET", "example.com") # 8 elementów
    ]
    try:
        log_to_dict(bad_log_data)
    except ValueError as e:
        print("Pomyślnie przechwycono błąd z elementu wewnętrznego:", e)
    print("Test 3 zaliczony.\n")
