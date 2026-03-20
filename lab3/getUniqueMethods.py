def getUniqueMethods1(log):
    if type(log) != list:
        print("Error: log is not a list")
        return []
    
    methods = {}

    for entry in log:
        if len(entry) > 6:
            method = entry[6]

            if type(method) == str:
                if method in methods:
                    methods[method] += 1
                else:
                    methods[method] = 1
    
    result = []

    for method in methods:
        if methods[method] == 1:
            result.append(method)

    return result

def getUniqueMethods2(log):
    if type(log) != list:
        print("Error: log is not a list")
        return []

    methods = set()

    for entry in log:
        if len(entry) > 6:
            method = entry[6]

            if type(method) == str:
                methods.add(method)

    return list(methods)

def test():
    testLogs = [
        ("ts", "uid1", "ip", 80, "ip", 80, "GET", "host", "/A", 200),
        ("ts", "uid2", "ip", 80, "ip", 80, "POST", "host", "/B", 404),
        ("ts", "uid3", "ip", 80, "ip", 80, "GET", "host", "/C", 200),
        ("ts", "uid4", "ip", 80, "ip", 80, "PUT", "host", "/D", 500),
        ("ts", "uid5", "ip", 80, "ip", 80, "GET", "host", "/E", 200)
    ]
    
    print("Testy funkcji getUniqueMethods1")
    
    print("Test 1")
    res1 = getUniqueMethods1(testLogs)
    print(res1)
    
    print("Test 2")
    res2 = getUniqueMethods1("To nie jest lista logow")
    print(res2)
    
    print("Test 3")
    res3 = getUniqueMethods1([])
    print(res3)
    
    print("Testy funkcji getUniqueMethods2")

    print("Test 1")
    res4 = getUniqueMethods2(testLogs)
    print(res4)

    print("Test 2")
    res5 = getUniqueMethods2("To nie jest lista logow")
    print(res5)

    print("Test 3")
    res6 = getUniqueMethods2([])
    print(res6)

if __name__ == "__main__":
    test()