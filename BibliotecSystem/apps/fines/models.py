  
from django.db import models
from apps.loans.models import Loan
from apps.readers.models import Reader

class Fine(models.Model):
    STATUS_CHOICES = [
        ('unpaid', 'Не оплачен'),
        ('paid', 'Оплачен'),
    ]

    loan = models.OneToOneField(Loan, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    issue_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')

    def __str__(self):
        return f"Штраф для {self.reader.full_name}: {self.amount} руб."