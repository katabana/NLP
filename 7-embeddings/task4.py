from gensim.models import Word2Vec
from gensim.models import KeyedVectors

model = KeyedVectors.load_word2vec_format("skip_gram_v100m8.w2v.txt")

sad = model.get_vector('ne#Wysoki_Sąd::noun')
kpc = model.get_vector('ne#KPC::noun') 
konstytucja = model.get_vector('konstytucja::noun') 

result = sad - kpc + konstytucja
result_word = model.most_similar(positive=[result]) 

print('sąd wysoki - kpc + konstytucja')
print(*result_word, sep='\n')
print()

pasazer = model.get_vector('pasażer::noun')
mezczyzna = model.get_vector('mężczyzna::noun') 
kobieta = model.get_vector('kobieta::noun') 

result = pasazer - mezczyzna + kobieta
result_word = model.most_similar(positive=[result]) 

print('pasazer - mezczyzna + kobieta')
print(*result_word, sep='\n')
print()


samochód = model.get_vector('samochód::noun')
droga = model.get_vector('droga::noun') 
rzeka = model.get_vector('rzeka::noun') 

result = samochód - droga + rzeka
result_word = model.most_similar(positive=[result]) 

print('samochód - droga + rzeka')
print(*result_word, sep='\n')
print()

