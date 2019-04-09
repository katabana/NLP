import os
import json
import string
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


def get_term_vectors(es, index, doc_type, field, start, end):
	termVectors = {}
	for ID in range(start, end + 1):
		v = es.termvectors(index=index, doc_type=doc_type, id=ID, fields=field)
		terms = v['term_vectors']
		termVectors[ID] = terms
		print(terms)
		exit(0)
	return termVectors


def read_bigrams(text):
	text = text.translate(str.maketrans('', '', string.punctuation))
	words = text.split()
	bigrams = []
	i = 1
	while i < len(words):
		bigrams.append(words[i - 1] + ' ' + words[i])
		i = i + 1
	return bigrams


def main():
	dir_name = 'results'
	ustawy_dir = 'ustawy'
	file_name = 'ranking_2'

	es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
	index = create_index(es)

	all_bigrams = []
	if os.path.exists(dir_name):
		os.makedirs(dir_name, exist_ok=True)
		n = 1
		for filename in os.listdir(ustawy_dir):
			name = filename[:-4]
			with open(ustawy_dir + '/' + filename, 'r') as bill_file:
				bill = bill_file.read() 
				bill = bill.replace('\n', ' ')
				bill = bill.replace('\xad', '')
				bill = bill.replace('-', '')
				bill = bill.lower()
				bigrams = read_bigrams(bill)
				all_bigrams += bigrams
				#e = es.index(index='bigrams', ignore=400, doc_type='bill', id=str(n), body=data_json)
			n = n + 1
	print(all_bigrams)
			
	# termVectors = get_term_vectors(es, 'bigrams', 'bill', 'content', 1, 1180)


	#  with open('results/' + file_name, 'w+') as ranking_file: 
	#  	  ranking_file.write(str(sortedTerms))

	# print(len(globalTerms.keys()))
	# print(len(filteredTerms.keys()))

main()
