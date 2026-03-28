def getEntriesByAddr(log, addr):
    
    if type(addr) != str:
        print("Error: addr is not a string")
        return []
    
    isIp = True

    for char in addr:
        if not char.isdigit() and char != ".":
            isIp = False
            break

    if isIp:
        partions = addr.split(".")

        if len(partions) != 4:
            print("Error: addr is not a valid IP address")
            return []
        
        for partion in partions:
            if not partion.isdigit() or int(partion) < 0 or int(partion) > 255:
                print("Error: addr is not a valid IP address")
                return []
            
    result = []

    for entry in log:
        if len(entry) > 7:
            ip = entry[2]
            hostAddr = entry[7]

            if hostAddr == addr or ip == addr:
                result.append(entry)

    return result

def test():
    testLogs = [
        ("ts", "uid1", "192.168.1.10", 80, "10.0.0.1", 80, "GET", "example.com", "/A", 200),
        ("ts", "uid2", "192.168.1.11", 80, "10.0.0.1", 80, "POST", "test.org", "/B", 404),
        ("ts", "uid3", "10.0.0.5", 80, "10.0.0.1", 80, "GET", "example.com", "/C", 200)
    ]
    
    print("Testy funkcji getEntriesByAddr")
    
    print("Test 1")
    res1 = getEntriesByAddr(testLogs, "192.168.1.10")
    print(res1)
    
    print("Test 2")
    res2 = getEntriesByAddr(testLogs, "example.com")
    print(res2)
    
    print("Test 3")
    res3 = getEntriesByAddr(testLogs, "999.1.1.1")
    print(res3)
    
    print("Test 4")
    res4 = getEntriesByAddr(testLogs, 192168110)
    print(res4)
    
    print("Test 5")
    res5 = getEntriesByAddr([], "192.168.1.10")
    print(res5)

if __name__ == "__main__":
    test()