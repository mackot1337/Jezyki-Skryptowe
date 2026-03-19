def sortLog(log, index):
    try:
        return sorted(log, key=lambda x: x[index])
    except IndexError:
        print(f"Error: index {index} out of range")
        return []
    except TypeError:
        print("Error: log is not a list")
        return []
    


def test():
    testLogs = [
        (3, "GET", "/login"),
        (1, "POST", "/api"),
        (2, "PUT", "/index.html")
    ]
    
    print("Testy funkcji sortLog")
    
    print("Test 1")
    res1 = sortLog(testLogs, 0)
    print(res1)
    
    print("Test 2")
    res2 = sortLog(testLogs, 2)
    print(res2)
    
    print("Test 3")
    res3 = sortLog(testLogs, 99)
    print(res3)
    
    print("Test 4")
    res4 = sortLog(testLogs, "zero")
    print(res4)
    
    print("Test 5")
    res5 = sortLog([], 0)
    print(res5)

if __name__ == "__main__":
    test()