import os
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def read_book(path):
    with open(path, 'r', encoding='utf8') as current_file:
        text = current_file.read().replace('\n', ' ').replace('\r', ' ')
    return text


def count_words(text):
    text = text.lower()
    skips = ['.', ',', ';', ':', "'", '"', '!', '?']
    for ch in skips:
        text = text.replace(ch, '')
    words_dict = Counter(text.split())
    return words_dict


def calc_stats(words_dict):
    total_words = sum(words_dict.values())
    unique_words = len(words_dict)
    return total_words, unique_words


def calc_frequencies(words_dict):
    count_dict = Counter(words_dict.values())
    total = sum(count_dict.values())
    freq_dict = {}
    for i in list(count_dict.keys()):
        sub_dict = {a: b for a, b in count_dict.items() if i < a}
        freq_dict[i] = sum(list(sub_dict.values())) / total
    return freq_dict


def calc_frequencies_alt(words_dict):
    count_dict = Counter(words_dict.values())
    total = sum(count_dict.values())
    a = sorted(list(count_dict.keys()), reverse=True)
    b = [count_dict[i] for i in a]
    c = (np.cumsum(b) - b) / total
    d = {a[i]: c[i] for i in range(len(a))}
    return d


books = pd.DataFrame(columns=('language',
                              'author',
                              'title',
                              'length',
                              'unique'))

hamlets = pd.DataFrame(columns=('language',
                                'distribution'))

book_num, hamlet_num = 1, 1
books_dir = './docs/books'
for root, dirs, file in os.walk(books_dir):
    for name in file:
        if '.txt' in name:
            book_path = os.path.join(root, name)
            word_count = count_words(read_book(book_path))
            stats = calc_stats(word_count)
            clean_root = root.replace(books_dir, '')
            clean_root = clean_root.replace('/', ' ').replace('\\', ' ')
            clean_root = clean_root.split()
            books.loc[book_num] = (clean_root[0].capitalize(),
                                   clean_root[1].capitalize(),
                                   name.replace('.txt', '').capitalize(),
                                   stats[0],
                                   stats[1])
            book_num += 1
            if name.lower() == 'hamlet.txt':
                frequencies = calc_frequencies(word_count)
                hamlets.loc[hamlet_num] = (clean_root[0].capitalize(),
                                           frequencies)
                hamlet_num += 1

colors = {'English': "red",
          'French': 'blue',
          'German': 'orange',
          'Portuguese': 'green'}

plt.figure(figsize=(12, 5))

plt.subplot(121)
for lang in sorted(set(books.language)):
    subset = books[books.language == lang]
    plt.loglog(subset.length,
               subset.unique,
               linestyle='none',
               marker='o',
               markeredgecolor='black',
               label=lang,
               color=colors[lang],
               alpha=1)
plt.legend(loc='upper left')
plt.title("Book analysis")
plt.xlabel("Total words")
plt.ylabel("Unique words")

plt.subplot(122)
for index in range(hamlets.shape[0]):
    lang = hamlets.language[index + 1]
    dist = hamlets.distribution[index + 1]
    plt.loglog(sorted(list(dist.keys())),
               sorted(list(dist.values()), reverse=True),
               color=colors[lang],
               linewidth=2,
               label=lang)
plt.legend()
plt.title("Word frequencies in Hamlet translations")
plt.xlabel("Frequency of word $W$")
plt.ylabel("Fraction of words with greater frequency than $W$")
plt.xlim([0, 2e3])

plt.savefig('plots/language_processing')
plt.show()
