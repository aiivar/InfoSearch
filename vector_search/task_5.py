import json
import math
import os
from nltk import word_tokenize

from InfoSearch.vector_search.task_3_2 import search


def read_reversed_index():
    with open('reversed_index.json')as file:
        json_index = file.read()
        index = json.loads(json_index)
        return index


def read_token_words():
    lemmas = {}
    with open('tokens_words_txt') as lemma_file:
        lines = lemma_file.readlines()
        for line in lines:
            line = line.rstrip('\n')
            words = line.split(' ')
            for word in words:
                lemmas[word] = words[0]
    return lemmas


def read_lemmas_tf_idf_pages():
    result = {}
    for file_name in os.listdir('lemmas_tf_idf_pages'):
        with open('lemmas_tf_idf_pages/' + file_name) as tf_idf_file:
            lines = tf_idf_file.readlines()
            result[file_name] = {}
            for line in lines:
                data = line.rstrip('\n').split(' ')
                result[file_name][data[0]] = float(data[2])
    return result


def read_lemmas_tf_idf():
    result = {}
    for file_name in os.listdir('lemmas_tf_idf_pages'):
        with open('lemmas_tf_idf_pages/' + file_name) as tf_idf_file:
            lines = tf_idf_file.readlines()
            for line in lines:
                data = line.rstrip('\n').split(' ')
                lemma_to_docs_tf_idf = result.get(data[0], {})
                lemma_to_docs_tf_idf[file_name] = float(data[2])
                result[data[0]] = lemma_to_docs_tf_idf
    return result


def calculate_vector_len(documents_to_words):
    return math.sqrt(sum(map(lambda i: i ** 2, documents_to_words.values())))


def multiply_vectors(query_vector, document_vector, document_vector_len):
    result = 0
    for token in query_vector:
        result += document_vector.get(token, 0)
    return result / len(query_vector) / document_vector_len


def search_in_reversed_index(index, lemma):
    for entry in index:
        if entry["lemma"] == lemma:
            return [page.replace(".html", "_tf.txt") for page in entry["pages"]]


def make_query(query):
    print(query)
    tokens = word_tokenize(query, language='russian')
    lemmas = []
    for token in tokens:
        if token.lower() in token_to_lemma:
            lemmas.append(token_to_lemma[token.lower()])
    if len(lemmas) > 1:
        search_string = ""
        for lemma in lemmas:
            search_string += f"{lemma} OR "
        new_string = search_string.rstrip(" OR ")
        doc_set = [page.replace(".html", "_tf.txt") for page in search(new_string)]
    else:
        doc_set = search_in_reversed_index(reverse_index, lemmas[0])
    results = {}
    for doc in doc_set:
        results[doc.replace("_tf.txt", ".html")] = multiply_vectors(lemmas, doc_to_lemma[doc], doc_lengths[doc])
    return dict(sorted(results.items(), key=lambda r: r[1], reverse=True))


docs_list = os.listdir('lemmas_tf_idf_pages')
doc_to_lemma = read_lemmas_tf_idf_pages()
lemma_to_doc = read_lemmas_tf_idf()
doc_lengths = {doc: calculate_vector_len(doc_to_lemma[doc]) for doc in docs_list}
token_to_lemma = read_token_words()
reverse_index = read_reversed_index()

if __name__ == '__main__':
    test_query = 'Пушкин Лермонтов'
    print(make_query(test_query))
    test_query = 'ложка'
    print(make_query(test_query))
