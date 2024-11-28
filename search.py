import json
from pprint import pprint
import os
import time

from dotenv import load_dotenv
from elasticsearch import Elasticsearch,exceptions

load_dotenv()


class Search:
    def __init__(self):
        self.es = Elasticsearch("http://elas:9200")  # <-- connection options need to be added here
        retries = 1
        while retries > 0:
            try:
                client_info = self.es.info()
                print('Connected to Elasticsearch!')
                pprint(client_info.body)
                break
            except exceptions.ConnectionError as e:
                print(exceptions)
                time.sleep(5)
                retries-=1

    def create_index(self,index_name='documents'):
        """

        :param index_name: Accepts index_name , checks if it exists and delete and creates a new one
        :return: None
        """
        self.es.indices.delete(index=index_name,ignore_unavailable=True)
        self.es.indices.create(index=index_name)

    def insert_document(self,document,index_name='documents'):
        """

        :param document: This is the document you want to index
        :param index_name: This is the index name which is like the database
        :return: Elasticsearch service returns a response but we need the response[_'id'] the most
        """
        return self.es.index(index=index_name,body=document)

    def insert_documents(self,documents,index_name='documents'):
        operations = []
        for document in documents:
            operations.append({'index':{
                '_index':index_name
            }})
            operations.append(document)

        return self.es.bulk(operations=operations)

    def reindex(self):
        """
        Reindex the document
        :return: response from bULK()
        """
        self.create_index()
        with open('data.json', 'rt') as f:
            documents = json.loads(f.read())
        return self.insert_documents(documents)

    def search(self,index_name='documents',**query_args):
        return self.es.search(index=index_name,**query_args)

    def retrieve_document(self, id, index_name='documents'):
        return self.es.get(index=index_name, id=id)


