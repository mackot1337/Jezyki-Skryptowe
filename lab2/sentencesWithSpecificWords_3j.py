from filter_utils import filter_result
from utils import print_output_newline

def is_target_word(word):
    w = ""
    for c in word:
        w += c.lower()
    
    if w == "i" or w == "oraz" or w == "ale" or w == "że" or w == "lub":
        return True
    return False

def filter_sentences_with_specific_words(sentence):
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
                
    if current_word != "":
        if is_target_word(current_word):
            target_count += 1
            
    if target_count >= 2:
        return sentence
    return ""

if __name__ == '__main__':
    filter_result(filter_sentences_with_specific_words, print_output_newline)