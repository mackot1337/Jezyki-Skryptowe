def getEntriesByCode(log, code):
    
    if type(log) != list:
        return []
    
    try:
        targetCode = int(code)
    except ValueError:
        print("Error: cannot convert code to int")
        return []
    except TypeError:
        print("Error: cannot convert code to int")
        return []

    entries = []

    for entry in log:
        if len(entry) > 9 and entry[9] == targetCode:
            entries.append(entry)

    return entries

def test():
    testLogs = [
        ("ts", "uid1", "ip", 80, "ip", 80, "GET", "host", "/A", 200),
        ("ts", "uid2", "ip", 80, "ip", 80, "POST", "host", "/B", 404),
        ("ts", "uid3", "ip", 80, "ip", 80, "GET", "host", "/C", 200),
        ("ts", "uid4", "ip", 80, "ip", 80, "PUT", "host", "/D", 500)
    ]
    
    print("Testy funkcji getEntriesByCode")
    
    print("Test 1")
    res1 = getEntriesByCode(testLogs, 200)
    print(res1)
    
    print("Test 2")
    res2 = getEntriesByCode(testLogs, "dwieście")
    print(res2)
    
    print("Test 3")
    res3 = getEntriesByCode([], 404)
    print(res3)
    
    print("Test 4")
    res4 = getEntriesByCode(testLogs, 418)
    print(res4)

if __name__ == "__main__":
    test()