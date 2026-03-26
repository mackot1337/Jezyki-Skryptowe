import os
from analyzer import analyzeFile

def testAnalyzeNormalFile():
    testFile = "testNormal.txt"
    with open(testFile, 'w', encoding='utf-8') as f:
        f.write("kot pies kot kot\nptak pies")
    
    result = analyzeFile(testFile)
    
    assert result['words'] == 6, "Błąd zliczania słów"
    assert result['lines'] == 2, "Błąd zliczania wierszy"
    assert result['freqWord'] == "kot", "Błąd szukania najczęstszego słowa"
    
    os.remove(testFile)
    print("Test 1 (normalny plik) zaliczony!")

def testAnalyzeEmptyFile():
    testFile = "test_empty.txt"
    open(testFile, 'w').close()
    
    result = analyzeFile(testFile)
    
    assert result['chars'] == 0, "Pusty plik powinien mieć 0 znaków"
    assert result['words'] == 0, "Pusty plik powinien mieć 0 słów"
    assert result['freqWord'] == "", "Brak słów powinien zwrócić pusty string"
    
    os.remove(testFile)
    print("Test 2 (pusty plik - wartość skrajna) zaliczony!")

if __name__ == "__main__":
    print("Uruchamiam testy dla Zadania 4...\n" + "-"*40)
    testAnalyzeNormalFile()
    testAnalyzeEmptyFile()
    print("-" * 40 + "\nTesty zakończone!")