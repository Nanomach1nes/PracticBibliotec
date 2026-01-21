  
from django.db import models
from django.utils import timezone
from apps.books.models import Book
from apps.readers.models import Reader
from apps.librarians.models import Librarian

class Loan(models.Model):
    LOAN_TYPE_CHOICES = [
        ('home', 'На дом'),
        ('hall', 'В читальный зал'),
    ]
    STATUS_CHOICES = [
        ('issued', 'Выдана'),
        ('returned', 'Возвращена'),
        ('overdue', 'Просрочена'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    librarian = models.ForeignKey(Librarian, on_delete=models.SET_NULL, null=True, blank=True)
    issue_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()  # Плановая дата возврата
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='issued')
    loan_type = models.CharField(max_length=10, choices=LOAN_TYPE_CHOICES)

    def save(self, *args, **kwargs):
        # При первой выдаче — уменьшаем доступные копии
        if not self.pk and self.book.available_copies > 0:
            self.book.available_copies -= 1
            self.book.save()
        super().save(*args, **kwargs)

    def return_book(self):
        """Метод для возврата книги"""
        from apps.fines.models import Fine
        self.return_date = timezone.now()
        if self.return_date > self.due_date:
            self.status = 'overdue'
            # Создаём штраф
            Fine.objects.create(
                loan=self,
                reader=self.reader,
                amount=50,  # например, 50 руб/день
                reason="Просрочка возврата",
                status='unpaid'
            )
        else:
            self.status = 'returned'
        self.book.available_copies += 1
        self.book.save()
        self.save()

    def __str__(self):
        return f"{self.book.title} → {self.reader.full_name}"