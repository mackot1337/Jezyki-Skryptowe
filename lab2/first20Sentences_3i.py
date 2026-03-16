from filter_utils import filter_result
from utils import print_output_newline

sentence_counter = 0

def filter_first_20_sentences(sentence):
    global sentence_counter
    if sentence_counter < 20:
        sentence_counter += 1
        return sentence
    return ""

if __name__ == '__main__':
    filter_result(filter_first_20_sentences, print_output_newline)