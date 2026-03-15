from common import read_sentences, print_output
import sys

def process_3h(sentence):
    # Logika sprawdzająca pytania/wykrzykniki
    last_char = ""
    for c in sentence:
        if c not in " \t\n\r":
            last_char = c
    if last_char in "?!":
        return sentence
    return ""

if __name__ == '__main__':
    try:
        count = read_sentences(process_3h, print_output)
        
        if not count:
            sys.stderr.write("Informacja: Brak treści odpowiadającej filtrowi lub plik jest pusty.\n")
    except Exception as e:
        sys.stderr.write("Blad: " + str(e) + "\n")