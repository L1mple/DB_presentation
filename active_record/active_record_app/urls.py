from django.urls import path

from .views import (
    AllBooksListView,
    BookDeleteView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
)

urlpatterns = [
    path("books/", BookCreateView.as_view(), name="book-list-create"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/", AllBooksListView.as_view(), name="all-books-list"),
    path("books/<int:pk>/", BookDeleteView.as_view(), name="book-delete"),
    path("books/<int:pk>/", BookUpdateView.as_view(), name="book-update"),
]
