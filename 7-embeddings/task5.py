from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
import random

highlights = ['szkoda::noun', 'strata::noun', 'uszczerbek::noun', 'szkoda_majątkowa::noun', 'uszczerbek_na_zdrowie::noun', 'Krzywda::noun', 'niesprawiedliwość::noun', 'nieszczęście::noun']

model = KeyedVectors.load_word2vec_format("skip_gram_v100m8.w2v.txt")

hv = np.array([model.get_vector(h) for h in highlights if h in model.wv.vocab])

sd = 20 # size difference
s = 20

for i in range(5):
	words = [model.get_vector(word) for word in model.wv.vocab.keys()]
	selected = random.sample(words, k=1000)

	colors = [sd if x in hv[:] else 0 for x in selected]
	size = np.array([s + sd for sd in colors])

	for p in [10., 15., 30., 40., 50., 60.]:
		tsne = TSNE(n_components=2, perplexity=p)
		data = tsne.fit_transform(np.array(selected))

		plt.figure(figsize=(12, 9))
		plt.scatter(data[:,0], data[:,1], c=colors, cmap=plt.cm.Wistia, alpha=0.9, s=size)
		plt.savefig('tsne_{}_{}.svg'.format(p, i))
		plt.clf()
		plt.close()
