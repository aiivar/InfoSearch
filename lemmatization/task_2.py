import os
import re
from pathlib import Path

import pymorphy2
import lxml.html
not_required_speech_parts = ["PRED", "PREP", "CONJ", "PRCL", "INTJ", "UNKN"]
pages_dir = "pages"
tokens_file = "tokens.txt"
words_set = set()
files_in_pages_dir = os.listdir(pages_dir)
for file in files_in_pages_dir:
    with open(Path("pages", file)) as f:
        text = f.read()
        new_text = text.replace('­', '')
        words = set(re.findall('[а-я]+|[А-Я]+[а-я]+', new_text))
        morph = pymorphy2.MorphAnalyzer(lang='ru')
        for word in words:
            speech_part = str(morph.parse(word)[0].tag).split(",")[0]
            if speech_part.split()[0] not in not_required_speech_parts and len(word) != 1:
                words_set.add(word.lower())
with open(tokens_file, "w") as f:
    for word in words_set:
        f.write(f"{word}\n")

tokens_dict = {}
for word in words_set:
    tokenized = morph.parse(word)[0].normal_form
    if tokenized not in tokens_dict.keys():
        tokens_dict[tokenized] = [word]
    else:
        tokens_dict[tokenized].append(word)
tokens_words_file = "tokens_words_txt"
with open(tokens_words_file, "w") as file:
    for key in tokens_dict.keys():
        lemmas = ""
        for lemma in tokens_dict[key]:
            lemmas += f"{lemma} "
        file.write(f"{key} {lemmas}\n")
