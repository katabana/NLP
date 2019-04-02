import os
from elasticsearch import Elasticsearch

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


def filter_terms(terms):
	return {term: n for term, n in terms.items() if len(term) >= 2 and term.isalpha()}


def sort_terms(terms):
	return sorted(terms.items(), key=lambda x: (1/(x[1]),x[0]), reverse=False)


def main():
	dir_name = 'results'
	file_name = 'ranking'

	es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
	termVectors = get_term_vectors(es, 'test_index', 'bill', 'content', 1, 1180)
	globalTerms = make_global_term_vectors(termVectors)
	filteredTerms = filter_terms(globalTerms)
	sortedTerms = sort_terms(filteredTerms)
	os.makedirs(dir_name, exist_ok=True)
	with open('results/' + file_name, 'w+') as ranking_file: 
		ranking_file.write(str(sortedTerms))

	print(sortedTerms[:10])
	# print(len(globalTerms.keys()))
	# print(len(filteredTerms.keys()))

main()
