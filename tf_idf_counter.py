import os
import math
from collections import defaultdict
from bs4 import BeautifulSoup

output_dirs = ['tokens_tf_idf', 'lemmas_tf_idf']
for output_dir in output_dirs:
    os.makedirs(output_dir, exist_ok=True)

html_folder = 'files_new'
tokens_file = 'tokens.txt'
lemmas_file = 'lemmas.txt'

tokens = set()
token_to_lemmas = {}
with open(tokens_file, 'r', encoding='utf-8') as f:
    tokens = set(line.strip() for line in f.readlines())

with open(lemmas_file, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split()
        token_to_lemmas[parts[0]] = parts[1:]

df_tokens = defaultdict(int)
df_lemmas = defaultdict(int)

num_documents = len(os.listdir(html_folder))

for file_name in os.listdir(html_folder):
    path = os.path.join(html_folder, file_name)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text().lower()
        words = text.split()

        unique_words = set(words)
        for word in unique_words:
            if word in tokens:
                df_tokens[word] += 1
            if word in token_to_lemmas:
                for lemma in token_to_lemmas[word]:
                    df_lemmas[lemma] += 1

idf_tokens = {token: math.log(num_documents / df) for token, df in df_tokens.items()}
idf_lemmas = {lemma: math.log(num_documents / df) for lemma, df in df_lemmas.items()}

for file_name in os.listdir(html_folder):
    path = os.path.join(html_folder, file_name)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text().lower()
        words = text.split()
        total_words = len(words)

        tf_tokens = defaultdict(int)
        tf_lemmas = defaultdict(int)

        for word in words:
            if word in tokens:
                tf_tokens[word] += 1
            if word in token_to_lemmas:
                for lemma in token_to_lemmas[word]:
                    tf_lemmas[lemma] += 1

        tf_tokens = {token: count / total_words for token, count in tf_tokens.items()}
        tf_lemmas = {lemma: count / total_words for lemma, count in tf_lemmas.items()}

        tokens_tf_idf = {token: (tf * idf_tokens[token]) for token, tf in tf_tokens.items()}
        lemmas_tf_idf = {lemma: (tf * idf_lemmas.get(lemma, 0)) for lemma, tf in tf_lemmas.items()}

        result_file_name = file_name.replace('.html', '')

        with open(os.path.join('tokens_tf_idf', f'{result_file_name}.txt'), 'w', encoding='utf-8') as f:
            for token, tf_idf in tokens_tf_idf.items():
                f.write(f"{token} {idf_tokens[token]} {tf_idf}\n")

        with open(os.path.join('lemmas_tf_idf', f'{result_file_name}.txt'), 'w', encoding='utf-8') as f:
            for lemma, tf_idf in lemmas_tf_idf.items():
                f.write(f"{lemma} {idf_lemmas.get(lemma, 0)} {tf_idf}\n")
