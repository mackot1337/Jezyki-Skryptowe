from filter_utils import filter_result
from utils import print_output_newline

def filter_questions_and_exclamations(sentence):
    last_char = ""
    for c in sentence:
        if c not in " \t\n\r":
            last_char = c
    if last_char in "?!":
        return sentence
    return ""

if __name__ == '__main__':
    filter_result(filter_questions_and_exclamations, print_output_newline)