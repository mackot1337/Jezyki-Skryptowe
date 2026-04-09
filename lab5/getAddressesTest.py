import os
from getAddresses import getAddresses

def runTest():
    print("Rozpoczynam testowanie Zadania 3...")
    
    testFile = "stacje_test_z3.csv"
    with open(testFile, 'w', encoding='utf-8') as f:
        f.write("Województwo,Miejscowość,Adres\n")
        f.write("MAŁOPOLSKIE,Kraków,ul. Dietla 4/6\n")
        f.write("MAŁOPOLSKIE,Kraków,Aleja Krasickiego\n")
        f.write("MAZOWIECKIE,Warszawa,ul. Wolska 11\n")
        
    krakowResult = getAddresses(testFile, "Kraków")
    assert len(krakowResult) == 2, "Błąd Test A: Powinno znaleźć 2 stacje dla Krakowa!"
    assert krakowResult[0] == ("MAŁOPOLSKIE", "Kraków", "ul. Dietla", "4/6"), "Błąd Test A: Źle rozbity adres nr 1!"
    assert krakowResult[1] == ("MAŁOPOLSKIE", "Kraków", "Aleja Krasickiego", ""), "Błąd Test A: Źle rozbity adres nr 2!"
    print("Test A (Rozbijanie adresów) -> ZALICZONY")
    
    sosnowiecResult = getAddresses(testFile, "Sosnowiec")
    assert sosnowiecResult == [], "Błąd Test B: Dla nieistniejącego miasta powinna być pusta lista!"
    print("Test B (Miasto-widmo) -> ZALICZONY")
    
    testCSuccess = False
    try:
        getAddresses("katalog_ktorego_nie_ma/stacje.csv", "Kraków")
    except FileNotFoundError:
        testCSuccess = True
    assert testCSuccess == True, "Błąd Test C: Nie wyrzuciło błędu przy złej ścieżce!"
    print("Test C (Brak pliku) -> ZALICZONY")
    
    os.remove(testFile)
    print("Wszystkie testy Z3 wykonane pomyślnie!\n")

if __name__ == "__main__":
    runTest()