import os
import csv
import sys
from utils import getConvertedDir, saveToHistory
from mediaConvert import getProgram, main

import shutil

def testGetProgram():
    assert getProgram("film.mp4") == "ffmpeg", "Błąd: .mp4 powinno być dla ffmpeg"
    assert getProgram("zdjecie.jpg") == "magick", "Błąd: .jpg powinno być dla magick"
    assert getProgram("dokument.txt") is None, "Błąd: .txt powinno zwrócić None"
    
    assert getProgram("plik_bez_kropki") is None, "Błąd: brak rozszerzenia powinien zwrócić None"
    
    print("Test 1 zaliczony!")

def testEnvVariable():
    testDirName = "testowy_katalog_abc123"
    os.environ["CONVERTED_DIR"] = testDirName
    
    katalog = getConvertedDir()
    
    assert testDirName in katalog, "Błąd: Zmienna środowiskowa nie została użyta"
    assert os.path.exists(katalog), "Błąd: Funkcja nie utworzyła katalogu na dysku"
    
    os.rmdir(katalog)
    del os.environ["CONVERTED_DIR"]
    
    print("Test 2 zaliczony!")

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
    
    print("Test 3 zaliczony!")


def testConversion():
    testInputDir = "testowy_katalog_wejsciowy"
    testOutputDir = "testowy_katalog_wyjsciowy"
    os.makedirs(testInputDir, exist_ok=True)

    path = r"./gatsby.gif"
    
    name = "gatsby.gif"
    targetFile = os.path.join(testInputDir, name)
    
    shutil.copy(path, targetFile)
        
    os.environ["CONVERTED_DIR"] = testOutputDir
    
    oldArgv = sys.argv
    sys.argv = ["mediaConvert.py", testInputDir, "png"]
    
    try:
        main()
    except Exception as e:
        assert False, f"Błąd! Szczegóły: {e}"
        
    converted = os.listdir(testOutputDir)
    plikPng = [plik for plik in converted if plik.endswith(".png")]
    
    assert len(plikPng) > 0, "Błąd: Plik wyjściowy PNG nie został utworzony przez ImageMagick!"
    
    historyFile = os.path.join(testOutputDir, "history.csv")
    assert os.path.exists(historyFile), "Błąd: Plik historii nie powstał."
    
    with open(historyFile, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        assert len(reader) >= 2, "Błąd: Brak wpisu w historii po konwersji"
        assert reader[1][4] == "magick", "Błąd: Skrypt nie zanotował użycia programu magick"
    
    sys.argv = oldArgv
    os.remove(targetFile)
    os.rmdir(testInputDir)
    
    for f in os.listdir(testOutputDir):
        os.remove(os.path.join(testOutputDir, f))
    os.rmdir(testOutputDir)
    del os.environ["CONVERTED_DIR"]
        
    print("Test 4 zaliczony!")

if __name__ == "__main__":
    print("Uruchamiam testy...\n" + "-"*40)
    testGetProgram()
    testEnvVariable()
    testSaveHistory()
    testConversion()
    print("-" * 40 + "\nWszystkie testy zakończone sukcesem!")