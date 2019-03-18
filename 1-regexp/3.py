import regex
import os


# PROBLEM:
# count adjectives/adverbs too?
# without ustawod.*


def invalid_word(word):
    match = (regex.match(r'\bustawicz\p{L}*\b', word)) or \
            (regex.match(r'\bustawyz\b', word)) or \
            (regex.match(r'\bustawow\p{L}*\b', word)) or \
            (regex.match(r'\bustaworaz\b', word)) or \
            (regex.match(r'\bustawod\p{L}*\b', word)) or \
            (regex.match(r'\bustawia\p{L}*\b', word)) or \
            (regex.match(r'\bustawio\p{L}*\b', word))
    return match


def find_references(file_path):
    # print(file_path)

    word_count = 0

    with open(file_path, 'r') as bill_file:
        bill = bill_file.read()
        bill = regex.sub(r'[\t\p{Zs}\xA0\n]+', ' ', bill)  # remove redundant spaces
        lowercase_bill = bill.lower()

        words = regex.findall(r'\bustaw\p{L}*?\b', lowercase_bill)

        word_count += len(words)

        word_set = []
        for word in words:
            # check if valid
            if invalid_word(word):
                word_count -= 1
                # don't add to word_set
            else:
                if word in word_set:
                    pass
                else:
                    word_set.append(word)

    return word_count, word_set


def add_words(words, word_set):
    for word in words:
        if word not in word_set:
            word_set.append(word)


def main():
    dir_path = 'ustawy'
    word_set = []
    total = 0

    n = 0
    for filename in os.listdir(dir_path):
        if n < 2000:
            count, words = find_references('{}/{}'.format(dir_path, filename))
            add_words(words, word_set)
            total += count
            # print('count', total)
            # print('set', word_set)
        n = n + 1
    print('Total count', total)
    print('Word set', word_set)

main()
