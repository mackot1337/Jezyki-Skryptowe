import os
import sys
import json
import subprocess
from collections import Counter

def main():
    if len(sys.argv) < 2:
        print("Użycie: python runner.py <ścieżka_do_katalogu>")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Błąd: '{directory}' nie jest katalogiem.")
        sys.exit(1)

    results = []

    for fileName in os.listdir(directory):
        path = os.path.join(directory, fileName)

        if not os.path.isfile(path):
            continue

        process = subprocess.run(
            ["python", "analyzer.py"],
            input=path,
            text=True,
            capture_output=True
        )

        if process.returncode == 0 and process.stdout.strip():
            try:
                data = json.loads(process.stdout)
                if "error" not in data:
                    results.append(data)
            except json.JSONDecodeError:
                print(f"Błąd dekodowania JSON z pliku: {path}")

    totalFiles = len(results)
    if totalFiles == 0:
        print("Brak plików do analizy.")
        return
    
    totalChars = sum(r['chars'] for r in results)
    totalWords = sum(r['words'] for r in results)
    totalLines = sum(r['lines'] for r in results)

    allFreqChars = [r['freqChar'] for r in results if r['freqChar']]
    allFreqWords = [r['freqWord'] for r in results if r['freqWord']]

    overallFreqChar = Counter(allFreqChars).most_common(1)[0][0] if allFreqChars else ""
    overallFreqWord = Counter(allFreqWords).most_common(1)[0][0] if allFreqWords else ""

    print("\n--- PODSUMOWANIE ANALIZY ---")
    print(f"Liczba przeczytanych plików: {totalFiles}")
    print(f"Sumaryczna liczba znaków: {totalChars}")
    print(f"Sumaryczna liczba słów: {totalWords}")
    print(f"Sumaryczna liczba wierszy: {totalLines}")
    print(f"Znak występujący najczęściej: '{overallFreqChar}'")
    print(f"Słowo występujące najczęściej: '{overallFreqWord}'")

if __name__ == "__main__":
    main()