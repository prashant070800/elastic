from elasticsearch import Elasticsearch
from typing import List, Dict,Optional
class Search:
    def __init__(self):
        """Initialize Elasticsearch connection"""
        self.es = Elasticsearch(["https://localhost:9200"],
                                 basic_auth=("elastic", "elastic"), verify_certs=False)

    def create_index(self, index_name: str, settings: Optional[dict]=None, mappings: Optional[dict]=None):
        """Create an index with settings and mappings"""
        if not self.es.indices.exists(index=index_name):
            body = {
                "settings": settings,
                "mappings": mappings
            }
            response = self.es.indices.create(index=index_name, body=body)
            return response.body
        return {"message": f"Index '{index_name}' already exists."}

    def get_index(self, index_name: str):
        """Retrieve index details"""
        if self.es.indices.exists(index=index_name):
            return self.es.indices.get(index=index_name)
        return {"error": f"Index '{index_name}' does not exist."}

    def insert_document(self, index_name: str, doc_id: str, document: dict):
        """Insert a single document"""
        response = self.es.index(index=index_name, id=doc_id, body=document)
        print(response)
        return response

    def insert_multiple_documents(self, index_name: str, documents: list):
        """Insert multiple documents"""
        actions = [{"_index": index_name, "_id": doc.get("id"), "_source": doc} for doc in documents]
        from elasticsearch.helpers import bulk
        response = bulk(self.es, actions)
        return response

    def search_documents(self, index_name: str, query: dict):
        """Search documents using a query"""
        response = self.es.search(index=index_name, body=query)
        print(response)
        return response
    #     response = self.es.termvectors(
    #     index=index_name,
    #     id="1",  # Document ID
    #     fields=["text"],  # Specify the field for which you need term vectors
        
    #     offsets= True,
    #     positions= True
        
    # )
    #     print(response)
