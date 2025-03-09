from django.urls import path
from .views import create_index, insert_document, search_documents,list_indexes

urlpatterns = [
    path("list_indexes/", list_indexes, name="list_indexes"),
    path("create_index/", create_index, name="create_index"),
    path("insert_document/", insert_document, name="insert_document"),
    path("search/", search_documents, name="search_documents"),
]
