from django.urls import path
from . import views

# root url: books/
app_name = 'books'
urlpatterns = [
    path("", views.get_authors, name ="get_authors"),
    path("<auth_tag>/", views.get_books, name="get_books"),
    path("<auth_tag>/<book_tag>/", views.get_chapters, name="get_chapters"),
    path("<auth_tag>/<book_tag>/<chapter_id>", views.get_chapter_content, name ="get_content"),
    path("next/<auth_tag>/<book_tag>/<chapter_id>", views.get_next_chapter, name="get_next_chapter"),
    # path("previous/<auth_tag>/<book_tag>/<chapter_id>", views.get_previous_chapter, name="get_previous_chapter")
]
