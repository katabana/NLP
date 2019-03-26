import os
import json
import requests
from elasticsearch import Elasticsearch

    
def main():

    url = "http://localhost:9200/acts"
    headers = {'Content-Type': 'application/json'}
    es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])

    dir_path = 'ustawy'
    all_references = []
    dir_name = 'jsons'
    os.makedirs(dir_name, exist_ok=True) 
    n = 1
    for filename in os.listdir(dir_path):
        name = filename[:-4]
        if n > 0:
            with open('ustawy/' + filename, 'r') as bill_file:
                bill = bill_file.read()
                j = {"name": name, "content": bill}
                data_json = json.dumps(j)
                # response = requests.post(url, json=data_json, headers=headers)
                e = es.index(index='test_index', ignore=400, doc_type='bill', id=str(n), body=data_json)
            print(filename) 
        n = n + 1

main()
