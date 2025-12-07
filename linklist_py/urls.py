# linklist_py/urls.py
from django.urls import path
from . import views

app_name = "linklist_py"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/create/", views.api_create, name="api_create"),
    path("api/destroy/", views.api_destroy, name="api_destroy"),
    path("api/insert_head/", views.api_insert_head, name="api_insert_head"),
    path("api/insert_tail/", views.api_insert_tail, name="api_insert_tail"),
    path("api/insert_at/", views.api_insert_at, name="api_insert_at"),
    path("api/delete_value/", views.api_delete_value, name="api_delete_value"),
    path("api/delete_at/", views.api_delete_at, name="api_delete_at"),
    path("api/reverse/", views.api_reverse, name="api_reverse"),
    path("api/search/", views.api_search, name="api_search"),
    path("api/size/", views.api_size, name="api_size"),
    path("api/snapshot/", views.api_snapshot, name="api_snapshot"),
]
