import json

from elasticsearch import Elasticsearch


es = Elasticsearch("http://elas:9200")

print(es.info())