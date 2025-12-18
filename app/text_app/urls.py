from django.urls import path
# URL routing utility for mapping endpoints to view classes

from .views import Submit, Search
# Import API views responsible for paragraph submission and search


urlpatterns = [
    # Endpoint for submitting multiple paragraphs for processing
    path("submit/", Submit.as_view()),

    # Endpoint for searching top paragraphs by word frequency
    path("search/", Search.as_view()),
]