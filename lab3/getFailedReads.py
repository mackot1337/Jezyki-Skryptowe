def getFailedReads(log, merge=False):
    if type(log) != list:
        if merge:
            print("Error: log is not a list")
            return []
        else:
            print("Error: log is not a list")
            return [], []
    
    m4xx = []
    m5xx = []

    for entry in log:
        if len(entry) > 9:
            statusCode = entry[9]

            if type(statusCode) == int:
                if statusCode >= 400 and statusCode < 500:
                    m4xx.append(entry)
                elif statusCode >= 500 and statusCode < 600:
                    m5xx.append(entry)

    if merge:
        merged = m4xx + m5xx
        return merged
    else:
        return m4xx, m5xx
    
def test():
    testLogs = [
        ("ts", "uid1", "ip", 80, "ip", 80, "GET", "host", "/A", 200),
        ("ts", "uid2", "ip", 80, "ip", 80, "GET", "host", "/B", 404),
        ("ts", "uid3", "ip", 80, "ip", 80, "GET", "host", "/C", 403),
        ("ts", "uid4", "ip", 80, "ip", 80, "GET", "host", "/D", 500),
        ("ts", "uid5", "ip", 80, "ip", 80, "GET", "host", "/E", None)
    ]
    
    print("Testy funkcji getFailedReads")
    
    print("Test 1")
    res1, res2 = getFailedReads(testLogs, merge=False)
    print(res1, res2)
    
    print("Test 2")
    res3 = getFailedReads(testLogs, merge=True)
    print(res3)
    
    print("Test 3")
    res4, res5 = getFailedReads([], merge=False)
    print(res4, res5)
    
    print("Test 4")
    res6 = getFailedReads("To nie jest lista", merge=True)
    print(res6)

if __name__ == "__main__":
    test()