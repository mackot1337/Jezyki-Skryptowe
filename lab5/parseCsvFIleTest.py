import os
from parseCsvFile import parseCsvFile

def runTests():
    print("Rozpoczynam testowanie...")
    
    correctFile = "testowy_poprawny.csv"
    emptyFile = "testowy_pusty.csv"
    
    with open(correctFile, 'w', encoding='utf-8') as f:
        f.write("id,nazwa,wartosc\n1,Stacja_A,10.5\n2,Stacja_B,20.1")
        
    with open(emptyFile, 'w', encoding='utf-8') as f:
        f.write("")
    
    correctResult = parseCsvFile(correctFile)
    assert len(correctResult) == 2, "Błąd w Test A: Oczekiwano 2 wierszy danych!"
    assert correctResult[0]['nazwa'] == 'Stacja_A', "Błąd w Test A: Zła nazwa w pierwszym wierszu!"
    print("Test A (Poprawne dane) -> ZALICZONY")

    emptyResult = parseCsvFile(emptyFile)
    assert emptyResult == [], "Błąd w Test B: Pusty plik nie zwrócił pustej listy!"
    print("Test B (Pusty plik) -> ZALICZONY")

    testCSuccess = False
    try:
        parseCsvFile("noFile.csv")
    except FileNotFoundError:
        testCSuccess = True
        
    assert testCSuccess == True, "Błąd w Test C: Funkcja nie rzuciła błędu o braku pliku!"
    print("Test C (Brak pliku) -> ZALICZONY")

    os.remove(correctFile)
    os.remove(emptyFile)
    
    print("Wszystkie testy wykonane pomyślnie!")

if __name__ == "__main__":
    runTests()