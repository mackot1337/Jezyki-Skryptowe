import sys

from utils import setEncoding

def read_sentences(filter_func, print_func):
    setEncoding()

    sentence = ""
    newline_count = 0
    found = False 

    try:
        while True:
            char = sys.stdin.read(1)
            if not char:
                cleaned = sentence.strip()
                if cleaned:
                    res = filter_func(cleaned)
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
                is_paragraph = (newline_count >= 2)
                cleaned = sentence.strip()
                if cleaned:
                    res = filter_func(cleaned)
                    if res:
                        print_func(res)
                        found = True
                if is_paragraph and res:
                    print_func("")
                sentence = ""
                newline_count = 0
        
        return found

    except Exception as e:
        sys.stderr.write("Blad: " + str(e) + "\n")
        return 0
    
def filter_result(filter_func, print_func):
    try:
        count = read_sentences(filter_func, print_func)
        if not count:
            sys.stderr.write("Informacja: Brak treści odpowiadającej filtrowi lub plik jest pusty.\n")
    except Exception as e:
        sys.stderr.write("Blad: " + str(e) + "\n")