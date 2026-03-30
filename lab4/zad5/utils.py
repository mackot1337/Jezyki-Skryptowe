import os
import csv
from datetime import datetime

def getConvertedDir():
    targetDir = os.environ.get("CONVERTED_DIR", os.path.join(os.getcwd(), "converted"))

    if not os.path.exists(targetDir):
        os.makedirs(targetDir)

    return targetDir

def saveToHistory(originalPath, outputFormat, outputPath, programUsed):
    targetDir = getConvertedDir()
    historyFile = os.path.join(targetDir, "history.csv")

    fileExists = os.path.isfile(historyFile)

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    with open(historyFile, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not fileExists:
            writer.writerow(["Data", "Oryginalny plik", "Format wyjściowy", "Plik wynikowy", "Program"])
        writer.writerow([now, originalPath, outputFormat, outputPath, programUsed])