import sys
import io

def cleanLineSpaces(line):
    line = line.strip()
    result = ""
    lastChar = ""

    for char in line:
        if char == " " and lastChar == " ":
            continue
        result += char
        lastChar = char
    return result

def main():
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    line = ""
    preamble = ""

    lineCounter = 0
    emptyLinesCounter = 0
    inPreamble = True

    while True:
        char = sys.stdin.read(1)

        if not char:
            if line:
                if inPreamble:
                    cleanedLine = cleanLineSpaces(line)
                    preamble += cleanedLine + "\n"
                    sys.stdout.write(preamble + "\n")
                else:
                    cleanedLine = cleanLineSpaces(line)
                    sys.stdout.write(cleanedLine + "\n")
            break

        if char != "\n":
            line += char
        else:
            lineCounter += 1

            if line == "-----":
                break

            if inPreamble:
                if line.strip() == "":
                    emptyLinesCounter += 1
                else:
                    emptyLinesCounter = 0

                cleanedLine = cleanLineSpaces(line)
                preamble += cleanedLine + "\n"
                
                if emptyLinesCounter >= 2:
                    inPreamble = False
                    preamble = ""
                elif lineCounter >= 10:
                    inPreamble = False
                    sys.stdout.write(preamble)
                    preamble = ""
            else:
                cleanedLine = cleanLineSpaces(line)
                sys.stdout.write(cleanedLine + "\n")

            line = ""

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.stderr.write(str(e) + "\n")
                