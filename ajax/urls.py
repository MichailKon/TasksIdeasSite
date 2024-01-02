from django.urls import path

from .views import get_ideas_by_query

urlpatterns = [
    path('ajax/get_ideas_by_query', get_ideas_by_query, name='get-ideas-by-query')
]
