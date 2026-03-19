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

if __name__ == "__main__":
    print(readLog(sys.stdin))