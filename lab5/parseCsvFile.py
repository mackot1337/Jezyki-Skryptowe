import csv
import os
import logging

logger = logging.getLogger("logger")

def parseCsvFile(filePath):
    if not os.path.exists(filePath):
        logger.error(f"Krytyczny błąd: Plik {filePath} nie istnieje!")
        raise FileNotFoundError("Błąd: Plik " + str(filePath) + " nie istnieje!")

    result = []
    logger.info(f"Otwieranie pliku: {filePath}")

    try:
        with open(filePath, mode='r', encoding='utf-8') as file:
            # We will read lines manually to count bytes before passing to csv.reader
            def line_reader():
                for line in file:
                    b_count = len(line.encode('utf-8'))
                    logger.debug(f"Przeczytano wiersz danych. Liczba bajtów: {b_count}")
                    yield line

            reader = csv.reader(line_reader(), delimiter=',')
            try:
                headers = next(reader, None)
            except StopIteration:
                headers = None

            if headers is None:
                logger.info(f"Zamykanie pliku: {filePath} (pusty)")
                return result

            for row in reader:
                record = {}
                for index in range(min(len(headers), len(row))):
                    key = headers[index]    
                    value = row[index]      
                    record[key] = value

                result.append(record)
    finally:
        logger.info(f"Zamykanie pliku: {filePath}")

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