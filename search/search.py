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

    def insert_document(self, index_name: str, document: dict, doc_id: Optional[str]=None):
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

    def search_term_positions(self,term: str,index_name: str, top_n: int = 5):
        # Step 1: Search for matching messages
        search_response = self.es.search(index=index_name, body={
            "query": {"match": {"text": term}},
            "size": top_n,
            "_source": ["message_id","text"]
        })
        print(search_response)
        results = []
        
        for hit in search_response["hits"]["hits"]:
            message_id = hit["_id"]

            # Step 2: Get term positions using term_vectors
            term_vector_response = self.es.termvectors(
                index=index_name,
                id=message_id,
                fields=["text"],
                term_statistics=False,
                positions=True,
                offsets=True,
                filter={"term": {"text": term}}
            )

            matches = []
            if "term_vectors" in term_vector_response and "text" in term_vector_response["term_vectors"]:
                terms = term_vector_response["term_vectors"]["text"]["terms"]
                for word, details in terms.items():
                    if "tokens" in details:
                        for token in details["tokens"]:
                            matches.append({
                                "term": word,
                                "start_offset": token["start_offset"],
                                "end_offset": token["end_offset"]
                            })

            results.append({"message_id": message_id, "matches": matches})
        print(results)
        return results
