import os
from elasticsearch import Elasticsearch
import string


def get_term_vectors(es, index, doc_type, field, start, end):
	termVectors = {}
	for ID in range(start, end + 1):
		v = es.termvectors(index=index, doc_type=doc_type, id=ID, fields=field)
		terms = v['term_vectors'][field]['terms']
		termVectors[ID] = terms
	return termVectors


def make_global_term_vectors(termVectors):
	globalTerms = {}
	for bill_vectors in termVectors.values():
		for term, info in bill_vectors.items():
			last_value = 0
			if term in globalTerms:
				last_value = globalTerms[term]
			
			globalTerms[term] = last_value + info['term_freq']
	return globalTerms


def sort_ranking(dictionary):
	return sorted(dictionary.items(), key=lambda x: (1/x[1], x[0]), reverse=False)


def filter_terms(terms):
	return {term: n for term, n in terms.items() if term.isalpha()}

es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
termVectors = get_term_vectors(es, 'test_index', 'bill', 'content', 1, 1180)
globalTerms = make_global_term_vectors(termVectors)
filteredTerms = filter_terms(globalTerms)

os.makedirs('results', exist_ok=True)
with open('results/ranking_2', 'w+') as ranking_file: 
	ranking_file.write(str(filteredTerms))

