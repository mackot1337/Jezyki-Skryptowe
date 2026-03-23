from entry_to_dict import entry_to_dict

def get_session_paths(log):
    if not isinstance(log, list):
        raise TypeError(f"Oczekiwano listy, otrzymano: {type(log).__name__}")
        
    session_paths = {}
    for entry in log:
        entry_dict = entry_to_dict(entry)
        uid = entry_dict["uid"]
        uri = entry_dict["uri"]
        
        if uid not in session_paths:
            session_paths[uid] = []
            
        session_paths[uid].append(uri)
        
    return session_paths

def test():
    testLogs = [
        ("ts", "uid1", "ip", 80, "ip", 80, "GET", "host", "/uriA", 200),
        ("ts", "uid1", "ip", 80, "ip", 80, "POST", "host", "/uriB", 404),
        ("ts", "uid2", "ip", 80, "ip", 80, "GET", "host", "/uriC", 200),
        ("ts", "uid3", "ip", 80, "ip", 80, "PUT", "host", "/uriD", 500),
        ("ts", "uid2", "ip", 80, "ip", 80, "GET", "host", "/uriE", 200)
    ]
    
    print("Testy funkcji get_session_paths")
    
    print("Test 1: poprawne dane")
    res1 = get_session_paths(testLogs)
    print(res1)
    
    print("Test 2: zły typ danych")
    try:
        res2 = get_session_paths("To nie jest lista logow")
        print(res2)
    except TypeError as e:
        print(e)
        
    print("Test 3: pusta lista")
    res3 = get_session_paths([])
    print(res3)

if __name__ == "__main__":
    test()
