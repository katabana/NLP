import os
from collections import Counter

excluded = ['interp']


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def read_lines(text):
	words = []
	lines = text.splitlines()
	i = 0
	while i < len(lines):
		if not lines[i]:
			i += 1
		else:
			word, category = lines[i + 1].split()[:2]
			if category in excluded or is_number(word):
				# print(category)
				pass
			else:
				words.append((word, category))
			i += 2
	return words


def read_bigrams(text):
	bigrams = []
	words = read_lines(text)
	for i in range(len(words) - 1):
		bigrams.append((words[i], words[i + 1]))
	return bigrams



def main():
	dir_name = 'tokeny'
	result_dir = 'results'

	all_bigrams = [] 

	all_bigrams_counted = Counter()

	n = 0
	if os.path.exists(dir_name):
		os.makedirs(result_dir, exist_ok=True)
		for filename in os.listdir(dir_name):
			if n % 20 == 0:
				print(n)
			# print(filename)
			name = filename[:-4]
			with open(dir_name + '/' + filename, 'r') as tokens_file:
				tokens = tokens_file.read()
				bigrams = read_bigrams(tokens)
				
				# get bigrams
				for bigram in bigrams:
					all_bigrams_counted[bigram] += 1
				# print(all_bigrams_counted)
			n += 1

		# print(all_bigrams_counted)
		with open(result_dir + '/bigrams', 'w+') as ranking_file: 
			ranking_file.write(str(all_bigrams_counted))

main()
