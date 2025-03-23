from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .search import Search

search_service = Search()

# 📌 List all indexes
@swagger_auto_schema(
    method='get',
    operation_description="List all indexes in Elasticsearch",
    responses={200: openapi.Response("Indexes listed successfully")}
)
@api_view(['GET'])
def list_indexes(request):
    """List all indexes"""
    try:
        response = search_service.es.cat.indices(format="json")  # ✅ Correct method
        print(response)
        return JsonResponse(list(response), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# 📌 Create an index
@swagger_auto_schema(
    method='post',
    operation_description="Create an index with settings and mappings",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'index_name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the index"),
        }
    ),
    responses={200: "Index created successfully"}
)
@api_view(['POST'])
def create_index(request):
    """Create an index"""
    index_name = request.data.get("index_name")
    settings = {
        "number_of_shards": 1,
        "number_of_replicas": 1
    }
    
    mappings = {
    "properties": {
      "text": {
        "type": "text",
        "term_vector": "with_positions_offsets",
        "store": False 
      }
    }
  }               

    response = search_service.create_index(index_name, settings, mappings)
    return JsonResponse(response)

# 📌 Insert a document
@swagger_auto_schema(
    method='post',
    operation_description="Insert a document into an index",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'index_name': openapi.Schema(type=openapi.TYPE_STRING, description="Index name"),
            'message_id': openapi.Schema(type=openapi.TYPE_STRING, description="Document ID"),
            'message': openapi.Schema(type=openapi.TYPE_STRING, description="Document content"),
        }
    ),
    responses={200: "Document inserted successfully"}
)
@api_view(['POST'])
def insert_document(request):
    """Insert a document into Elasticsearch"""
    index_name = request.data.get("index_name")
    doc_id = request.data.get("message_id")
    message = request.data.get("message")

    response = search_service.insert_document(index_name, document={"message_id":doc_id, "text":message }, doc_id=doc_id)
    return JsonResponse(response.body, safe=False)

# 📌 Search in an index
@swagger_auto_schema(
    method='post',
    operation_description="Search for documents in an index",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'index_name': openapi.Schema(type=openapi.TYPE_STRING, description="Index name"),
            'query': openapi.Schema(type=openapi.TYPE_OBJECT, description="Search query"),
        }
    ),
    responses={200: "Search results"}
)
@api_view(['POST'])
def search_documents(request):
    """Search documents in Elasticsearch"""
    index_name = request.data.get("index_name")
    query = request.data.get("query")

    response = search_service.search_documents(index_name, query)
    print(response)
    return JsonResponse(response.body)

# 📌 Search in an index with term vector
@swagger_auto_schema(
    method='post',
    operation_description="Search for documents in an index",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'index_name': openapi.Schema(type=openapi.TYPE_STRING, description="Index name"),
            'term': openapi.Schema(type=openapi.TYPE_STRING, description="Search string"),
        }
    ),
    responses={200: "Search results"}
)
@api_view(['POST'])
def search_documents_terms(request):
    """Search documents in Elasticsearch"""
    index_name = request.data.get("index_name")
    term = request.data.get("term")

    response = search_service.search_term_positions(term=term, index_name=index_name)
    return JsonResponse(response.body)