import csv
import os

def parseCsvFile(filePath):
    if not os.path.exists(filePath):
        raise FileNotFoundError("Błąd: Plik " + str(filePath) + " nie istnieje!")

    result = []

    with open(filePath, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        headers = next(reader, None)

        if headers is None:
            return result

        for row in reader:
            record = {}
            for index in range(len(headers)):
                key = headers[index]    
                value = row[index]      
                record[key] = value

            result.append(record)

    return result

# stations = "stacje.csv"

# print(f"Próbuję wczytać plik: {stations}...")

# try:
#     stationsData = parseCsvFile(stations)
    
#     print(f"Sukces! Wczytano {len(stationsData)} stacji pomiarowych.\n")
    
#     print("Oto dwa pierwsze rekordy:")
#     for rekord in stationsData[:2]:
#         print(rekord)
#         print("-" * 40)
        
# except FileNotFoundError as e:
#     print(e)
# except UnicodeDecodeError:
#     print("Błąd kodowania znaków! Zmień 'encoding' w wywołaniu funkcji na 'windows-1250'.")