import json
import os
from pathlib import Path

pages_dir = "pages"
tokens_file = "tokens_words_txt"
words_set = set()
lemmas_array = []
counter = 0
files_in_pages_dir = os.listdir(pages_dir)
with open(tokens_file, "r") as token_file:
    readlines = token_file.readlines()
    total_lemmas = len(readlines)
    for line in readlines:
        if counter % 100 == 0:
            print(f"PROCESS: {counter}/{total_lemmas}")
        words = line.replace("\n", "").strip(" ").split(" ")
        lemmas_dict = {
            "lemma": words[0],
            "forms": words,
            "pages": []
        }
        for file in files_in_pages_dir:
            with open(Path("pages", file), "r") as html_file:
                text = html_file.read()
                new_text = text.replace('­', '').lower()
                for word in words:
                    if word in new_text and file not in lemmas_dict["pages"]:
                        lemmas_dict["pages"].append(file)
        lemmas_array.append(lemmas_dict)
        counter += 1
print(lemmas_array)
json.dumps(lemmas_array)
with open("reversed_index.json", "w", encoding='utf8') as j:
    json.dump(lemmas_array, j, ensure_ascii=False)




