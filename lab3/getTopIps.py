def getTopIps(log, n=10):
    if type(log) != list:
        print("Error: log is not a list")
        return []
    
    if type(n) != int or n < 0:
        print("Error: n is not a positive integer")
        return []

    ips = {}

    for entry in log:
        if len(entry) > 2:
            ip = entry[2]

            if ip in ips:
                ips[ip] += 1
            else:
                ips[ip] = 1

    sortedIps = sorted(ips.items(), key=lambda x: x[1], reverse=True)

    return sortedIps[:n]

def test():
    testLogs = [
        ("ts", "uid1", "192.168.1.10", 80),
        ("ts", "uid2", "192.168.1.11", 80),
        ("ts", "uid3", "192.168.1.10", 80),
        ("ts", "uid4", "10.0.0.5", 80),
        ("ts", "uid5", "192.168.1.11", 80),
        ("ts", "uid6", "192.168.1.10", 80)
    ]
    
    print("Testy funkcji getTopIps")
    
    print("Test 1")
    res1 = getTopIps(testLogs, n=2)
    print(res1)
    
    print("Test 2")
    res2 = getTopIps(testLogs, n="pięć")
    print(res2)
    
    print("Test 3")
    res3 = getTopIps([], n=5)
    print(res3)

if __name__ == "__main__":
    test()