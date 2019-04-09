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


def print_llr(sorted_bigrams):
	n = 1
	for keys, val in sorted_bigrams:
		print("{}. {}, {} : {}".format(n, keys[0], keys[1], val))
		n += 1


def main():
	global ranking
	global bigrams	
	global cached

	ranking = []
	bigrams = {}
	cached = {}
	with open('results/ranking_2', 'r') as ranking_file:
		ranking = eval(ranking_file.read())

	with open('results/bigrams', 'r') as bigrams_file:
		bigrams = eval(bigrams_file.read())

	words_count = sum(ranking.values())
	# print(words_count)
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
	print_llr(a[:30])
	

main()


