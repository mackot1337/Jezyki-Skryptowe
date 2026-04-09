from pathlib import Path
from groupMeasurementFilesByKey import groupMeasurementFilesByKey

def runTests():
    print("Rozpoczynam testowanie Zadania 2...")
    
    testDir = Path("measurement_files_test")
    testDir.mkdir(exist_ok=True)
    
    file1 = testDir / "2023_PM10_24g.csv"
    file2 = testDir / "2022_NO2_1g.csv"
    wrongFile1 = testDir / "raport_styczen.txt"
    wrongFile2 = testDir / "2021_SO2_24g_stary.csv"
    
    file1.touch()
    file2.touch()
    wrongFile1.touch()
    wrongFile2.touch()

    emptyDir = Path("empty_test_dir")
    emptyDir.mkdir(exist_ok=True)

    result = groupMeasurementFilesByKey(testDir)
    assert len(result) == 2, "Błąd w Test A: Funkcja powinna wyłapać dokładnie 2 pliki!"
    assert ("2023", "PM10", "24g") in result, "Błąd w Test A: Brak klucza dla pierwszego pliku!"
    assert result[("2022", "NO2", "1g")] == file2, "Błąd w Test A: Ścieżka przypisana do klucza jest zła!"
    print("Test A (Wyszukiwanie regexem i grupowanie) -> ZALICZONY")

    emptyResult = groupMeasurementFilesByKey(emptyDir)
    assert emptyResult == {}, "Błąd w Test B: Pusty folder nie zwrócił pustego słownika!"
    print("Test B (Pusty folder) -> ZALICZONY")

    testCSuccess = False
    try:
        groupMeasurementFilesByKey("some_dir")
    except NotADirectoryError:
        testCSuccess = True
    assert testCSuccess == True, "Błąd w Test C: Funkcja nie rzuciła błędu dla nieistniejącego folderu!"
    print("Test C (Nieistniejący folder) -> ZALICZONY")

    file1.unlink()
    file2.unlink()
    wrongFile1.unlink()
    wrongFile2.unlink()
    testDir.rmdir()
    emptyDir.rmdir()

    print("Wszystkie testy Z2 wykonane pomyślnie!\n")

if __name__ == "__main__":
    runTests()