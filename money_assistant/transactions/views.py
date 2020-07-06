from rest_framework import viewsets, status
from rest_framework.validators import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action

from money_assistant.transactions.serializers import (
    AccountSerializer,
    CategorySerializer,
    TransactionSerializer,
    TransactionImportSerializer,
)
from money_assistant.transactions.services import import_transactions_from_file
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

    @action(detail=False, url_path="import", methods=["post"])
    def import_from_file(self, request, **kwargs):
        file = request.FILES.get("file")
        if not file:
            raise ValidationError(detail={"file": ["This field is required."]})
        serializer = TransactionImportSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            import_transactions_from_file(file=file, **serializer.data)
        return Response("Success", status=status.HTTP_200_OK)
