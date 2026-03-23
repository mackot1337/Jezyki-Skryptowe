def get_largest_session(log_dict):
    if not isinstance(log_dict, dict):
        raise TypeError(f"Oczekiwano słownika, otrzymano: {type(log_dict).__name__}")
        
    if not log_dict:
        return None
        
    return max(log_dict.keys(), key=lambda uid: len(log_dict[uid]))

def test():
    testDict = {
        "uid1": [1, 2, 3],
        "uid2": [1],
        "uid3": [1, 2, 3, 4, 5]
    }
    
    print("Testy funkcji get_largest_session")
    
    print("Test 1: poprawne dane")
    res1 = get_largest_session(testDict)
    print(res1)
    
    print("Test 2: zły typ danych")
    try:
        res2 = get_largest_session("To nie jest slownik")
        print(res2)
    except TypeError as e:
        print(e)
        
    print("Test 3: pusty słownik")
    res3 = get_largest_session({})
    print(res3)

if __name__ == "__main__":
    test()
