def countStatusClasses(log):
    if type(log) != list:
        print("Error: log is not a list")
        return {}

    classes = {
        "2xx": 0,
        "3xx": 0,
        "4xx": 0,
        "5xx": 0
    }

    for entry in log:
        if len(entry) > 9:
            statusCode = entry[9]

            if type(statusCode) == int:
                if 200 <= statusCode <= 299:
                    classes["2xx"] += 1
                elif 300 <= statusCode <= 399:
                    classes["3xx"] += 1
                elif 400 <= statusCode <= 499:
                    classes["4xx"] += 1
                elif 500 <= statusCode <= 599:
                    classes["5xx"] += 1
                

    return classes

def test():
    testLogs = [
        ("ts", "uid1", "ip", 80, "ip", 80, "GET", "host", "/A", 200), 
        ("ts", "uid2", "ip", 80, "ip", 80, "POST", "host", "/B", 201),
        ("ts", "uid3", "ip", 80, "ip", 80, "GET", "host", "/C", 302), 
        ("ts", "uid4", "ip", 80, "ip", 80, "GET", "host", "/D", 404), 
        ("ts", "uid5", "ip", 80, "ip", 80, "PUT", "host", "/E", 500), 
        ("ts", "uid6", "ip", 80, "ip", 80, "GET", "host", "/F", None) 
    ]
    
    print("Testy funkcji countStatusClasses")
    
    print("Test 1")
    res1 = countStatusClasses(testLogs)
    print(res1)
    
    print("Test 2")
    res2 = countStatusClasses("To nie sa logi")
    print(res2)
    
    print("Test 3")
    res3 = countStatusClasses([])
    print(res3)

if __name__ == "__main__":
    test()