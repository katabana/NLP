import os
import json
import string
import regex
from collections import Counter
from elasticsearch import Elasticsearch

def create_index(es_object, index_name='bigrams'):
    created = False
    # index settings
    settings = {
		"settings": {
		    "index" : {
		        "analysis" : {
		            "analyzer" : {
		                "lang_pl_morfologik" : {
							"type": "custom",
		                    "tokenizer" : "standard",
		                    "filter" : [
								"synonym_filter",
								"morfologik_stem",
								"lowercase"
							]
		                }
		            },
		            "filter" : {
						"filter_shingle": {
							"type": "shingle",
							"max_shingle_size": 2,
							"min_shingle_size": 2,
							"output_unigrams": 'false'
					    },
		                "synonym_filter" : {
		                    "type" : "synonym",
		                    "lenient": 'true',
		                    "synonyms" : [
								"kpk => kodeks postępowania karnego",
								"kpc => kodeks postępowania cywilnego",
								"kk => kodeks karny",
								"kc => kodeks cywilny"
							]
		                }
		            }
		        }
		    }
		},
		"mappings": {
			"bill": {
				"properties": {
					"content": {
						"type": "text",
						"analyzer": "lang_pl_morfologik"
					}
				}
			}
		}
	}

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def is_word(text):
	if regex.fullmatch(r'\b\p{L}+\b', text):
		if text in ranking.keys():
			return True
	return False


def base_form(word):
	if word in base_forms:
		return base_forms[word]
	analysis = es.indices.analyze('bigrams',
		{
			"tokenizer": "standard",
			"filter": ["synonym_filter", "morfologik_stem"],
			"text": word
		}
	)
	base = analysis["tokens"][0]["token"]
	base_forms[word] = base
	return base

def read_bigrams(text):
	text = text.translate(str.maketrans('', '', string.punctuation))
	words = text.split()
	bigrams = []
	i = 1
	while i < len(words):
		a = words[i - 1]
		b = words[i]
		if is_word(a) and is_word(b):
			a = base_form(a)
			b = base_form(b)
			bigrams.append((a, b))
		i = i + 1
	return bigrams


def main():
	dir_name = 'results'
	ustawy_dir = 'ustawy'
	file_name = 'ranking_2'

	global ranking
	with open('results/ranking_2', 'r') as ranking_file:
		ranking = eval(ranking_file.read())

	global base_forms
	base_forms = {}
	global es
	es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
	index = create_index(es)

	all_bigrams = []
	n = 1
	if os.path.exists(dir_name):
		for filename in os.listdir(ustawy_dir):
			name = filename[:-4]
			with open(ustawy_dir + '/' + filename, 'r') as bill_file:
				bill = bill_file.read() 
				bill = bill.replace('\n', ' ')
				bill = bill.replace('\xad', '')
				bill = bill.lower()
				bigrams = read_bigrams(bill)
				all_bigrams += bigrams
				print(n)
			n += 1
			
			
	os.makedirs(dir_name, exist_ok=True)
	
	all_bigrams_counted = Counter()
	for bigram in all_bigrams:
		all_bigrams_counted[bigram] += 1
		
	print(all_bigrams_counted)
	
	with open('results/bigrams', 'w+') as ranking_file: 
		ranking_file.write(str(all_bigrams_counted))
			


main()
