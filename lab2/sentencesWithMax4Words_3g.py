from filter_utils import filter_result
from utils import print_output_newline

def filter_sentences_with_max_4_words(sentence):
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
    filter_result(filter_sentences_with_max_4_words, print_output_newline)