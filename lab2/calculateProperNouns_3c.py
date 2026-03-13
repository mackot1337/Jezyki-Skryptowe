import sys
import io

def calculateProperNouns():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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

    return (properNounSentences/totalSentences) * 100 if totalSentences > 0 else 0

if __name__ == "__main__":
    try:
        result = calculateProperNouns()
        sys.stdout.write(f"{result:.2f}\n")
    except Exception as e:
        sys.stderr.write(str(e) + "\n")