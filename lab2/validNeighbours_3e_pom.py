import sys

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