from django.urls import path
from . import views

# root url: books/
# books/<author_tag>
# books/<book_tag>
urlpatterns = [path("", views.index, name="index")]
