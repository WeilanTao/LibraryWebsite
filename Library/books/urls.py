from django.urls import path
from . import views

# root url: books/
app_name = 'books'
urlpatterns = [
    path("", views.get_authors, name ="get_authors"),
    path("booklist", views.get_books, name="get_books"),
]
