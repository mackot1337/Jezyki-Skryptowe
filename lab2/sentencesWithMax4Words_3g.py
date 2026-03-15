import sys

from common import read_sentences, print_output

def process_3g(sentence):
    word_count = 0
    in_word = False
    
    for c in sentence:
        if c.isalpha():
            if not in_word:
                word_count += 1
                in_word = True
        else:
            in_word = False
            
    if 0 < word_count <= 4:
        return sentence
    return ""

if __name__ == '__main__':
    try:
        count = read_sentences(process_3g, print_output)
        
        if not count:
            sys.stderr.write("Informacja: Brak treści odpowiadającej filtrowi lub plik jest pusty.\n")
    except Exception as e:
        sys.stderr.write("Blad: " + str(e) + "\n")