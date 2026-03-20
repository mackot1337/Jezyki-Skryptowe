def getEntriesByExtension(log, ext):
    if type(ext) != str:
        print("Error: ext is not a string")
        return []
    
    wantedExtension = "." + ext

    result = []

    for entry in log:
        if len(entry) > 8:
            uri = entry[8]

            cleanUri = uri.split("?")[0]

            if cleanUri.endswith(wantedExtension):
                result.append(entry)

    return result

def test():
    testLogs = [
        ("ts", "uid1", "ip", 80, "ip", 80, "GET", "host", "/image.jpg", 200),
        ("ts", "uid2", "ip", 80, "ip", 80, "GET", "host", "/photo.jpg?size=1024&crop=1", 200),
        ("ts", "uid3", "ip", 80, "ip", 80, "GET", "host", "/index.html", 200),
        ("ts", "uid4", "ip", 80, "ip", 80, "GET", "host", "/script.js?v=2.0", 200)
    ]
    
    print("Testy funkcji getEntriesByExtension")
    
    print("Test 1")
    res1 = getEntriesByExtension(testLogs, "jpg")
    print(res1)
    
    print("Test 2")
    res2 = getEntriesByExtension(testLogs, "js")
    print(res2)
    
    print("Test 3")
    res3 = getEntriesByExtension(testLogs, 123)
    print(res3)
    
    print("Test 4")
    res4 = getEntriesByExtension([], "jpg")
    print(res4)

if __name__ == "__main__":
    test()