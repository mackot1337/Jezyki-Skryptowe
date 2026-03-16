import sys
from utils import result, setEncoding

def findFirstComplexSentence():
    setEncoding()

    current = ""

    while True:
        char = sys.stdin.read(1)
        if not char:
            if current.strip() != "" and current.count(",") > 1:
                return current.strip()
            break

        current += char

        if char in ".?!":
            if current.count(",") > 1:
                return current.strip()
            current = ""

    return ""

if __name__ == '__main__':
    result(findFirstComplexSentence)