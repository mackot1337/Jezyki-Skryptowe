import os
import csv
from utils import getConvertedDir, saveToHistory
from mediaConvert import getProgram

def testGetProgram():
    assert getProgram("film.mp4") == "ffmpeg", "Błąd: .mp4 powinno być dla ffmpeg"
    assert getProgram("zdjecie.jpg") == "magick", "Błąd: .jpg powinno być dla magick"
    assert getProgram("dokument.txt") is None, "Błąd: .txt powinno zwrócić None"
    
    assert getProgram("plik_bez_kropki") is None, "Błąd: brak rozszerzenia powinien zwrócić None"
    
    print("Test 1 (rozpoznawanie programów i wartości skrajne) zaliczony!")

def testEnvVariable():
    testDirName = "testowy_katalog_abc123"
    os.environ["CONVERTED_DIR"] = testDirName
    
    katalog = getConvertedDir()
    
    assert testDirName in katalog, "Błąd: Zmienna środowiskowa nie została użyta"
    assert os.path.exists(katalog), "Błąd: Funkcja nie utworzyła katalogu na dysku"
    
    os.rmdir(katalog)
    del os.environ["CONVERTED_DIR"]
    
    print("Test 2 (zmienne środowiskowe) zaliczony!")

def testSaveHistory():
    testDirName = "testowy_katalog_historia"
    os.environ["CONVERTED_DIR"] = testDirName
    
    saveToHistory("oryginal.avi", "mp4", "wynik.mp4", "ffmpeg")
    
    historyFIle = os.path.join(testDirName, "history.csv")
    
    assert os.path.exists(historyFIle), "Błąd: Plik historii nie powstał"
    
    with open(historyFIle, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        assert len(reader) == 2, "Błąd: Oczekiwano 1 wiersza nagłówka i 1 wiersza danych"
        assert reader[1][1] == "oryginal.avi", "Błąd: Zła nazwa pliku źródłowego"
        assert reader[1][4] == "ffmpeg", "Błąd: Zła nazwa użytego programu"
    
    os.remove(historyFIle)
    os.rmdir(testDirName)
    del os.environ["CONVERTED_DIR"]
    
    print("Test 3 (zapis historii CSV i sprzątanie) zaliczony!")

if __name__ == "__main__":
    print("Uruchamiam testy (wersja manualna)...\n" + "-"*40)
    testGetProgram()
    testEnvVariable()
    testSaveHistory()
    print("-" * 40 + "\nWszystkie testy zakończone sukcesem!")