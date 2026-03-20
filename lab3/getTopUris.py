def getTopUris(log, n=10):
    if type(log) != list:
        print("Error: log is not a list")
        return {}

    if type(n) != int or n < 0:
        print("Error: n is not a positive integer")
        return {}

    uris = {}

    for entry in log:
        if len(entry) > 8:
            uri = entry[8]

            if uri in uris:
                uris[uri] += 1
            else:
                uris[uri] = 1

    sortedUris = sorted(uris.items(), key=lambda x: x[1], reverse=True)

    return sortedUris[:n]

def test():
    testLogs = [
        ("ts", "uid1", "ip", 80, "ip", 80, "GET", "host", "/index.html", 200),
        ("ts", "uid2", "ip", 80, "ip", 80, "POST", "host", "/login", 404),
        ("ts", "uid3", "ip", 80, "ip", 80, "GET", "host", "/index.html", 200),
        ("ts", "uid4", "ip", 80, "ip", 80, "GET", "host", "/api/data", 200),
        ("ts", "uid5", "ip", 80, "ip", 80, "GET", "host", "/index.html", 200),
        ("ts", "uid6", "ip", 80, "ip", 80, "POST", "host", "/login", 200)
    ]
    
    print("Testy funkcji getTopUris")
    
    print("Test 1")
    res1 = getTopUris(testLogs, n=2)
    print(res1)
    
    print("Test 2")
    res2 = getTopUris(testLogs, n="pięć")
    print(res2)
    
    print("Test 3")
    res3 = getTopUris([], n=5)
    print(res3)

if __name__ == "__main__":
    test()