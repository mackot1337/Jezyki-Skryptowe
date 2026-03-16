import sys
from utils import setEncoding

def countNoWhiteChars():
    setEncoding()

    count = 0

    while True:
        char = sys.stdin.read(1)
        if not char:
            break

        if not char.isspace():
            count += 1

    return count

if __name__ == "__main__":
    try:
        result = countNoWhiteChars()
        sys.stdout.write(str(result) + "\n")
    except Exception as e:
        sys.stderr.write(str(e) + "\n")