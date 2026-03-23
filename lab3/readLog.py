import sys
import datetime

def readLog(stream):
    logs = []

    for line in stream:
        line = line.strip()
        if not line:
            continue

        fields = line.split("\t")
        if len(fields) <= 11:
            continue

        try:
            ts = datetime.datetime.fromtimestamp(float(fields[0]))

            uid = fields[1]
            idOrigH = fields[2]
            idOrigP = int(fields[3]) if fields[3].isdigit() else 0
            
            idRespH = fields[4]
            idRespP = int(fields[5]) if fields[5].isdigit() else 0

            method = fields[7]
            host = fields[8]
            uri = fields[9]

            statusCode = int(fields[11]) if fields[11].isdigit() else None

            tup = (ts, uid, idOrigH, idOrigP, idRespH, idRespP, method, host, uri, statusCode)

            logs.append(tup)
        except (ValueError, TypeError):
            continue

    return logs

def test():
    print("Testy funkcji readLog\n")
    
    print("Test 1: Poprawne dane")
    # valid_record = ["1680133200\tU123\t192.168.1.1\t1234\t10.0.0.1\t80\t-\tGET\texample.com\t/index.html\t-\t200\n"]
    valid_record = ["1331901000.000000	CHEt7z3AzG4gyCNgci	192.168.202.79	50465	192.168.229.251	80	1	HEAD	192.168.229.251	/DEASLog02.nsf	-	Mozilla/5.0 (compatible; Nmap Scripting Engine; http://nmap.org/book/nse.html)	0	0	404	Not Found	-	-	-	(empty)	-	-	-	-	-	-	-\n"]
    res1 = readLog(valid_record)
    print("Wynik:", len(res1), "rekordów")
    if res1: print(res1[0])
    
    print("\nTest 2: Puste wejście")
    res2 = readLog([])
    print("Wynik:", res2)
    
    print("\nTest 3: Błędne dane (za mało kolumn)")
    invalid_record = ["1680133200\tU123\t192.168.1.1\n"]
    res3 = readLog(invalid_record)
    print("Wynik:", res3)
    
    print("\nTest 4: Błędne dane (nieprawidłowy timestamp)")
    bad_ts_record = ["INVALID_TS\tU123\t192.168.1.1\t1234\t10.0.0.1\t80\t-\tGET\texample.com\t/index.html\t-\t200\n"]
    res4 = readLog(bad_ts_record)
    print("Wynik:", res4)

if __name__ == "__main__":
    test()