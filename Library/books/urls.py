from django.urls import path
from . import views

# root url: books/
app_name = 'books'
urlpatterns = [
    path("", views.get_authors, name ="get_authors"),
    path("<author_tag>/", views.get_books, name="get_books"),
    path("<author_tag>/<book_tag>/", views.get_chapters, name="get_chapters"),
    path("<author_tag>/<book_tag>/<chapter_id>", views.get_chapter_content, name ="get_content"),
    path("<author_tag>/<book_tag>/<chapter_id>/<next_previous>", views.get_next_previous, name="next_previous"),
]
