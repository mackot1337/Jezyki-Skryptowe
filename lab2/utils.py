import io
import sys

def setEncoding():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def validNeighbours(sentence):
    lastFirstChar = ""
    inWord = False

    for char in sentence:
        if char.isalpha():
            if not inWord:
                currentFirstChar = char.lower()
                if currentFirstChar == lastFirstChar:
                    return False
                lastFirstChar = currentFirstChar
                inWord = True
        else:
            inWord = False
    return True