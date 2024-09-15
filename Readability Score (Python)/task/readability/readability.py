import math
import argparse
import re
from nltk.tokenize import sent_tokenize, regexp_tokenize


grade_dict = {
    1: {"Age": "5-6", "Grade Level": "Kindergarten"},
    2: {"Age": "6-7", "Grade Level": "First Grade"},
    3: {"Age": "7-8", "Grade Level": "Second Grade"},
    4: {"Age": "8-9", "Grade Level": "Third Grade"},
    5: {"Age": "9-10", "Grade Level": "Fourth Grade"},
    6: {"Age": "10-11", "Grade Level": "Fifth Grade"},
    7: {"Age": "11-12", "Grade Level": "Sixth Grade"},
    8: {"Age": "12-13", "Grade Level": "Seventh Grade"},
    9: {"Age": "13-14", "Grade Level": "Eighth Grade"},
    10: {"Age": "14-15", "Grade Level": "Ninth Grade"},
    11: {"Age": "15-16", "Grade Level": "Tenth Grade"},
    12: {"Age": "16-17", "Grade Level": "Eleventh Grade"},
    13: {"Age": "17-18", "Grade Level": "Twelfth Grade"},
    14: {"Age": "18-22", "Grade Level": "College student"}
}

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)
parser.add_argument('freq_words_file', type=str)
args = parser.parse_args()

file_name = args.file
freq_words_file_name = args.freq_words_file

with open(file_name, mode='r') as f:
    text = f.read()

with open(freq_words_file_name, mode='r') as f:
    freq_words = f.read().split('\n')

pattern = r"[0-9A-z']+"

sentences = sent_tokenize(text)
words = regexp_tokenize(text, pattern)
characters = sum(1 for char in text if char not in ' \n\t')
n_of_sentences = len(sentences)
n_of_words = len(words)
syllables = 0
diff = len([element for element in words if element not in freq_words])


def count_syllables(word):
    vowel_pattern = r'[aeiouy]+'

    vowel_groups = re.findall(vowel_pattern, word, re.IGNORECASE)

    syllable_count = 0
    for group in vowel_groups:
        length = len(group)
        if length == 1:
            syllable_count += 1
        elif length == 2:
            syllable_count += 1
        elif length >= 3:
            syllable_count += 2

    silent_vowels = re.findall(r'[aeiouy]$', word, re.IGNORECASE)
    syllable_count -= len(silent_vowels)

    if syllable_count <= 0:
        syllable_count = 1

    return syllable_count


for word in words:
    syllables += count_syllables(word)

ARI = math.ceil(4.71 * (characters / n_of_words) + 0.5 * (n_of_words / n_of_sentences) - 21.43)
FKRT = math.ceil(0.39 * (n_of_words / n_of_sentences) + 11.8 * (syllables / n_of_words) - 15.59)
if (diff / n_of_words) * 100 > 5:
    DCRI = math.ceil(0.1579 * (diff / n_of_words) * 100 + 0.0496 * (n_of_words / n_of_sentences) + 3.6365)
else:
    DCRI = math.ceil(0.1579 * (diff / n_of_words) * 100 + 0.0496 * (n_of_words / n_of_sentences))


ages = grade_dict[ARI]["Age"].split('-') + grade_dict[FKRT]["Age"].split('-') + grade_dict[DCRI]["Age"].split('-')
average = sum([int(age) for age in ages]) / len(ages)


print(f'Text: {text}')
print(f'Characters: {characters}')
print(f'Sentences: {n_of_sentences}')
print(f'Words: {n_of_words}')
print(f'Difficult words: {diff}')
print(f'Syllables: {syllables}')
print(f'Automated Readability Index: {ARI} (this text should be understood by {grade_dict[ARI]["Age"]} year olds).')
print(f'Flesch–Kincaid Readability Test: {FKRT} (this text should be understood by {grade_dict[FKRT]["Age"]} year olds).')
print(f'Dale-Chall Readability Index: {DCRI} (this text should be understood by {grade_dict[DCRI]["Age"]} year olds).')
print(f'This text should be understood in average by {average} year olds.')


