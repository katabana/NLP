from gensim.models import Word2Vec
from gensim.models import KeyedVectors

model = KeyedVectors.load_word2vec_format("skip_gram_v100m8.w2v.txt")
print("model loaded")
vector = model.most_similar(positive=['ne#Wysoki_Sąd::noun'])  # numpy vector of a word

words = ['ne#Wysoki_Sąd::noun', 'ne#Trybunał_Konstytucyjny::noun', 'ne#kodeks_cywilny::noun', 'ne#KPK::noun', 'ne#Sąd_Rejonowy::noun', 'szkoda::noun', 'wypadek::noun', 'kolizja::noun', ['szkoda::noun', 'majątkowy::adj'], 'nieszczęście::noun', 'rozwód::noun']

for word in words:
	if isinstance(word, str):
		word = [word]
	vector = model.most_similar(positive=word) 
	print(word)
	print(*vector, sep='\n')
	print()


# krzywda -> krzywde || Krzywda
