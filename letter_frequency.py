import string

alphabet = string.ascii_letters
sentence = 'Jim quickly realized that the beautiful gowns are expensive'


def counter(text):
    return {i: text.count(i) for i in set(text) if i in alphabet}


sentence_count = counter(sentence)
max_value = max(sentence_count.values())
most_frequent_letter = ''
for key, value in sentence_count.items():
    if value == max_value:
        most_frequent_letter = key
        break

print(sentence)
print(sentence_count)
print("Most frequent letter: ", most_frequent_letter)
