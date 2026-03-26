import os
import sys
import subprocess
from datetime import datetime
import mimetypes

from utils import getConvertedDir, saveToHistory

def getProgram(path):
    mimeType = mimetypes.guess_type(path)[0]
    if mimeType:
        if mimeType.startswith("image"):
            return "magick"
        elif mimeType.startswith("video") or mimeType.startswith("audio"):
            return "ffmpeg"

    return None

def main():
    if len(sys.argv) < 3:
        print("Użycie: python mediaconvert.py <katalog_wejsciowy> <format_wyjsciowy>")
        sys.exit(1)

    inputDir = sys.argv[1]
    outputFormat = sys.argv[2]

    targetDir = getConvertedDir()

    if not os.path.isdir(inputDir):
        print(f"Błąd: '{inputDir}' nie jest poprawnym katalogiem.")
        sys.exit(1)

    for filename in os.listdir(inputDir):
        inputPath = os.path.join(inputDir, filename)

        if not os.path.isfile(inputPath):
            continue

        program = getProgram(inputPath)
        if not program:
            print(f"Pominięto plik {filename} - nie rozpoznano typu multimediów.")
            continue

        timestamp = datetime.now().strftime("%Y%m%d")
        nameWithoutExt = os.path.splitext(filename)[0]
        outputFileName = timestamp + "-" + nameWithoutExt + "." + outputFormat
        outputPath = os.path.join(targetDir, outputFileName)

        print(f"Konwertowanie pliku {filename} przy użyciu programu {program}...")

        try:
            if program == "ffmpeg":
                subprocess.run(["ffmpeg", "-i", inputPath, outputPath], check=True)
            elif program == "magick":
                subprocess.run(["magick", inputPath, outputPath], check=True)

            saveToHistory(inputPath, outputFormat, outputPath, program)
            print(f"Sukces: zapisano jako {outputFileName}")

        except subprocess.CalledProcessError as e:
            print(f"Blad: Konwersja pliku {filename} zakonczona niepowodzeniem. Szczegły: {e}")

if __name__ == "__main__":
    main()