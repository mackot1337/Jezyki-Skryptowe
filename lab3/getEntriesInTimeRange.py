import  datetime

def getEntriesInTimeRange(log, start, end):
    if type(log) != list:
        print("Error: log is not a list")
        return []

    if type(start) != datetime.datetime:
        print("Error: start is not a datetime")
        return []

    if type(end) != datetime.datetime:
        print("Error: end is not a datetime")
        return []

    if start > end:
        print("Error: start is after end")
        return []

    result = []

    for entry in log:
        if len(entry) > 0:
            ts = entry[0]

            if type(ts) == datetime.datetime:
                if ts >= start and ts < end:
                    result.append(entry)

    return result

def test():
    t1 = datetime.datetime(2021, 1, 1, 10, 0, 0) 
    t2 = datetime.datetime(2021, 1, 1, 10, 5, 0) 
    t3 = datetime.datetime(2021, 1, 1, 10, 10, 0)
    t4 = datetime.datetime(2021, 1, 1, 10, 15, 0)
    
    testLogs = [
        (t1, "uid1", "ip", 80, "ip", 80, "GET", "host", "/A", 200),
        (t2, "uid2", "ip", 80, "ip", 80, "GET", "host", "/B", 200),
        (t3, "uid3", "ip", 80, "ip", 80, "GET", "host", "/C", 200),
        (t4, "uid4", "ip", 80, "ip", 80, "GET", "host", "/D", 200)
    ]
    
    print("Testy funkcji getEntriesInTimeRange")
    
    print("Test 1")
    res1 = getEntriesInTimeRange(testLogs, t1, t3)
    print(res1)
    
    print("Test 2")
    res2 = getEntriesInTimeRange(testLogs, t4, t1)
    print(res2)
    
    print("Test 3")
    res3 = getEntriesInTimeRange(testLogs, "2021-01-01", "2021-01-02")
    print(res3)
    
    print("Test 4")
    res4 = getEntriesInTimeRange([], t1, t4)
    print(res4)

if __name__ == "__main__":
    test()