  
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Loan
from .serializers import LoanSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        loan = self.get_object()
        if loan.status == 'returned':
            return Response({"error": "Книга уже возвращена"}, status=status.HTTP_400_BAD_REQUEST)
        loan.return_book()
        return Response({"status": "Книга возвращена", "fine_created": loan.status == 'overdue'})