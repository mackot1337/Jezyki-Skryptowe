import sys
from utils import result, setEncoding

def calculateProperNouns():
    setEncoding()

    totalSentences = 0
    properNounSentences = 0

    isFirstWord = True
    inWord = False
    hasProperNoun = False
    hasContent = False
    newLineCounter = 0

    while True:
        char = sys.stdin.read(1)
        if not char:
            if hasContent:
                totalSentences += 1
                if hasProperNoun:
                    properNounSentences += 1
            break
        
        if char == "\n":
            newLineCounter += 1
            if newLineCounter >= 2:
                if hasContent:
                    totalSentences += 1
                    if hasProperNoun:
                        properNounSentences += 1
                
                isFirstWord = True
                inWord = False
                hasProperNoun = False
                hasContent = False
            continue
        elif not char.isspace():
            newLineCounter = 0

        if char.isalpha():
            if not inWord:
                if not isFirstWord and char.isupper():
                    hasProperNoun = True
                inWord = True
                hasContent = True
                isFirstWord = False
        else:
            inWord = False
        
        if char in ".?!":
            if hasContent:
                totalSentences += 1
                if hasProperNoun:
                    properNounSentences += 1
            
            isFirstWord = True
            inWord = False
            hasProperNoun = False
            hasContent = False

    return (properNounSentences/totalSentences) * 100

if __name__ == '__main__':
    result(calculateProperNouns)