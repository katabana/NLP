from collections import Counter 
import math
from functools import reduce

	
def add(a, n):
	if a in cached:
		cached[a] += n
	else:
		cached[a] = n


def compute_cached():
	for words, n in bigrams.items():
		a, b = words
		add((a, '_'), n)
		add(('_', b), n)


def get_table(a, b, bigrams_count):
	all_count = bigrams_count
	a_b = bigrams[(a, b)]
	xa_b = cached[('_', b)] - a_b
	a_xb = cached[(a, '_')] - a_b
	xa_xb = all_count - xa_b - a_xb - a_b
	return [a_b, a_xb, xa_b, xa_xb]


def H(k):
	N = sum(k)
	a = list(map(lambda x: x / N, k))
	l = list(map(lambda x: math.log(x + 1e-9), a))
	al = [(lambda x, y: x * y)(x, y) for x, y in zip(a, l)]
	return sum(al)


def LLR(tab):
	a_b, a_xb, xa_b, xa_xb = tab
	rowSums = [a_b + xa_b, a_xb, xa_xb]
	colSums = [a_b + a_xb, xa_b + xa_xb]
	return 2 * sum(tab) * (H(tab) - H(rowSums) - H(colSums))


def sort_bigrams(dictionary):
	return sorted(dictionary.items(), key=lambda x: (x[1]), reverse=True)


def top_50(sorted_bigrams):
	result = []
	k = 1
	print(sorted_bigrams[:20])
	for bigram in sorted_bigrams:
		((w1, c1), (w2, c2)), _ = bigram
		if k == 50:
			break

		if c1.split(':')[0] == 'subst':
			if c2.split(':')[0] in ['subst', 'adj']:
				result.append(bigram)
				k += 1

	print(result)
	n = 1
	text = ""
	for keys, val in result:
		w1, g1 = keys[0]
		w2, g2 = keys[1]
		text += "{}. {}, {} ({}, {}) : {}\n".format(n, w1, w2, g1, g2, val)
		n += 1
	return text


def main():
	global bigrams	
	global cached

	ranking = []
	bigrams = {}
	cached = {}

	with open('results/bigrams', 'r') as bigrams_file:
		bigrams = eval(bigrams_file.read())

	bigrams_count = sum(bigrams.values())
	# print(bigrams_count)

	compute_cached()

	LLR_bigrams = {}
	for bigram in bigrams:
		a, b = bigram
		t = get_table(a, b, bigrams_count)
		score = LLR(t)
		LLR_bigrams[(a, b)] = score		
	

	a = sort_bigrams(LLR_bigrams)
	with open('results/llr_results', 'w+') as llr_file:
		llr_file.write(top_50(a))

main()


