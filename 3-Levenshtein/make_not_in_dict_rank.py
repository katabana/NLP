import os

def main():
	with open('results/dict', 'r') as dict_file:
		dictionary = eval(dict_file.read())

		ranking = []
		with open('results/ranking', 'r') as ranking_file:
			ranking = eval(ranking_file.read())

		not_in_dict = []
		for word, n in ranking:
			if word not in dictionary:
				not_in_dict.append((word, n))

		with open('results/ranking_not_in_dict', 'w+') as new_ranking:
			new_ranking.write(str(not_in_dict))

main()	
			
		
