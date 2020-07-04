from rest_framework import viewsets

from money_assistant.transactions.serializers import (
    AccountSerializer,
    CategorySerializer,
    TransactionSerializer,
)
from money_assistant.transactions.models import Account, Category, Transaction


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_fields = ("account", "category", "kind")
