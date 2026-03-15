import sys

from common import read_sentences, print_output

sentence_counter = 0

def process_3i(sentence):
    global sentence_counter
    if sentence_counter < 20:
        sentence_counter += 1
        return sentence
    return ""

if __name__ == '__main__':
    try:
        count = read_sentences(process_3i, print_output)
        
        if not count:
            sys.stderr.write("Informacja: Brak treści odpowiadającej filtrowi lub plik jest pusty.\n")
    except Exception as e:
        sys.stderr.write("Blad: " + str(e) + "\n")