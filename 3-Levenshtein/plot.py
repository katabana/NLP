import os
import csv
import matplotlib.pyplot as plt
import numpy as np


def main():
	file_name = 'ranking'
	ranking = []
	with open('results/' + file_name, 'r') as ranking_file:
		ranking = eval(ranking_file.read())

	plot = True
	if plot:
		print(ranking[:10])
		y = [x[1] for x in ranking]
		plt.plot(range(1, len(ranking) + 1), y, 'r.', markersize=1, linestyle='')
		plt.yscale('log')
		plt.xscale('log')
		plt.savefig('results/log_scale_both.svg')

	else:
		polDict = []
		with open('polimorfologik-2.1/polimorfologik-2.1.txt') as dict_file:
			reader = csv.reader(dict_file, delimiter=';')
			for row in reader:
				word = row[0]
				if word not in polDict:
					polDict.append(word)

		print(polDict)
		with open('results/dict', 'w+') as py_dict_file:
			py_dict_file.write(str(polDict))

main()


