import sys

from common import read_sentences, print_output

def is_target_word(word):
    w = ""
    for c in word:
        w += c.lower()
    
    if w == "i" or w == "oraz" or w == "ale" or w == "że" or w == "lub":
        return True
    return False

def process_3j(sentence):
    target_count = 0
    current_word = ""
    
    for c in sentence:
        if c.isalpha():
            current_word += c
        else:
            if current_word != "":
                if is_target_word(current_word):
                    target_count += 1
                current_word = ""
                
    # Sprawdzenie ostatniego wyrazu (jeśli zdanie nie kończy się znakiem interpunkcyjnym)
    if current_word != "":
        if is_target_word(current_word):
            target_count += 1
            
    if target_count >= 2:
        return sentence
    return ""

if __name__ == '__main__':
    try:
        count = read_sentences(process_3j, print_output)
        
        if not count:
            sys.stderr.write("Informacja: Brak treści odpowiadającej filtrowi lub plik jest pusty.\n")
    except Exception as e:
        sys.stderr.write("Blad: " + str(e) + "\n")