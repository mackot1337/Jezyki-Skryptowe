import sys
import io
from utils import setEncoding

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

if __name__ == "__main__":
    try:
        result = findFirstComplexSentence()
        if result:
            sys.stdout.write(result + "\n")
        else:
            sys.stdout.write("No complex sentence found.\n")
    except Exception as e:
        sys.stderr.write(f"Wystąpił błąd: {e}\n")