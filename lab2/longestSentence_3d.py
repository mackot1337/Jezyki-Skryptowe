import sys
from utils import setEncoding

def longestSentence():
    setEncoding()
    
    longest = ""
    current = ""
    newLineCount = 0

    while True:
        char = sys.stdin.read(1)
        if not char:
            if current.strip() != "" and len(current.strip()) > len(longest):
                longest = current.strip()
            break

        if char == "\n":
            newLineCount += 1
            if newLineCount >= 2:
                if current.strip() != "" and len(current.strip()) > len(longest):
                    longest = current.strip()
                current = ""
            else:
                if current.strip() != "" and current[-1] != " ":
                    current += " "
        else:
            if char.strip() or char == " ":
                newLineCount = 0
            current += char

            if char in ".?!":
                if len(current.strip()) > len(longest):
                    longest = current.strip()
                current = ""
    return longest

if __name__ == "__main__":
    try:
        result = longestSentence()
        sys.stdout.write(result + "\n")
    except Exception as e:
        sys.stderr.write(str(e) + "\n")