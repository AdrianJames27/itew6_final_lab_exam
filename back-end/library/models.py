from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    copies_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author}"
    
class BorrowTransaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_transactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[
            ('borrowed', 'Borrowed'),
            ('returned', 'Returned')
        ],
        default='borrowed'
    )
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"