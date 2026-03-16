import sys
from utils import print_output_newline, setEncoding

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
    setEncoding()

    line = ""
    preamble = ""

    lineCounter = 0
    emptyLinesCounter = 0
    inPreamble = True

    while True:
        char = sys.stdin.read(1)

        if not char:
            if line:
                cleanedLine = cleanLineSpaces(line)
                if inPreamble:
                    preamble += cleanedLine + "\n"
                    print_output_newline(preamble)
                else:
                    print_output_newline(cleanedLine)
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
                    print_output_newline(preamble)
                    preamble = ""
            else:
                cleanedLine = cleanLineSpaces(line)
                print_output_newline(cleanedLine)

            line = ""

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.stderr.write(str(e) + "\n")
                