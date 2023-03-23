import json
import os
from math import log
from pathlib import Path

pages_path = Path("pages")
pages_files = os.listdir(pages_path)
lemmas = []
reversed_index_json = json.load(open("reversed_index.json"))
for entry in reversed_index_json:
    forms = entry["forms"]
    new_list = list(filter((entry["lemma"]).__ne__, forms))
    new_list.append(entry["lemma"])
    lemmas.append(new_list)
print(lemmas)
token_in_docs_map = {}
lemmas_in_docs_map = {}
entries_idf_map = {}
lemmas_idf_map = {}
with open("tokens.txt", "r") as tokens_file:
    tokens = tokens_file.readlines()
    stripped_tokens = [x.strip("\n") for x in tokens]
    total_files = len(pages_files)
    counter_files = 0
    for file in pages_files:
        print(f"{counter_files} / {total_files}")
        counter_files += 1
        with open(Path("pages", file), "r") as html_file:
            text = html_file.read()
            new_text = text.replace('­', '').lower()
            entries_occurancies_map = {}
            entries_tf_map = {}
            lemmas_occurancies_map = {}
            lemmas_idf_map = {}
            lemmas_tf_map = {}
            for token in stripped_tokens:
                in_text = True if new_text.count(token) > 0 else False
                if token not in token_in_docs_map.keys():
                    token_in_docs_map[token] = 0 if not in_text else 1
                else:
                    if in_text:
                        token_in_docs_map[token] += 1
                entries_occurancies_map[token] = new_text.count(token)
            for lemma in lemmas:
                for word in lemma:
                    in_text = True if new_text.count(word) > 0 else False
                    if lemma[-1] not in lemmas_in_docs_map.keys():
                        if not in_text:
                            lemmas_in_docs_map[lemma[-1]] = 0
                        else:
                            lemmas_in_docs_map[lemma[-1]] = 1
                            break
                    else:
                        if in_text:
                            lemmas_in_docs_map[lemma[-1]] += 1
                            break
                for word in lemma:
                    if lemma[-1] not in lemmas_occurancies_map.keys():
                        lemmas_occurancies_map[lemma[-1]] = new_text.count(word)
                    else:
                        lemmas_occurancies_map[lemma[-1]] += new_text.count(word)
            total_tokens_occurance = sum(entries_occurancies_map.values())
            total_lemmas_occurance = sum(lemmas_occurancies_map.values())
            entries_tf_file_name = f"entries_tf_idf_pages/{file.rstrip('.html')}_tf.txt"
            lemmas_tf_file_name = f"lemmas_tf_idf_pages/{file.rstrip('.html')}_tf.txt"
            for token in stripped_tokens:
                token_tf = entries_occurancies_map[token] / total_tokens_occurance
                with open(entries_tf_file_name, "a") as tf_file:
                    tf_file.write(f"{token} {token_tf}\n")

            for lemma in lemmas_occurancies_map:
                lemma_tf = lemmas_occurancies_map[lemma] / total_lemmas_occurance
                with open(lemmas_tf_file_name, "a") as tf_file:
                    tf_file.write(f"{lemma} {lemma_tf}\n")
entries_pages = os.listdir("entries_tf_idf_pages")
lemmas_pages = os.listdir("lemmas_tf_idf_pages")
token_index = 0
for token in token_in_docs_map.keys():
    idf = log(len(pages_files) / token_in_docs_map[token], 2) if token_in_docs_map[token] != 0 else 0
    entries_idf_map[token] = idf
for lemma in lemmas_in_docs_map.keys():
    idf = log(len(pages_files) / lemmas_in_docs_map[lemma], 2) if lemmas_in_docs_map[lemma] != 0 else 0
    lemmas_idf_map[lemma] = idf
for entries_file in entries_pages:
    with open(Path("entries_tf_idf_pages", entries_file), 'r') as file:
        # read a list of lines into data
        data = file.readlines()
        counter = 0
        while counter != len(data):
            splitted_string = data[counter].rstrip("\n").split(" ")
            tf = float(splitted_string[1])
            token = splitted_string[0]
            data[counter] = data[counter].rstrip("\n") + f" {tf * entries_idf_map[token]}\n"
            counter += 1
        # and write everything back
        with open(Path("entries_tf_idf_pages", entries_file), 'w') as new_file:
            new_file.writelines(data)

for lemmas_file in lemmas_pages:
    with open(Path("lemmas_tf_idf_pages", lemmas_file), 'r') as file:
        # read a list of lines into data
        data = file.readlines()
        counter = 0
        while counter != len(data):
            splitted_string = data[counter].rstrip("\n").split(" ")
            tf = float(splitted_string[1])
            token = splitted_string[0]
            data[counter] = data[counter].rstrip("\n") + f" {tf * lemmas_idf_map[token]}\n"
            counter += 1
        # and write everything back
        with open(Path("lemmas_tf_idf_pages", lemmas_file), 'w') as new_file:
            new_file.writelines(data)
