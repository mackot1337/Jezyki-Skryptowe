import sys
import io

def countParagraphs():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    count = 0
    lastLineEmpty = False
    hasContent = False

    line = ""

    while True:
        char = sys.stdin.read(1)
        if not char:
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

if __name__ == "__main__":
    try:
        result = countParagraphs()
        sys.stdout.write(str(result) + "\n")
    except Exception as e:
        sys.stderr.write(str(e) + "\n")