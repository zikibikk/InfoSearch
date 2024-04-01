import os
from collections import defaultdict


def load_index(folder_path):
    index = defaultdict(dict)
    for file_name in os.listdir(folder_path):
        doc_id = file_name.split('.')[0]
        with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as f:
            for line in f:
                token, idf, tf_idf = line.strip().split()
                index[token][doc_id] = (float(idf), float(tf_idf))
    return index


def evaluate_query_similarity(query_vector, index):
    scores = defaultdict(float)
    for token, docs in index.items():
        for doc_id, (idf, tf_idf) in docs.items():
            if doc_id in query_vector:
                scores[doc_id] += query_vector[doc_id] * tf_idf
    return scores


def vector_search(query, index):
    query_vector = defaultdict(float)
    for word in query.split():
        for doc_id, (idf, tf_idf) in index.get(word, {}).items():
            query_vector[doc_id] += idf
    scores = evaluate_query_similarity(query_vector, index)
    docs_list = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return docs_list


lemmas_index = load_index('lemmas_tf_idf')

while True:
    query = input("\nВведите запрос: ")
    results = vector_search(query, lemmas_index)
    for doc_id, score in results:
        print(f"{doc_id} {score:.5f}")