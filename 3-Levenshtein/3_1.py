import os
import re
import Levenshtein as l


def known(words, ranking, poldict):
	# if in dictionary
	result = set(w for w in words if w in poldict)
	# if more than 10 times in the ranking
	for pos, _ in filter_rank(ranking, 10, 100000000):
		if pos in words:
			result.add(pos)


def distances_occur(word, ranking):
	result = []
	for pos, n in filter_rank(ranking, 10, float('inf')):
		distance = l.distance(word, pos)
		result.append((pos, distance, n))

	return sorted(result, key=lambda x: (x[1], 1/(x[2]), x[0]))


# list of (word from dict, distance)
def distances_dict(word, poldict):
	res = [(w, l.distance(word, w)) for w in poldict]
	return sorted(res, key=lambda x: x[1])


def possibilities(word, dist_dict, dist_occur):
	current_best = ('', float('inf'), '')
	for pos, dist, n in dist_occur:
		p = (dist)**4 * 1/n
		if p < current_best[1]:
			current_best = (pos, p, word)	

	# print(current_best)
	for w, dist in dist_dict:
		p = (dist/10)**3
		if p < current_best[1]:
			current_best = (w, p, word)

	return current_best


def find_corrections(words, dictionary, ranking):
	for word_entry in words:
		word = word_entry[0]
		# find the most probable correction
		dist_dict = distances_dict(word, dictionary)[:10]
		dist_occur = distances_occur(word, ranking)[:10]
		sol = possibilities(word, dist_dict, dist_occur)
		print("SOLUTION", sol)
		print("**")

def sort_rank(rank):
	return sorted(rank, key=lambda x: (1/(x[1]),x[0]), reverse=False)


def filter_rank(rank, occurences_min, occurences_max=None):
	if not occurences_max:
		occurences_max = occurences_min
	return [x for x in rank if x[1] >= occurences_min and x[1] <= occurences_max]


def main():
	with open('results/dict', 'r') as dict_file:
		dictionary = eval(dict_file.read())

		exists = os.path.isfile('results/ranking_not_in_dict')
		if not exists:

			# make a new ranking
			ranking = []
			with open('results/ranking', 'r') as ranking_file:
				ranking = eval(ranking_file.read())

			not_in_dict = []
			for word, n in ranking:
				if word not in dictionary:
					not_in_dict.append((word, n))

			with open('results/ranking_not_in_dict', 'w+') as new_ranking:
				new_ranking.write(str(not_in_dict))

		with open('results/ranking_not_in_dict', 'r') as f:
			ranking = sort_rank(eval(f.read()))
			first_30 = ranking[:30]
			print("30 most often occuring words that are not in the dictionary:\n\n", first_30)
			print()
			filtered = filter_rank(ranking, 3)
			print("All the words that occur exactly 3 times:\n\n", filtered)

		print()
		print("** CORRECTIONS **")
		find_corrections(filtered, dictionary, ranking)
	

main()	
			
		
