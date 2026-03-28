import sys
import json
from collections import Counter

def analyzeFile(path):
    path = path.strip()

    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        return {"Blad": str(e)}
    
    if not text:
        return {"path": path, "chars": 0, "words": 0, "lines": 0, "freqChar": "", "freqWord": ""}
    
    chars = len(text)
    wordsList = text.split()
    words = len(wordsList)
    lines = len(text.splitlines())

    textNoSpaces = "".join(wordsList)
    freqChar = Counter(textNoSpaces).most_common(1)[0][0] if textNoSpaces else ""
    freqWord = Counter(wordsList).most_common(1)[0][0] if wordsList else ""

    return {"path": path, "chars": chars, "words": words, "lines": lines, "freqChar": freqChar, "freqWord": freqWord}

if __name__ == "__main__":
    inputPath = sys.stdin.read().strip()
    if inputPath:
        result = analyzeFile(inputPath)
        print(json.dumps(result))