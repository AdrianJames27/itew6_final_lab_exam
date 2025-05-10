from django.urls import path
from .views import (
    BookListCreateView,
    BookDetailView,
    BorrowBook,
    ReturnBook,
    TransactionList,
    AvailableBooks,
    UserListView
)

urlpatterns = [
    # Books endpoints
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/available/', AvailableBooks.as_view(), name='available-books'),

    # User lists
    path('users/', UserListView.as_view(), name='user-list'),

    # Borrow and Return endpoints
    path('borrow/', BorrowBook.as_view(), name='borrow-book'),
    path('return/<int:borrow_id>/', ReturnBook.as_view(), name='return-book'),
    path('transactions/', TransactionList.as_view(), name='transaction-list')
]
