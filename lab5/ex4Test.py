from ex4 import *

def runTest():
    print("Rozpoczynam testowanie Zadania 4...")
    
    testData = [
        {'Kod stacji': 'KrakMOB', 'Nazwa stacji': 'Kraków - Aleja Krasińskiego', 'Data uruchomienia': '2010-01-01', 'WGS84 φ N': '50.058333', 'WGS84 λ E': '19.926111', 'Rodzaj stacji': 'mobilna'},
        {'Kod stacji': 'Wawa01', 'Nazwa stacji': 'Warszawa - Centrum - Północ', 'Data zamknięcia': '2023-12-31', 'WGS84 φ N': '52.229', 'WGS84 λ E': '21.012', 'Rodzaj stacji': 'stacjonarna'}, # Złe współrzędne (brak 6 cyfr)
        {'Kod stacji': 'Biel02', 'Nazwa stacji': 'Bielawa, ul. Grota', 'Data uruchomienia': 'Zla_Data', 'WGS84 φ N': '50.682510', 'WGS84 λ E': '16.617348', 'Rodzaj stacji': 'stacjonarna'},
        {'Kod stacji': 'FakeMOB', 'Nazwa stacji': 'Zła Stacja', 'Rodzaj stacji': 'stacjonarna'} # Fałszywy MOB żeby uwalić weryfikację
    ]
    
    daty = pullDates(testData)
    assert '2010-01-01' in daty, "Błąd 4a"
    assert 'Zla_Data' not in daty, "Błąd 4a"
    print("Test 4a (Daty) ZALICZONY")
    
    coords = pullCoordinates(testData)
    assert coords[0] == ('50.058333', '19.926111'), "Błąd 4b"
    assert len(coords) == 2, "Błąd 4b: Powinno być 2"
    print("Test 4b (Współrzędne) ZALICZONY")

    assert pullTwoPartNames(testData) == ['Kraków - Aleja Krasińskiego'], "Błąd 4c"
    assert pullThreePartNames(testData) == ['Warszawa - Centrum - Północ'], "Błąd 4f"
    print("Test 4c i 4f (Człony i myślniki) ZALICZONE")
    
    assert cleanName("Żółta Gęś") == "Zolta_Ges", "Błąd 4d"
    print("Test 4d (Czyszczenie nazw) ZALICZONY")
    
    assert verify_mob(testData) == False, "Błąd 4e"
    print("Test 4e (Weryfikacja MOB) ZALICZONY")
    
    assert stationWithStreet(testData) == ['Bielawa, ul. Grota'], "Błąd 4g"
    print("Test 4g (Przecinki i ulice) ZALICZONY")
    
    print("Wszystkie testy Z4 wykonane pomyślnie!\n")

if __name__ == "__main__":
    runTest()