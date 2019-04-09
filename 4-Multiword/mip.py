import os
import math
from collections import Counter
from functools import reduce

def p_c(x, y, bigrams_count):
	return float(bigrams[(x, y)]) / float(bigrams_count)


def p(a, words_count):
	if a not in ranking.keys():
		print("error", a)
	else:
		return float(ranking[a]) / float(words_count)

def is_in(a):
	return a in ranking.keys()


def pmi(x, y, words_count, bigrams_count):
	p_xy = p_c(x, y, bigrams_count)
	p_x = p(x, words_count)
	p_y = p(y, words_count)
	return math.log(p_xy / (p_x * p_y))


def sort_bigrams(dictionary):
	return sorted(dictionary.items(), key=lambda x: (x[1]), reverse=True)


def print_mip(sorted_bigrams):
	n = 1
	for keys, val in sorted_bigrams:
		print("{}. {}, {} : {}".format(n, keys[0], keys[1], val))
		n += 1

def main():
	global ranking
	global bigrams	

	ranking = []
	bigrams = {}
	with open('results/ranking_2', 'r') as ranking_file:
		ranking = eval(ranking_file.read())

	with open('results/bigrams', 'r') as bigrams_file:
		bigrams = eval(bigrams_file.read())

	words_count = sum(ranking.values())
	# print(words_count)
	bigrams_count = sum(bigrams.values())
	# print(bigrams_count)
	

	pmis = {}
	n = 0
	for bigram in bigrams:
		# if n % 20 == 0:
		# 	 print("{}/{}".format(n, len(bigrams)))
		a, b = bigram
		if is_in(a) and is_in(b):
			res = pmi(a, b, words_count, bigrams_count)
			pmis[bigram] = res
		n += 1

	
	with open('results/pmis', 'w+') as pmis_file:
		pmis_file.write(str(pmis))


	pmis_sorted = sort_bigrams(pmis)
	with open('results/pmis_sorted', 'w+') as pmis_file:
		pmis_file.write(str(pmis_sorted))

	print_mip(pmis_sorted[:30])

main()
