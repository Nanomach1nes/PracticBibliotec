  
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.loans.models import Loan
from apps.fines.models import Fine
from apps.books.models import Book
from apps.readers.models import Reader
from django.db.models import Count, Sum
from datetime import timedelta

class OverdueLoansReport(APIView):
    """Отчёт: просроченные выдачи"""
    def get(self, request):
        overdue = Loan.objects.filter(status='overdue')
        data = [{
            'book': l.book.title,
            'reader': l.reader.full_name,
            'due_date': l.due_date.strftime('%Y-%m-%d %H:%M'),
            'days_overdue': (timezone.now() - l.due_date).days
        } for l in overdue]
        return Response(data)

class PopularBooksReport(APIView):
    """Отчёт: топ-10 самых популярных книг"""
    def get(self, request):
        popular = Book.objects.annotate(num_loans=Count('loan')).order_by('-num_loans')[:10]
        data = [{'title': b.title, 'loans': b.num_loans} for b in popular]
        return Response(data)

class FinesTotalReport(APIView):
    """Отчёт: финансовые итоги по штрафам"""
    def get(self, request):
        total_unpaid = Fine.objects.filter(status='unpaid').aggregate(total=Sum('amount'))['total'] or 0
        total_paid = Fine.objects.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
        return Response({
            'unpaid_total': total_unpaid,
            'paid_total': total_paid,
            'total_fines': total_unpaid + total_paid
        })

class ReadersActivityReport(APIView):
    """Отчёт: активность читателей (сколько книг взяли)"""
    def get(self, request):
        readers = Reader.objects.annotate(books_taken=Count('loan')).order_by('-books_taken')[:10]
        data = [{'name': r.full_name, 'books_taken': r.books_taken} for r in readers]
        return Response(data)

class BooksByGenreReport(APIView):
    """Отчёт: книги по жанрам"""
    def get(self, request):
        genres = Book.objects.values('genre__name').annotate(count=Count('id')).order_by('-count')
        data = [{'genre': g['genre__name'], 'count': g['count']} for g in genres if g['genre__name']]
        return Response(data)