  
from django.urls import path
from .views import (
    OverdueLoansReport,
    PopularBooksReport,
    FinesTotalReport,
    ReadersActivityReport,
    BooksByGenreReport
)

urlpatterns = [
    path('overdue/', OverdueLoansReport.as_view(), name='overdue-report'),
    path('popular-books/', PopularBooksReport.as_view(), name='popular-books-report'),
    path('fines-total/', FinesTotalReport.as_view(), name='fines-total-report'),
    path('readers-activity/', ReadersActivityReport.as_view(), name='readers-activity-report'),
    path('books-by-genre/', BooksByGenreReport.as_view(), name='books-by-genre-report'),
]