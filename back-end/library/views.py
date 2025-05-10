from rest_framework import generics, status
from rest_framework.response import Response
from .models import Book, BorrowTransaction
from .serializers import BookSerializer, BorrowTransactionSerializer, UserSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

# Create your views here.
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        # Prevent deletion if there's any active borrow (status 'borrowed')
        if instance.borrow_transactions.filter(status='borrowed').exists():
            return Response({
                'message': 'Cannot delete a book with an active borrow record.'
            }, status=status.HTTP_400_BAD_REQUEST)

        return self.destroy(request, *args, **kwargs)
    
class BorrowBook(APIView):
    def post(self, request):
        book_id = request.data.get('book_id')
        user_id = request.data.get('user_id')
        borrow_date = request.data.get('borrow_date')

        if not book_id or not user_id:
            return Response({
                'message': 'Missing Book ID or User ID'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if borrow_date:
            try:
                borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({
                    'message': 'Invalid date format.'
                }, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({
                'message': 'Book not found.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if book.copies_available < 1:
            return Response({
                'message': 'No copies available.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Deduct 1 available copy
        book.copies_available -= 1
        book.save()

        # Record the borrow transaction
        transaction = BorrowTransaction.objects.create(book=book, user_id=user_id, borrow_date=borrow_date)
        serializer = BorrowTransactionSerializer(transaction)

        return Response({
            'message': 'Book borrowed successfully.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
class ReturnBook(APIView):
    def post(self, request, borrow_id):
        transaction = get_object_or_404(BorrowTransaction, id=borrow_id)
        return_date = request.data.get('return_date')

        if transaction.status == 'returned':
            return Response({
                'message': 'This book has already been returned.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if return_date:
            try:
                return_date = datetime.strptime(return_date, '%Y-%m-%d').date()

                # Prevent return_date from being before borrow_date
                if return_date < transaction.borrow_date:
                    return Response({
                        'message': 'Return date cannot be before borrow date.'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({
                    'message': 'Invalid date format.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        transaction.status = 'returned'
        transaction.return_date = return_date
        transaction.save()

        # Increment the available copy count for the returned book
        book = transaction.book
        book.copies_available += 1
        book.save()

        serializer = BorrowTransactionSerializer(transaction)

        return Response({
            'message': 'Book returned successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
class TransactionList(APIView):
    def get(self, request):
        transactions = BorrowTransaction.objects.all()
        serializer = BorrowTransactionSerializer(transactions, many=True)

        return Response({
            'message': 'Fetch success.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class AvailableBooks(APIView):
    def get(self, request):
        books = Book.objects.filter(copies_available__gt=0)
        serializer = BookSerializer(books, many=True)

        return Response({
            'message': 'Fetch success.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
class UserListView(generics.ListAPIView):
    # exclude the super users
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer