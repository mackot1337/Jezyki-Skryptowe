import io
import sys

def setEncoding():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_output_newline(text):
    sys.stdout.write(text + "\n")

def result(func):
    try:
        output = func()
        sys.stdout.write(str(output) + "\n")
    except Exception as e:
        sys.stderr.write(str(e) + "\n")

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