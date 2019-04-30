import requests
from pprint import pprint 

def get(str):
    r = requests.get(str)
    return r.json()

# def sysnset_search(lemma, pos="noun"):
#     str = "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/search?lemma={}&&&partOfSpeech={}&&&&&&".format(lemma, pos)
#     return get(str)

# def sense_get(id):
#     str = "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/{}".format(id)
#     return get(str)

# ids = [s['id'] for s in sysnset_search("szkoda")]
# print(ids)

# for id in ids:
#     pprint(sense_get(id))

def z4(id):
    str = "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/{}/relations".format(id)
    r = get(str)

    for s in r:
        if s['relation']['name'] == 'hiperonimia' and s['synsetTo']['id'] == id:
            print("---")
            pprint(s['synsetFrom'])
            pprint(s['synsetTo'])


def find_senses(synsetId, option=None):
	senses = "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/{}/senses".format(synsetId)
	sense = get(senses)
	
	result = set([])
	for s in sense:
		w = s['id']
		if option == 'words':
			w = s['lemma']['word']
		result.add(w)
	return result


def z5(id):
	str = "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/{}/relations".format(id)
	relations = get(str)

	words = []
	ids = set([])
	for r in relations:
		if r['relation']['name'] == 'hiponimia':
			result = r['synsetFrom']['id']
			source = r['synsetTo']['id']
			if source == id:
				words += find_senses(result, 'words')
				

	print("Direct hyponyms of wypadek_1 noun:\n {}\n".format(words))


def find_owing_synset(senseId):
	link = "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/{}/synset".format(senseId)
	response = get(link)
	if 'id' not in response:
		return None
	return response['id']
	

def hyponymy(id):
	str = "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/{}/relations".format(id)
	relations = get(str)
	
	ids = set([])
	for r in relations:
		if r['relation']['name'] == 'hiponimia':
			result = r['synsetFrom']['id']
			source = r['synsetTo']['id']
			if source == id:
				ids.update(find_senses(result))
	return ids


def z6(id):
	str = "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/{}/relations".format(id)
	relations = get(str)

	ids = set([])
	words = set([])
	for r in relations:
		if r['relation']['name'] == 'hiponimia':
			result = r['synsetFrom']['id']
			source = r['synsetTo']['id']
			if source == id:
				ids.update(hyponymy(result))

	for senseId in ids:
		synsetId = find_owing_synset(senseId)
		words.update(find_senses(synsetId, 'words'))

	print("Second-order hyponyms of wypadek_1 noun:\n{}\n".format(words))
	

def find_sense(word, number):
	link = "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/senses/search?lemma={}&&&partOfSpeech=noun".format(word)
	senses = get(link)['content']

	for s in senses:
		if s['senseNumber'] == number:
			return s['id']


def find_synset(word, number):
	senseId = find_sense(word, number)
	return find_owing_synset(senseId)


def z7(words):
	result = []
	ids = {}
	for word, senseNo in words:
		link_word = word.replace(" ", "%20")
		synsetId = find_synset(link_word, senseNo)
		if synsetId in ids.keys():
			ids[synsetId] += " | {}_{}".format(word, senseNo)
		else:
			ids[synsetId] = "{}_{}".format(word, senseNo)

	for key in ids.keys():
		if key is not None:
			link = "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/synsets/{}/relations".format(key)
			relations = get(link)
			for r in relations:
				source = r['synsetFrom']['id']
				next = r['synsetTo']['id']
				if next in ids.keys() and source in ids.keys():
					label = r['relation']['name']
					record = [ids[source], ids[next], label]
					if record not in result:
						result.append(record)
		else:
			print("Not found:", ids[key])
	print(ids)

	for r in result:
		print(r)
				
		

# z4(27419)
z5(3982)
z6(3982)


list_1 = [('szkoda', 2), ('strata', 1), ('uszczerbek', 1), ('szkoda majątkowa', 1), ('uszczerbek na zdrowiu', 1), ('krzywda', 1), ('niesprawiedliwość', 1), ('nieszczęście', 2)]

print("\ni.\n")
z7(list_1)

list_2 = [('wypadek', 1), ('wypadek komunikacyjny', 1), ('kolizja', 2), ('zderzenie', 2), ('kolizja drogowa', 1), ('bezkolizyjny', 2), ('katastrofa budowlana', 1), ('wypadek drogowy', 1)]

print("\nii.\n")
z7(list_2)



