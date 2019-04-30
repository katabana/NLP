import nltk 
from nltk.corpus import wordnet as wn

def similarity(word_1, word_2):
	a = wn.synset(word_1)
	b = wn.synset(word_2)
	
	print(a, b, a.lch_similarity(b))

print('Leacock-Chodorow semantic similarity')
similarity('szkoda.n.02', 'wypadek.n.01')
similarity('kolizja.n.02', 'szkoda.n.01')
similarity('nieszczęście.n.02', 'katastrofa_budowlana.n.01')


