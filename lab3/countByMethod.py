def countByMethod(log):
    if type(log) != list:
        print("Error: log is not a list")
        return {}

    methods = {}

    for entry in log:
        if len(entry) > 6:
            method = entry[6]

            if type(method) == str:
                if method in methods:
                    methods[method] += 1
                else:
                    methods[method] = 1

    return methods

def test():
    testLogs = [
        ("ts", "uid1", "ip", 80, "ip", 80, "GET", "host", "/A", 200),
        ("ts", "uid2", "ip", 80, "ip", 80, "POST", "host", "/B", 404),
        ("ts", "uid3", "ip", 80, "ip", 80, "GET", "host", "/C", 200),
        ("ts", "uid4", "ip", 80, "ip", 80, "PUT", "host", "/D", 500),
        ("ts", "uid5", "ip", 80, "ip", 80, "GET", "host", "/E", 200)
    ]
    
    print("Testy funkcji countByMethod")
    
    print("Test 1")
    res1 = countByMethod(testLogs)
    print(res1)
    
    print("Test 2")
    res2 = countByMethod("To nie sa logi")
    print(res2)
    
    print("Test 3")
    res3 = countByMethod([])
    print(res3)

if __name__ == "__main__":
    test()