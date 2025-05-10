from rest_framework import serializers
from .models import Book, BorrowTransaction
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowTransactionSerializer(serializers.ModelSerializer):
    # Nested details can be shown for better response data.
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = BorrowTransaction
        fields = '__all__'