from collections import Counter

def print_dict_entry_dates(log_dict):
    if not isinstance(log_dict, dict):
        raise TypeError(f"Oczekiwano słownika, otrzymano: {type(log_dict).__name__}")
    
    for uid, entries in log_dict.items():
        if not entries:
            continue
            
        print(f"--- Sesja UID: {uid} ---")
        
        ips = set(entry.get("ip") for entry in entries if entry.get("ip"))
        hosts = set(entry.get("host") for entry in entries if entry.get("host"))
        print(f"Adresy IP: {', '.join(ips) if ips else 'brak'}")
        print(f"Hosty: {', '.join(hosts) if hosts else 'brak'}")
        
        num_requests = len(entries)
        print(f"Liczba żądań: {num_requests}")
        
        timestamps = [entry.get("ts") for entry in entries if entry.get("ts")]
        if timestamps:
            first_date = min(timestamps)
            last_date = max(timestamps)
            print(f"Pierwsze żądanie: {first_date}")
            print(f"Ostatnie żądanie: {last_date}")
        else:
            print("Daty żądań: brak")
            
        methods = [entry.get("method") for entry in entries if entry.get("method")]
        if methods:
            method_counts = Counter(methods)
            print("Procentowy udział metod HTTP:")
            for method, count in method_counts.items():
                percentage = (count / len(methods)) * 100
                print(f"  {method}: {percentage:.2f}%")
        else:
            print("Procentowy udział metod HTTP: brak")
            
        status_codes = [entry.get("statusCode") for entry in entries if entry.get("statusCode") is not None]
        if status_codes:
            success_codes = sum(1 for code in status_codes if 200 <= code < 300)
            ratio_str = f"{success_codes}/{len(status_codes)}"
            ratio_pct = (success_codes / len(status_codes)) * 100
            print(f"Stosunek kodów 2xx do wszystkich: {ratio_str} ({ratio_pct:.2f}%)")
        else:
            print("Stosunek kodów 2xx do wszystkich: brak")
            
        print()

def test():
    print("Test 1: Prawidłowe dane (dobry przypadek)")
    log_dict = {
        "uid1": [
            {"ip": "192.168.1.1", "host": "example.com", "method": "GET", "statusCode": 200, "ts": "2023-01-01 10:00:00"},
            {"ip": "192.168.1.1", "host": "example.com", "method": "GET", "statusCode": 200, "ts": "2023-01-01 10:05:00"},
        ]
    }
    print_dict_entry_dates(log_dict)
    
    print("\nTest 2: Brak wejść (krawędziowy przypadek)")
    print_dict_entry_dates({})
    
    print("\nTest 3: Niepoprawny typ na wejściu (błąd)")
    try:
        print_dict_entry_dates("nie słownik")
    except TypeError as e:
        print(f"Oczekiwany błąd przechwycony: {e}")

if __name__ == "__main__":
    test()

