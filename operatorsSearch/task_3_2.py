import json
import re

import pymorphy2
from eldar import Query

morph = pymorphy2.MorphAnalyzer(lang='ru')
input = input()
boolean_operators = ["AND", "OR", "NOT", "(", ")"]
words = re.findall('[а-я]+|[А-Я]+[а-я]+', input)
lemmatized_words = [morph.parse(word)[0].normal_form.lower() for word in words]
index = 0
while index != len(words):
    input = input.replace(words[index], f'\"{lemmatized_words[index]}\"')
    index += 1

with open("reversed_index.json", "r") as file:
    info_dict = json.loads(file.read())

keys_array = []
for lemma in info_dict:
    keys_array.append(lemma["lemma"])

eldar = Query(input)
found_words = eldar.filter(keys_array)
pages = []
for lemma in info_dict:
    if lemma["lemma"] in found_words:
        pages += (lemma["pages"])

print(set(pages))
