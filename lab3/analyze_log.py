from collections import Counter
from entry_to_dict import entry_to_dict
from get_extension_stats import get_extension_stats
from log_to_dict import log_to_dict
from get_largest_session import get_largest_session

def analyze_log(log):
    if not isinstance(log, list):
        raise TypeError(f"Oczekiwano listy, otrzymano: {type(log).__name__}")
        
    ip_counter = Counter()
    uri_counter = Counter()
    method_counter = Counter()
    error_count = 0
    
    for entry in log:
        entry_dict = entry_to_dict(entry)
        
        # Zbieranie IP, URI, Metod
        if entry_dict.get("ip"):
            ip_counter[entry_dict["ip"]] += 1
            
        if entry_dict.get("uri"):
            uri_counter[entry_dict["uri"]] += 1
            
        if entry_dict.get("method"):
            method_counter[entry_dict["method"]] += 1
            
        # Zliczanie błędów (kody HTTP >= 400 uważamy za błędy)
        status = entry_dict.get("statusCode")
        if status is not None and status >= 400:
            error_count += 1
            
    # Wyciąganie najczęstszych
    most_frequent_ip = ip_counter.most_common(1)[0][0] if ip_counter else None
    most_frequent_uri = uri_counter.most_common(1)[0][0] if uri_counter else None
    
    # 2 dodatkowe statystyki z poprzednich zadań
    # 1. Statystyki rozszerzeń plików
    ext_stats = get_extension_stats(log)
    
    # 2. Sesja (UID) z największą liczbą zapytań
    session_dict = log_to_dict(log)
    largest_session = get_largest_session(session_dict)
    
    return {
        "most_frequent_ip": most_frequent_ip,
        "most_frequent_uri": most_frequent_uri,
        "methods_distribution": dict(method_counter),
        "error_count": error_count,
        "extension_stats": ext_stats,         # Dodatkowa statystyka 1
        "largest_session_uid": largest_session # Dodatkowa statystyka 2
    }

def test():
    import os
    try:
        from readLog import readLog
    except ImportError:
        readLog = None

    print("Test 1: Normalny przypadek (dane z files/http_first_100k.log)")
    log_path = os.path.join(os.path.dirname(__file__), "files", "http_first_100k.log")
    
    if readLog and os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            # Weźmy małą próbkę dla testu, np. 100 pierwszych linijek
            lines = [f.readline() for _ in range(100)]
            logs = readLog(lines)
            result = analyze_log(logs)
            print("Wyniki analizy logów (podsumowanie):")
            for k, v in result.items():
                if k == "methods_distribution":
                    print(f"  {k}: {v}")
                elif k == "extension_stats":
                    print(f"  {k}: {v}")
                else:
                    print(f"  {k}: {v}")
    else:
        print(f"Brak pliku {log_path} lub modułu readLog. Upewnij się, że plik istnieje.")
    
    print("\nTest 2: Pusta lista/brak danych (krawędziowy)")
    print(analyze_log([]))
    
    print("\nTest 3: Niepoprawny typ wejściowy (błąd)")
    try:
         print(analyze_log("To nie są logi"))
    except TypeError as e:
         print(f"Przechwycono oczekiwany błąd: {e}")

if __name__ == "__main__":
    test()

