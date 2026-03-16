import sys
from utils import result, setEncoding

def countParagraphs():
    setEncoding()

    count = 0
    lastLineEmpty = False
    hasContent = False

    line = ""

    while True:
        char = sys.stdin.read(1)
        if not char:
            if hasContent and not lastLineEmpty:
                count += 1
            break

        if char != '\n':
            line += char
        else:
            if line.strip() == "":
                if not lastLineEmpty and hasContent:
                    count += 1
                    lastLineEmpty = True
            else:
                hasContent = True
                lastLineEmpty = False
            line = ""

    return count

if __name__ == '__main__':
    result(countParagraphs)