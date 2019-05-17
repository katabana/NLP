import os
import random
from shutil import copyfile


def main():
	name = 'selected'
	os.makedirs(name, exist_ok=True) 

	filenames = os.listdir('ustawy')
	selected = random.sample(filenames, k=100)

	for f in selected:
		src = os.path.join('ustawy', f)
		dst = os.path.join(name, f)
		copyfile(src, dst)

main()
