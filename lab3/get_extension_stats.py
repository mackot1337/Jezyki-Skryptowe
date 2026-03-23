import os
from urllib.parse import urlparse
from collections import Counter
from entry_to_dict import entry_to_dict

def get_extension_stats(log):
    if not isinstance(log, list):
        raise TypeError(f"Oczekiwano listy, otrzymano: {type(log).__name__}")
        
    ext_counter = Counter()
    
    for entry in log:
        entry_dict = entry_to_dict(entry)
        uri = entry_dict.get("uri", "")
        
        # Parsowanie URI w celu usunięcia ewentualnych parametrów zapytania (np. ?id=1)
        parsed_uri = urlparse(uri)
        path = parsed_uri.path
        
        # Ekstrakcja rozszerzenia z wyodrębnionej ścieżki
        _, ext = os.path.splitext(path)
        
        if ext.startswith('.'):
            # Usunięcie początkowej kropki i sprowadzenie do małych liter
            ext = ext[1:].lower()
            
        if ext:
            ext_counter[ext] += 1
            
    return dict(ext_counter)

def test():
    testLogs = [
        ("ts", "uid1", "ip", 80, "ip", 80, "GET", "host", "http://nmap.org/book/nse.html", 200),
        ("ts", "uid2", "ip", 80, "ip", 80, "GET", "host", "/script.js", 200),
        ("ts", "uid3", "ip", 80, "ip", 80, "GET", "host", "/style.CSS", 200),
        ("ts", "uid4", "ip", 80, "ip", 80, "GET", "host", "/image.png", 200),
        ("ts", "uid5", "ip", 80, "ip", 80, "GET", "host", "/index.html", 200)
    ]
    
    print("Testy funkcji get_extension_stats")
    
    print("Test 1: poprawne dane")
    res1 = get_extension_stats(testLogs)
    print(res1)
    
    print("Test 2: zły typ danych")
    try:
        res2 = get_extension_stats("To nie jest lista logow")
        print(res2)
    except TypeError as e:
        print(e)
        
    print("Test 3: pusta lista")
    res3 = get_extension_stats([])
    print(res3)

if __name__ == "__main__":
    test()
