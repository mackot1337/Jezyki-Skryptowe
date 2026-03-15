import io
import sys

def print_output(text):
    sys.stdout.write(text + "\n")

def read_sentences(process_func, print_func):
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    sentence = ""
    newline_count = 0
    found = False 

    try:
        while True:
            char = sys.stdin.read(1)
            if not char:
                cleaned = sentence.strip()
                if cleaned:
                    res = process_func(cleaned)
                    if res:
                        print_func(res)
                        found = True
                break

            sentence += char
            if char == '\n':
                newline_count += 1
            elif char != '\r' and char != ' ':
                newline_count = 0

            if char in ".?!" or newline_count >= 2:
                cleaned = sentence.strip()
                if cleaned:
                    res = process_func(cleaned)
                    if res:
                        print_func(res)
                        found = True
                sentence = ""
                newline_count = 0
        
        return found

    except Exception as e:
        sys.stderr.write("Blad: " + str(e) + "\n")
        return 0